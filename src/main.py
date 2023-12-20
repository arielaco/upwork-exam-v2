from fastapi import FastAPI


app = FastAPI(docs_url="/")


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
