from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import uuid
import os
import asyncio
from recondorker.core import ReconDorker

app = FastAPI(title="ReconDorker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory scan storage (for demo purposes)
scans = {}

class ScanRequest(BaseModel):
    target: str
    pages: Optional[int] = 1
    dorks: Optional[List[str]] = None

class ScanStatus(BaseModel):
    id: str
    target: str
    status: str
    results_count: int
    results: Optional[List[dict]] = None

async def run_scan_task(scan_id: str, target: str, dorks: List[str], pages: int):
    recon = ReconDorker(target)
    scans[scan_id]["status"] = "running"
    try:
        results = await recon.run_scan(dorks, pages=pages)
        scans[scan_id]["status"] = "completed"
        scans[scan_id]["results"] = results
        scans[scan_id]["results_count"] = len(results)
    except Exception as e:
        scans[scan_id]["status"] = f"failed: {str(e)}"
    finally:
        await recon.close()

@app.post("/api/scan", response_model=dict)
async def start_scan(request: ScanRequest, background_tasks: BackgroundTasks):
    scan_id = str(uuid.uuid4())
    dorks = request.dorks or [
        "intitle:index.of", "ext:php", "ext:log", "inurl:admin"
    ]
    scans[scan_id] = {
        "id": scan_id,
        "target": request.target,
        "status": "pending",
        "results_count": 0,
        "results": []
    }
    background_tasks.add_task(run_scan_task, scan_id, request.target, dorks, request.pages)
    return {"scan_id": scan_id}

@app.get("/api/scan/{scan_id}", response_model=ScanStatus)
async def get_scan_status(scan_id: str):
    if scan_id not in scans:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scans[scan_id]

@app.get("/api/scans", response_model=List[ScanStatus])
async def list_scans():
    return list(scans.values())

# Serve static files
# app.mount("/", StaticFiles(directory="webui/static", html=True), name="static")
@app.get("/")
async def read_index():
    return FileResponse('webui/static/index.html')
