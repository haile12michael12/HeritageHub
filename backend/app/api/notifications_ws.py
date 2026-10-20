from typing import Dict, List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import db_session
from app.models.notification import Notification
from app.schemas.response import ApiResponse

router = APIRouter(prefix="/notifications", tags=["Notifications"])

# In-memory connection manager (for demo; use Redis pubsub in prod)
class ConnectionManager:
    def __init__(self):
        self.active: Dict[str, List[WebSocket]] = {}

    async def connect(self, ws: WebSocket, user_id: str):
        await ws.accept()
        self.active.setdefault(user_id, []).append(ws)

    def disconnect(self, ws: WebSocket, user_id: str):
        if user_id in self.active and ws in self.active[user_id]:
            self.active[user_id].remove(ws)

    async def send_to_user(self, user_id: str, message: dict):
        for ws in self.active.get(user_id, []):
            try:
                await ws.send_json(message)
            except:
                pass

    async def broadcast(self, message: dict):
        for conns in self.active.values():
            for ws in conns:
                try:
                    await ws.send_json(message)
                except:
                    pass

manager = ConnectionManager()

@router.get("", status_code=status.HTTP_200_OK)
async def list_notifications(email: str | None = None, db: AsyncSession = Depends(db_session)):
    stmt = select(Notification).order_by(Notification.created_at.desc()).limit(20)
    if email:
        stmt = stmt.where(Notification.recipient_email == email)
    result = await db.scalars(stmt)
    return ApiResponse(status=200, message="Notifications", data=list(result.all()))

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo with order update simulation
            await websocket.send_json({"type": "ack", "message": f"Received: {data}", "user_id": user_id})
            # Broadcast live order status demo
            await manager.broadcast({"type": "live_update", "message": "New inventory update", "product_id": 1})
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)

@router.post("/send/{user_id}", status_code=status.HTTP_200_OK)
async def send_test_notification(user_id: str, message: str = "Hello from HeritageHub!"):
    await manager.send_to_user(user_id, {"type": "notification", "message": message})
    await manager.broadcast({"type": "notification", "message": message, "target": user_id})
    return ApiResponse(status=200, message="Notification sent", data={"user_id": user_id, "message": message})
