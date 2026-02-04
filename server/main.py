from fastapi import FastAPI, UploadFile, File, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List, Dict
import os
import shutil
import json

app = FastAPI(title="Freelancer Hub Sync Server")

# --- Storage Setup ---
UPLOAD_DIR = "server_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- Connection Manager ---
class ConnectionManager:
    def __init__(self):
        # Map project_id -> List of WebSockets
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, project_id: int):
        await websocket.accept()
        if project_id not in self.active_connections:
            self.active_connections[project_id] = []
        self.active_connections[project_id].append(websocket)

    def disconnect(self, websocket: WebSocket, project_id: int):
        if project_id in self.active_connections:
            if websocket in self.active_connections[project_id]:
                self.active_connections[project_id].remove(websocket)

    async def broadcast(self, message: dict, project_id: int):
        if project_id in self.active_connections:
            for connection in self.active_connections[project_id]:
                try:
                    await connection.send_text(json.dumps(message))
                except:
                    pass

manager = ConnectionManager()

# --- Models ---
class ActivityLog(BaseModel):
    project_id: int
    window_title: str
    start_time: str
    end_time: str

# --- Endpoints ---
@app.get("/")
def read_root():
    return {"status": "running", "message": "Freelancer Hub Sync Server is Active"}

@app.post("/upload/screenshot")
async def upload_screenshot(project_id: int, file: UploadFile = File(...)):
    try:
        # Create project specific folder
        project_dir = os.path.join(UPLOAD_DIR, str(project_id))
        os.makedirs(project_dir, exist_ok=True)
        
        file_path = os.path.join(project_dir, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Notify Clients
        await manager.broadcast({
            "type": "new_screenshot",
            "url": file_path, # In real app, this would be a URL
            "timestamp": "Just now"
        }, project_id)
            
        return {"status": "success", "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sync/activity")
async def sync_activity(logs: List[ActivityLog]):
    # In a real app, save to Server DB
    print(f"Received {len(logs)} activity logs")
    
    # Notify Clients
    if logs:
        pid = logs[0].project_id
        await manager.broadcast({
            "type": "new_activity",
            "data": [log.model_dump() for log in logs]
        }, pid)

    return {"status": "synced", "count": len(logs)}

# --- WebSocket for Live Dashboard ---
@app.websocket("/ws/project/{project_id}")
async def websocket_endpoint(websocket: WebSocket, project_id: int):
    await manager.connect(websocket, project_id)
    try:
        while True:
            # Keep connection alive and listen for client messages if any
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, project_id)
    except Exception:
        manager.disconnect(websocket, project_id)
