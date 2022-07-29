import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder

from api.utils import get_password_hash
from api.schema import User, UserResponse, db
from api import oauth2

router = APIRouter(prefix="/users", tags=["User Routes"])


@router.post(
    "/registration",
    response_description="Register User",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def registration(user_info: User):
    user_info = jsonable_encoder(user_info)

    # Check User Exist
    username_found = await db["users"].find_one({"name": user_info["name"]})

    if username_found:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username is Already Exist"
        )

    # Check User Exist
    email_found = await db["users"].find_one({"email": user_info["email"]})
    if email_found:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email is Already Exist"
        )

    # Hash Password
    user_info["password"] = get_password_hash(user_info["password"])

    # Create API key
    user_info["apiKey"] = secrets.token_hex(30)

    # Create User
    new_user = await db["users"].insert_one(user_info)
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})

    # FIXME: SEND EMAIL
    # from api.send_email import send_registration_mail
    # await send_registration_mail(
    #     subject="Your Register is complete",
    #     email_to=user_info["email"],
    #     body={
    #         "title": "Registration Successful",
    #         "name": user_info["name"],
    #     },
    # )

    return created_user


@router.get(
    "/me",
    response_description="Get user details",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def detail(current_user=Depends(oauth2.get_current_user)):
    user = await db["users"].find_one({"_id": current_user["_id"]})
    return user
