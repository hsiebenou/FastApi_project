from jose import (
    JWTError,
    jwt,
)
from sqlalchemy.orm import Session
from fastapi import (
    status,
    HTTPException,
    Depends,
)

from app.models.model_pydantic import (
    ApiUser,
    TokenData,
)
from app.database.database_init import get_db
from app.routers.login import (
    oauth2_scheme,
    get_user,
    SECRET_KEY,
    ALGORITHM,
    logger,
)



def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db),
) -> dict:
    """
    Get the current user based on the used token
    :param token: string token
    :param db: database
    :return: dictionary information
    """

    logger.info(msg="Start get_current_user function")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldn't validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            ALGORITHM,
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(
        login=token_data.username,
        db=db,
    )
    if user is None:
        raise credentials_exception
    logger.info(msg="get_current_user function end")
    return user


def check_admin_user(
        current_user: ApiUser = Depends(get_current_user),
) -> ApiUser:
    """
    Checks if the inquired user is admin
    :param current_user: Api User
    :return: the string user
    """

    logger.info(msg="get_current_active_user function start")
    logger.info(msg=f"Argument user : {current_user}")
    if not current_user.admin:
        raise HTTPException(
            status_code=400,
            detail="inactive user",
        )

    logger.info(msg="get_current_active_user function end")
    return current_user