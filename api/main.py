from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import products, users, auth


app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def get():
    return {"Hello": "World!"}
