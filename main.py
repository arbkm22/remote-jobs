import json
from fastapi import FastAPI
from hashnode import hashnode

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello, world!"}

@app.get("/hashnode", response_model=dict)
async def hashnode_api():
    jobs = hashnode()
    jobs = json.dumps(jobs, indent=None)
    return json.loads(jobs)