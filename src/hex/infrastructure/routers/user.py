from fastapi import APIRouter


router = APIRouter(prefix="")


@router.get("/sign-up/")
async def say_hello_world():
    return {"message": "Hello world"}
