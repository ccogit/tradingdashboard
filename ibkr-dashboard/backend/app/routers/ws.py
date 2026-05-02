from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.core.security import ClerkJWTVerifier
from app.services.ws_manager import ws_manager
from app.core.events import event_bus

router = APIRouter()
verifier = ClerkJWTVerifier()


@router.websocket("/ws/market")
async def ws_market(websocket: WebSocket, token: str = Query(...)):
    try:
        claims = await verifier.verify(token)
        user_id = claims["sub"]
    except Exception:
        await websocket.close(code=4001)
        return

    await websocket.accept()
    ws_manager.connect(user_id, websocket)
    tick_queue = event_bus.subscribe("tick")
    try:
        while True:
            msg = await websocket.receive_json()
            if msg.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
            elif msg.get("type") == "subscribe":
                from app.services.ib_market_data import subscribe_market_data
                from app.services.ib_gateway import ib_client
                for conid in msg.get("conids", []):
                    await subscribe_market_data(conid, ib_client)
                await websocket.send_json({"type": "subscribed", "conids": msg.get("conids", [])})
    except WebSocketDisconnect:
        pass
    finally:
        event_bus.unsubscribe("tick", tick_queue)
        ws_manager.disconnect(user_id, websocket)


@router.websocket("/ws/account")
async def ws_account(websocket: WebSocket, token: str = Query(...)):
    try:
        claims = await verifier.verify(token)
        user_id = claims["sub"]
    except Exception:
        await websocket.close(code=4001)
        return

    await websocket.accept()
    ws_manager.connect(user_id, websocket)
    account_queue = event_bus.subscribe("account_value")
    pnl_queue = event_bus.subscribe("pnl")
    try:
        while True:
            import asyncio
            await asyncio.sleep(20)
            await websocket.send_json({"type": "ping"})
    except WebSocketDisconnect:
        pass
    finally:
        event_bus.unsubscribe("account_value", account_queue)
        event_bus.unsubscribe("pnl", pnl_queue)
        ws_manager.disconnect(user_id, websocket)


@router.websocket("/ws/orders")
async def ws_orders(websocket: WebSocket, token: str = Query(...)):
    try:
        claims = await verifier.verify(token)
        user_id = claims["sub"]
    except Exception:
        await websocket.close(code=4001)
        return

    await websocket.accept()
    ws_manager.connect(user_id, websocket)
    order_queue = event_bus.subscribe("order_status")
    try:
        while True:
            import asyncio
            await asyncio.sleep(20)
    except WebSocketDisconnect:
        pass
    finally:
        event_bus.unsubscribe("order_status", order_queue)
        ws_manager.disconnect(user_id, websocket)
