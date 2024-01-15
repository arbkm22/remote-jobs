from fastapi import FastAPI
from hashnode import hashnode

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello, world!"}


@app.get("/hashnode")
async def hashnode_api():
    jobs = hashnode()
    print(f'jobs in api: {jobs} | {type(jobs)}')
    # return jobs
    return {"message": "hashnode"}
    