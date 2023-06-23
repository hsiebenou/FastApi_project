from datetime import datetime

from pydantic import BaseModel, EmailStr, Field



# token
class Token(BaseModel):
    access_token: str = Field(description="Acces token with expired time : 15 minutes")
    token_type: str = Field(description="Token type")


class TokenData(BaseModel):
    username: str = Field(description="User name to sign in")


# API User
class ApiUserActivate(BaseModel):
    admin: bool = Field(
        default=False,
        description="Manage all end point or not",
    )


class ApiUserBase(ApiUserActivate):
    login: EmailStr = Field(description="Login (e-mail format) to sign in")


class ApiUserCreate(ApiUserBase):
    password: str = Field(description="Password to sign in")


class ApiUserReturn(ApiUserBase):
    id_user: int = Field(description="User identification")
    registered_on: str = Field(
        default=str(datetime.now()).split('.')[0],
        description="Registered user date",
    )


class ApiUser(ApiUserBase):
    id_user: int = Field(description="User identification")
    registered_on: datetime = Field(
        default=datetime.now(),
        description="Registred user date",
    )

    class Config:
        orm_mode = True


# delete table example
class DeletePUSU(BaseModel):
    response: bool

# product
class ProductReturn(BaseModel):
    activity_date: datetime = Field(description="activity date")
    product: int = Field(description="Product id")
    price: float = Field(description="Product price")

    class Config:
        orm_mode = True
