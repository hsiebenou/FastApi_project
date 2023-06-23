from typing import List

from fastapi import Depends, HTTPException, Path, Query, APIRouter
from sqlalchemy.orm import Session

from app.crud import crud_product
from app.models import model_pydantic
from app.database.database_init import get_db
from app.dependencies.auth import check_admin_user
from app.routers.login import logger

router = APIRouter(
    prefix="/product",
    tags=["Products"],
    dependencies=[Depends(check_admin_user)],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/{product_id}",
    response_model=List[model_pydantic.ProductReturn],
)
def read_one_product(
        product_id: int = Path(
            ...,
            description="User identification",
            ge=1,
            le=1000000,
        ),
        db: Session = Depends(get_db),
):
    logger.info(f"Product reading endpoint: {product_id}")
    db_product = crud_product.get_product(
        db,
        product_id=product_id,
    )

    if db_product is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return db_product

@router.get(
    "",
    response_model=List[model_pydantic.ProductReturn],
)
def read_all_products(
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
    logger.info(f"Product reading endpoint between {skip} and {limit}")
    return crud_product.get_products(
        db,
        first_product=skip,
        last_product=limit,
    )


@router.post("", response_model=dict)
async def get_prices_evolution_between_last_two_dates(list_of_sku: List[int], db: Session = Depends(get_db)):
    logger.info(f"Reading price endpoint")
    logger.info(f"The SKU number are : {list_of_sku}")
    result = crud_product.get_diff_price(
        list_of_sku,
        db,
    )
    return result