from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Cookie, Response

app=FastAPI()

req_counters = {}
max_requests = 5

@app.get("/data")
def get_data(request:Request):
    client_ip = request.client.host
    req_counters[client_ip] = req_counters.get(client_ip, 0) + 1
    if req_counters[client_ip] > max_requests:
        raise HTTPException(status_code=429, detail="Too many requests")

    return {"message": "Data retrieved successfully"}