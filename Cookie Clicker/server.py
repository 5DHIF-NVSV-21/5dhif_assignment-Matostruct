import asyncio
from asyncio.windows_events import NULL
import json
import logging
import websockets
import threading
import time
from asyncio.tasks import wait_for

logging.basicConfig()

STATE = {"value": 0, "autoCookies": 0, "thread": False}

UPGRADES = {"omi": 0, "omiPrice": 20, "wolf": 0, "wolfPrice": 30}

USERS = set()


def state_event():
    return json.dumps({"type": "state", **STATE})


def upgrades_event():
    return json.dumps({"type": "upgrades", **UPGRADES})


def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})


async def counter(websocket, path):
    try:
        # Register user
        USERS.add(websocket)
        websockets.broadcast(USERS, users_event())
        # Send current state to user
        await websocket.send(state_event())
        await websocket.send(upgrades_event())
        # Manage state changes
        async for message in websocket:
            data = json.loads(message)
            if data["action"] == "click":
                onClick()
            if data["action"] == "buyOmi" and STATE["value"] >= UPGRADES["omiPrice"]:
                buyOmi()
            if data["action"] == "buyWolf" and STATE["value"] >= UPGRADES["wolfPrice"]:
                buyWolf()
    except Exception:
        pass
    finally:
        # Unregister user
        USERS.remove(websocket)
        websockets.broadcast(USERS, users_event())


def broadcast():
    STATE["autoCookies"] = round((UPGRADES["wolf"] * 3.14) + (UPGRADES["omi"] * 1.02), 2)
    websockets.broadcast(USERS, state_event())
    websockets.broadcast(USERS, upgrades_event())


def onClick():
    STATE["value"] += 1
    STATE["autoCookies"] = UPGRADES["wolf"] + UPGRADES["omi"]
    if STATE["thread"] == False:
        thread = threading.Thread(target=autoClick, daemon=True)
        thread.start()
        STATE["thread"] = True
    broadcast()


def buyOmi():
    UPGRADES["omi"] += 1
    STATE["value"] = STATE["value"] - UPGRADES["omiPrice"]
    UPGRADES["omiPrice"] = round(UPGRADES["omiPrice"] * 1.3)
    broadcast()


def buyWolf():
    UPGRADES["wolf"] += 1
    STATE["value"] = STATE["value"] - UPGRADES["wolfPrice"]
    UPGRADES["wolfPrice"] = round(UPGRADES["wolfPrice"] * 2.6)
    broadcast()


def autoClick():
    while(True):
        STATE["value"] += round(STATE["autoCookies"], 2)
        STATE["value"] = round(STATE["value"])
        broadcast()
        time.sleep(1)

async def main():
    async with websockets.serve(counter, "localhost", 6789):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass