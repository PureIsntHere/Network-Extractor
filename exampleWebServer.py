from fastapi import FastAPI,Request
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/")
async def post_root(request: Request):
    data = await request.json()
    print(data)
    return ("OK")

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=80)