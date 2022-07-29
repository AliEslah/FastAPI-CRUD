from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm


from api import oauth2
from api.schema import db, Token
from api.utils import verify_password

router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post(
    "",
    response_description="Login and Get Access Token",
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    user = await db["users"].find_one({"name": user_credentials.username})

    # FIXME:
    # if user then verify or in one line check both
    if user and verify_password(user_credentials.password, user["password"]):
        access_token = oauth2.create_access_token(payload={"id": user["_id"]})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found or Password is not be Correct",
        )
