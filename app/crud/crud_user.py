from sqlalchemy.orm import Session 
from passlib.hash import sha256_crypt
from fastapi.encoders import jsonable_encoder 
from fastapi import HTTPException


from app.database import DPredictORM
from app.models import model_pydantic
from app.routers.login import logger

def get_password_hash(password):
    """
    Get hash password
    :param password: password
    :return: password hash
    """
    logger.info("Get password hash")
    return sha256_crypt.using(salt="a" * 6).hash(password)


def get_user(
        db: Session,
        user_id: int,
) -> dict:
    """
    Get user according to a given user id
    :param db: database str
    :param user_id: user id
    :return user information
    """
    logger.info("Get user function")
    result = db.query(
        DPredictORM.ApiUser
    ).filter(
        DPredictORM.ApiUser.id_user == user_id
    ).first()

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"No user id {user_id} found",
        )

    result.registered_on = str(result.registered_on).split('.')[0]
    return {
        "admin": result.admin,
        "id_user": result.id_user,
        "login": result.login,
        "registered_on": result.registered_on,
    }


def get_user_by_login(
        db: Session,
        login: str,
):
    """
    Get user information by login
    :param db: database str
    :param login: login email
    :return: user information
    """
    logger.info("Get user by login function")
    return db.query(
        DPredictORM.ApiUser
    ).filter(
        DPredictORM.ApiUser.login == login
    ).first()


# TODO : Why this function ? It seems to be duplicated
def get_all_users(db: Session):
    """
    Get all existent API users
    :param db: database str
    :return all user in database
    """
    logger.info("Get all users function")
    result = db.query(DPredictORM.ApiUser).all()
    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"No users found",
        )

    for i in range(len(result)):
        result[i].registered_on = str(result[i].registered_on).split('.')[0]
    return result


def get_users(
        db: Session,
        skip: int = 0,
        limit: int = 100,
) -> list:
    """
    Get all existent API users
    :param db: database str
    :param skip: min user asked
    :param limit: max user asked
    :return all user in limite asked
    """
    logger.info("Get all users in limite asked function")
    all_result = []
    result = db.query(
        DPredictORM.ApiUser
    ).offset(skip).limit(limit).all()

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="No users found",
        )

    for i in range(len(result)):
        all_result.append(
            {
                "admin": result[i].admin,
                "id_user": result[i].id_user,
                "login": result[i].login,
                "registered_on": str(result[i].registered_on).split('.')[0]
            }
        )

    return all_result


def create_user(
        db: Session,
        user: model_pydantic.ApiUserCreate,
) -> dict:
    """
    Create API user
    :param db: database str
    :param user: user id
    :return user created
    """
    logger.info("Create user function")
    hashed_password = get_password_hash(user.password)

    db_user = DPredictORM.ApiUser(
        login=user.login,
        password=hashed_password,
        admin=user.admin,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_user.registered_on = str(db_user.registered_on).split('.')[0]
    return {
        "admin": db_user.admin,
        "id_user": db_user.id_user,
        "login": db_user.login,
        "registered_on": db_user.registered_on,
    }


def delete_user_by_id(
        db: Session,
        user_id: int,
) -> bool:
    """
    User deletion according to a given id
    :param db: database str
    :param user_id: user id
    :return bool when user is deleted
    """
    logger.info("Delete user function")
    id_in_base = get_user(
        db,
        user_id,
    )
    if id_in_base is None:
        raise HTTPException(
            status_code=404,
            detail="User id not found",
        )
    db.query(
        DPredictORM.ApiUser
    ).filter(
        DPredictORM.ApiUser.id_user == user_id
    ).delete()

    db.commit()

    return True


def update_user_by_id(
        db: Session,
        user_id: int,
        user: model_pydantic.ApiUserActivate,
) -> dict:
    """
    Update user according to a given id
    :param db: database str
    :param user_id: user id
    :param user: schema user model
    :return user update
    """
    logger.info("Update user function")
    db_user_by_id = get_user(
        db,
        user_id,
    )
    db_user_by_id = jsonable_encoder(db_user_by_id)
    if db_user_by_id is None:
        raise HTTPException(
            status_code=404,
            detail=f"User id : {user_id} not found",
        )

    db_user_by_id.update(user.dict())
    db.query(
        DPredictORM.ApiUser
    ).filter(
        DPredictORM.ApiUser.id_user == user_id
    ).update(
        {
            "login": db_user_by_id["login"],
            "admin": db_user_by_id["admin"],
        }
    )
    db.commit()

    return {
        "admin": db_user_by_id["admin"],
        "id_user": db_user_by_id["id_user"],
        "login": db_user_by_id["login"],
        "registered_on": str(db_user_by_id["registered_on"]).split('.')[0],
    }