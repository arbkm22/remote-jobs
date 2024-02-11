import json
from fastapi import FastAPI
from hashnode import hashnode
from openplay import openplay
from instagram import instagram

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello, world!"}

@app.get("/hashnode", response_model=dict)
async def hashnode_api():
    jobs = hashnode()
    jobs = json.dumps(jobs, indent=None)
    return json.loads(jobs)

@app.get("/openplay", response_model=dict)
async def openplay_api():
    openplay_jobs = openplay()
    jobs = json.dumps(openplay_jobs, indent=None)
    return json.loads(jobs)

@app.get("/instagram", response_model=dict)
async def instagram_api():
    ig_jobs = instagram()
    jobs = json.dumps(ig_jobs, indent=None)
    return json.loads(jobs)