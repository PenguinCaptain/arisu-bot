import asyncio
import websockets
import requests
import json
import _starter.server as server

async def server(websocket):

    response = await websocket.recv()
    
    response = json.loads(response)

    try:
        type = response["post_type"]
    except:
        return 0

    if type == "message":
        try:
            group_id = response["group_id"] # 获取group_id (群号)
        except:
            group_id = None # private chat 情况
        
        user_id = response["user_id"] # 获取user_id (qq号)
        message = response["message"]
        # raw_message = response["raw_message"]

        if message[0]["type"] == "text": # 目前只打算handle text
            raw_message = message[0]["data"]["text"]

            try:
                print(raw_message)
                sender = response["raw_message"]

                reply = server.handle(group_id, user_id, raw_message, sender)

                reply_json = {
                    "action": "send_group_msg",
                    "params": {
                        "group_id": group_id,
                        "message": reply
                    }
                }

                if reply != None:
                    await requests.post("ws://127.0.0.1:8081/api", json.dumps(reply_json))
                    await print("回复" + reply)

                

            except:
                pass

            

start_server = websockets.serve(server, 'localhost', 8081)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()










