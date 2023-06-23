import os
import polars as pl

from typing import Optional
from jose import jwt
from passlib.hash import sha256_crypt
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from datetime import (
    datetime,
    timedelta,
)
from fastapi import (
    APIRouter,
    status,
    HTTPException,
    Depends,
)
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)

from app.database.database_init import (
    get_db,
    config,
    logger,
    engine,
)
from app.models.model_pydantic import (
    ApiUserCreate,
    Token,
)
from app.crud.crud_user import (
    get_user_by_login,
    get_all_users,
    get_password_hash,
)
from app.database import DPredictORM
from app.helpers import load_csv_file


logger.info(msg="Program start !")

ALGORITHM = config.get("algorithm")
ACCESS_TOKEN_EXPIRE_MINUTES = config.get("acces_token_expire_minutes")
API_SERVICE_NAME = config.get("api_service_name")
API_VERSION = config.get("api_version")
API_VERSION_SERVER = config.get("api_version_server")
SECRET_KEY = config.get("secret_key")



router = APIRouter(
    prefix="/login",
    tags=["Login"],
    responses={404: {"description": "Not found"}},

)


def create_user_admin_default(
        admin_default: dict,
        db: Session = Depends(get_db),
) -> None:
    """
    Default Admin user creation
    :param admin_default: dict
    :param db: database
    :return: None
    """

    all_users = get_all_users(db=db)
    logins = [
        jsonable_encoder(user)["login"]
        for user in all_users
    ]

    if admin_default["login"] not in logins:
        hashed_password = get_password_hash(
            admin_default["password"],
        )
        db_user = DPredictORM.ApiUser(
            login=admin_default["login"],
            password=hashed_password,
            admin=admin_default["admin"],
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        # insert de reference csv data to database
        bdd_insert_data(db)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(
        passed_password,
        hashed_password,
) -> bool:
    """
    Verify the inquired password
    :param passed_password: string
    :param hashed_password: string
    :return: boolean
    """
    return sha256_crypt.verify(
        passed_password,
        hashed_password,
    )


def get_user(
        login: str,
        db: Session = Depends(get_db),
) -> ApiUserCreate:
    """ Check if the user exists
    :param login: API user --> address email
    :param db: database
    :return: class user
    """

    user = get_user_by_login(db=db, login=login)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"login : {login} not found",
        )

    # Convert user object into dict
    user_dict = jsonable_encoder(user)
    return ApiUserCreate(**user_dict)



def authenticate_user(
        login: str,
        password: str,
        db: Session = Depends(get_db),
) -> ApiUserCreate:
    """
    User authentication by checking information in database
    :param login: API user
    :param password: password str
    :param db: database str
    :return: API user
    """

    logger.info(msg="Authentication start")
    user = get_user(
        login=login,
        db=db,
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User does not exist",
        )

    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=404,
            detail="Wrong password passed",
        )

    logger.info(msg="Authentication end")
    return user


def create_acces_token(
        data: dict,
        expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Access token creation
    :param data: user and password str
    :param expires_delta: expire token time int
    :return: token str
    """

    logger.info(msg="Token creation start")

    to_encode = data.copy()
    # Set an expiration time for the token to create
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    logger.info(msg=f"Created token : {encoded_jwt}")
    logger.info(msg="Token creation end")
    return encoded_jwt


@router.post(
    "",
    response_model=Token,
)
def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
) -> dict:
    """
    Api login with inquired access token
    :param form_data: user and password str
    :param db: database str
    :return: dict
    """

    logger.info(msg="login for access token function start ...")
    admin_default = {
        "login": config.get("api").get("user"),
        "password": config.get("api").get("password"),
        "admin": config.get("api").get("admin"),
    }
    create_user_admin_default(
        admin_default=admin_default,
        db=db,
    )

    user = authenticate_user(
        login=form_data.username,
        password=form_data.password,
        db=db,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    access_token = create_acces_token(
        data={"sub": user.login},
        expires_delta=access_token_expires,
    )
    logger.info(msg="login for access token function end")
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

def bdd_insert_data(db: Session):
    """
    Read and insert csv file in product table
    :param db: database str
    :return: None
    """
    logger.info(msg="Start insering the reference data to database...")
    data = load_csv_file(
        file_path=os.path.realpath("data/data.csv"),
    )

    data = data.unique()
    data = data.with_columns(
        pl.col(["activity_date"]).str.strptime(pl.Date, format = '%d/%m/%Y')
    )
    data.to_pandas().to_sql(DPredictORM.Products.__tablename__, con=engine.connect(), index=False, if_exists="replace")
    db.commit()
    logger.info(msg="End insering the reference data to database :-) ")
