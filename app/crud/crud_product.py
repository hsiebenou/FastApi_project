import pandas as pd

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database import DPredictORM
from app.routers.login import logger


def get_products(
        db: Session,
        first_product: int = 0,
        last_product: int = 1000000,
) -> dict:
    """
    Get table filtered between first to last sku
    :param db: database str
    :param first_product: first product id
    :param last_product: last product id
    """
    logger.info("Start get_products function")
    product_tuple = ()
    for s in range(first_product, last_product+1):
        product_tuple = product_tuple + (s,)

    results = (
        db
        .query(DPredictORM.Products)
        .filter(DPredictORM.Products.product.in_(product_tuple))
        .all()
    )

    if results is None:
        raise HTTPException(
            status_code=404,
            detail="No product found",
        )
    logger.info("End get_products function")
    return results

def get_product(
        db: Session,
        product_id: int
) -> DPredictORM.Products:
    """
    Get table filtered by sku
    :param db: database str
    :param product_id: product id
    """
    logger.info("Start get_product function")
    result = (
        db
        .query(DPredictORM.Products)
        .filter(DPredictORM.Products.product == product_id)
        .all()
    )
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Score id {product_id} not found",
        )
    logger.info("Start get_product function")
    return result


def get_diff_price(
        list_of_sku: list,
        db: Session,
) -> dict:
    """
    Get all sku with difference price between de 2 last date par sku
    :param list_of_sku: list of product
    :param  db: database str
    :return  dict content difference price for all sku
    """
    logger.info("Start get_diff_price function")
    product_tuple = ()
    for s in list_of_sku:
        product_tuple = product_tuple + (s,)

    results = (
        db
        .query(DPredictORM.Products)
        .filter(DPredictORM.Products.product.in_(product_tuple))
        .all()
    )

    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"all list product not found",
        )
    data = pd.DataFrame([{"date": x.activity_date, "product": x.product, "price": x.price} for x in results])
    data.sort_values(by=["product", "date"], inplace=True, ignore_index=True)
    data['diff'] = data.groupby("product")['price'].diff().fillna(0)
    data = data.loc[data.groupby('product').date.idxmax(), ["product", "diff"]]

    logger.info("End get_diff_price function")
    return dict(zip(data['product'], data['diff']))