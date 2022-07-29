import motor.motor_asyncio
import os

from pydantic import BaseModel, EmailStr, Field
from dotenv import load_dotenv
from bson import ObjectId
from typing import Optional


load_dotenv()

# Connect to MongoDB
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URL"))
db = client.blog_api


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectID")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Ali Eslah",
                "email": "alieslah@gmail.com",
                "password": "admin",
            }
        }


class UserResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)

    class Config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Ali Eslah",
                "email": "alieslah@gmail.com",
            }
        }


class Product(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    description: str = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {"title": "product title", "description": "product description"}
        }


class ProductResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    description: str = Field(...)
    author_name: str = Field(...)
    author_id: str = Field(...)
    created_at: str = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "product title",
                "description": "product description",
                "author_name": "name of the author",
                "author_id": "ID of the author",
                "created_at": "Date of product creation",
            }
        }


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
