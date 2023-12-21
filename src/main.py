from fastapi import FastAPI


app = FastAPI(docs_url="/")


@app.get("/hello/")
async def say_hello_world():
    return {"message": "Hello world"}
