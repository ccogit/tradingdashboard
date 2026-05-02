from fastapi import WebSocket
from collections import defaultdict


class ConnectionManager:
    def __init__(self):
        self._connections: dict[str, set[WebSocket]] = defaultdict(set)

    def connect(self, user_id: str, ws: WebSocket) -> None:
        self._connections[user_id].add(ws)

    def disconnect(self, user_id: str, ws: WebSocket) -> None:
        self._connections[user_id].discard(ws)

    async def broadcast_to_user(self, user_id: str, event: dict) -> None:
        dead = set()
        for ws in self._connections.get(user_id, set()):
            try:
                await ws.send_json(event)
            except Exception:
                dead.add(ws)
        for ws in dead:
            self._connections[user_id].discard(ws)


ws_manager = ConnectionManager()
