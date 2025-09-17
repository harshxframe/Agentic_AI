from fastapi import FastAPI, Query
from clients.rq_client import queue
from queues.worker import processQuery


app = FastAPI()


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/chat")
def userQuery(
        query: str = Query(..., description="Query string"),
):
    jobID = queue.enqueue(processQuery, query)
    return {"status": "Queued", "jobID": jobID.id}



@app.post("/getQueue")
def get_result(jobId: str = Query(..., description="Job ID")):
    job = queue.fetch_job(job_id=jobId)
    result = job.return_value()
    return {"result": result}
