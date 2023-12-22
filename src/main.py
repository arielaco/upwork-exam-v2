from fastapi import FastAPI, APIRouter


from .hex.infrastructure.routers.rest import router as rest_router


router = APIRouter(prefix="/api")
router.include_router(rest_router)


app = FastAPI(docs_url="/")
app.include_router(router)
