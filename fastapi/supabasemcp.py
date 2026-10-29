from fastapi import FastAPI

from mcp.server.fastmcp import FastMCP

app = FastAPI()

@app.get('/')
def test():
    return {"message": "Hello, world"}

@app.get("/again")
def test2():
    return {"message": "Hello again fron test2"}


@app.get("/test3")
def test3(a: int, b: int):
    return {"message": f"Hello from test3 with a={a} and b={b}"}

@mcp.tool()
def read_my_drive():
    return {"message": "Reading my drive "}
