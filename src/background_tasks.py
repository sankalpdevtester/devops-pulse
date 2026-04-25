```python
from fastapi import BackgroundTasks
from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List
import sqlite3
import requests
import time
from src.models.endpoints import Endpoint
from src.models.database import get_db
from src.utils.helpers import send_notification

app = FastAPI()

# Define the OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Define the endpoint model
class EndpointModel(BaseModel):
    id: int
    url: str
    method: str
    headers: dict
    data: dict

# Define the background task function
def check_endpoint(endpoint_id: int, db: sqlite3.Connection):
    # Get the endpoint from the database
    endpoint = Endpoint.get(db, endpoint_id)
    
    if endpoint is None:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    
    # Send the request
    try:
        response = requests.request(endpoint.method, endpoint.url, headers=endpoint.headers, data=endpoint.data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Save the result to the database
        Endpoint.update(db, endpoint_id, {"status": "failed", "message": str(e)})
        send_notification(endpoint_id, "failed", str(e))
        return
    
    # Save the result to the database
    Endpoint.update(db, endpoint_id, {"status": "success", "message": "Endpoint is healthy"})
    send_notification(endpoint_id, "success", "Endpoint is healthy")

# Define the background task route
@app.post("/endpoints/{endpoint_id}/check")
async def check_endpoint_route(endpoint_id: int, background_tasks: BackgroundTasks, db: sqlite3.Connection = Depends(get_db)):
    background_tasks.add_task(check_endpoint, endpoint_id, db)
    return {"message": "Endpoint check started"}

# Define the scheduled task function
def schedule_endpoint_checks(db: sqlite3.Connection):
    # Get all endpoints from the database
    endpoints = Endpoint.get_all(db)
    
    for endpoint in endpoints:
        # Check if the endpoint needs to be checked
        if endpoint.next_check <= int(time.time()):
            # Update the next check time
            Endpoint.update(db, endpoint.id, {"next_check": int(time.time()) + 60})
            
            # Start the background task
            check_endpoint(endpoint.id, db)

# Define the scheduled task route
@app.get("/endpoints/check")
async def schedule_endpoint_checks_route(db: sqlite3.Connection = Depends(get_db)):
    schedule_endpoint_checks(db)
    return {"message": "Endpoint checks scheduled"}

# Define the endpoint results route
@app.get("/endpoints/{endpoint_id}/results")
async def get_endpoint_results(endpoint_id: int, db: sqlite3.Connection = Depends(get_db)):
    # Get the endpoint from the database
    endpoint = Endpoint.get(db, endpoint_id)
    
    if endpoint is None:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    
    # Get the results from the database
    results = Endpoint.get_results(db, endpoint_id)
    
    return {"results": results}
```