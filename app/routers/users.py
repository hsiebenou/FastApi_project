from typing import List

from fastapi import Depends, HTTPException, Path, Query, APIRouter
from sqlalchemy.orm import Session

from app.crud import crud_user
from app.models import model_pydantic
from app.database.database_init import get_db
from app.dependencies.auth import check_admin_user
from app.routers.login import logger

router = APIRouter(
    prefix="/user",
    tags=["Users"],
    dependencies=[Depends(check_admin_user)],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/{user_id}",
    response_model=model_pydantic.ApiUserReturn,
)
def read_user(
        user_id: int = Path(
            ...,
            description="User identification",
            ge=1,
            le=1000,
        ),
        db: Session = Depends(get_db),
):
    logger.info(f"User reading endpoint: {user_id}")
    db_user = crud_user.get_user(
        db,
        user_id=user_id,
    )

    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return db_user


@router.post(
    "",
    response_model=model_pydantic.ApiUserReturn,
)
def create_user(
        user: model_pydantic.ApiUserCreate,
        db: Session = Depends(get_db),
):
    logger.info(msg="User creation endpoint")
    db_user = crud_user.get_user_by_login(
        db,
        login=user.login,
    )

    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Login already registered",
        )
    logger.info(f"User to create : {user}")
    return crud_user.create_user(
        db=db,
        user=user,
    )


@router.get(
    "",
    response_model=List[model_pydantic.ApiUserReturn],
)
def read_users(
        skip: int = Query(
            0,
            name="minimum value",
            description="Minimum value to read"
        ), limit: int = Query(
            100,
            name="limit value",
            description="Maximum value to read",
        ),
        db: Session = Depends(get_db),
):
    logger.info(msg="Users reading endpoint")
    return crud_user.get_users(
        db,
        skip=skip,
        limit=limit,
    )



@router.put(
    "/{user_id}",
    response_model=model_pydantic.ApiUserReturn,
)
def update_by_user(
        *,
        user_id: int = Path(
            ...,
            description="User identification",
            ge=1,
            le=1000,
        ),
        user: model_pydantic.ApiUserActivate,
        db: Session = Depends(get_db),
):
    logger.info(msg=f"User update endpoint: {user_id}")
    return crud_user.update_user_by_id(
        db=db,
        user=user,
        user_id=user_id,
    )


@router.delete(
    "/{user_id}",
    response_model=model_pydantic.DeletePUSU,
)
def delete_user_by_id(
        *,
        user_id: int = Path(
            ...,
            description="User identification",
            ge=1,
            le=1000,
        ),
        db: Session = Depends(get_db),
):
    logger.info(msg=f"User deletion endpoint: {user_id}")
    result = crud_user.delete_user_by_id(
        db=db,
        user_id=user_id,
    )
    return {"response": result}
