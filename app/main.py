from app.routers import (
login,
users,
product,
)
from app.routers.login import (
    API_SERVICE_NAME,
    API_VERSION,
    API_VERSION_SERVER,
    logger,
)
from app.database.database_init import (
    Base,
    engine,
)

from fastapi import FastAPI
Base.metadata.create_all(bind=engine)


# Headers description
description = """
This project help you know the difference between the last tow final prices per product. 🚀

## Users
Manages users:
* **Create users** : create a user in database
* **Read users**   : read a user information in database
* **Delete users** : delete a user information in database
* **Update users** : update a user information in database

## Products
Manages Products:
* **Read on product**  : read information product
* **Read all product** : read information product between two to id
* **get prices evolution between last two dates** : get price evolution between last two date

"""
# Description headers on API endpoints
tags_metadata = [
    {
        "name": "Home page",
        "description": "Welcome to this test application",
        "externalDocs": {
                    "description": "link to our webside",
                    "url": "https://www.pricinghub.net/en/",
                },
    },
    {
        "name": "Login",
        "description": "Get token after login",
    },
    {
        "name": "Users",
        "description": "Manage all users",
    },
    {
        "name": "Products",
        "description": "Manage all Products",
    },
]

logger.info(msg=f"API_SERVICE_NAME : {API_SERVICE_NAME}")
logger.info(msg=f"API_VERSION_SERVER : {API_VERSION_SERVER}")
logger.info(msg=f"API_VERSION : {API_VERSION}")



# Application initialisation
app = FastAPI(
     title=API_SERVICE_NAME,
     description=description,
     version=str(API_VERSION_SERVER),
     terms_of_service="http://127.0.0.1:8000/redoc",
     contact={
         "name": "RD-DS Teams",
         "url": "http://127.0.0.1:8000/docs",
         "email": "contact@pricinghub.net",
     },
     license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
     },
     openapi_url=f"/api/{API_VERSION}/openapi.json",
     openapi_tags=tags_metadata,
)


app.include_router(login.router)
app.include_router(users.router)
app.include_router(product.router)


@app.get(
    "/",
    tags=["Home page"],
)
def home():
    logger.info(msg="Homepage endpoint")
    return "Welcome to my new application application :-)"
