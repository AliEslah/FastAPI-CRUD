from typing import List
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from api.schema import Product, ProductResponse, db
from api import oauth2

router = APIRouter(prefix="/product", tags=["Product"])


@router.get(
    "/",
    response_description="Get Products",
    response_model=List[ProductResponse],
    status_code=status.HTTP_200_OK,
)
async def get_products(limit: int = 10, orderby: str = "created_at"):
    try:
        products = (
            await db["products"]
            .find({"$query": {}, "$orderby": {orderby: -1}})
            .to_list(limit)
        )
        return products
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post(
    "/",
    response_description="Create Product",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
async def read_item(product: Product, current_user=Depends(oauth2.get_current_user)):
    try:
        product = jsonable_encoder(product)
        product["author_name"] = current_user["name"]
        product["author_id"] = current_user["_id"]
        product["created_at"] = str(datetime.utcnow())

        # create products collection
        new_product = await db["products"].insert_one(product)

        # get created post content
        created_product = await db["products"].find_one(
            {"_id": new_product.inserted_id}
        )

        return created_product

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get(
    "/{id}",
    response_description="Get Product Detail",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
)
async def get_product_detail(id: str):
    try:
        product = await db["products"].find_one({"_id": id})
        return product
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.put(
    "/{id}",
    response_description="Update a Product",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
)
async def update_product(
    id: str, product_content: Product, current_user=Depends(oauth2.get_current_user)
):

    if product := await db["products"].find_one({"_id": id}):
        print(product)
        # check if the owner is the currently logged in user
        if product["author_id"] == current_user["_id"]:
            print("owner")
            try:
                product_content = {
                    k: v for k, v in product_content.dict().items() if v is not None
                }

                if len(product_content) >= 1:
                    update_result = await db["products"].update_one(
                        {"_id": id}, {"$set": product_content}
                    )

                    if update_result.modified_count == 1:
                        if (
                            updated_product := await db["products"].find_one(
                                {"_id": id}
                            )
                        ) is not None:
                            return updated_product

                if (
                    exist_product := await db["products"].find_one({"_id": id})
                ) is not None:
                    return exist_product

            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Internal server error",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"You are not the owner of this Product",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Product #{id} not found"
        )


@router.delete(
    "/{id}",
    response_description="Delete Product",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product(id: str, current_user=Depends(oauth2.get_current_user)):

    if product := await db["products"].find_one({"_id": id}):

        # check if the owner is the currently logged in user
        if product["author_id"] == current_user["_id"]:
            try:
                delete_result = await db["products"].delete_one({"_id": id})
                if not delete_result.deleted_count:
                    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Internal server error",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"You are not the owner of this Product",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Product #{id} not found"
        )
