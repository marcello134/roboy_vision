from __future__ import print_function

import logging
import asyncio
import websockets
import json as json

# # from config import params_setup
# from lib import data_utils

async def findobject_service_callback():
    async with websockets.connect('ws://localhost:9090') as websocket:

        # advertise the service
        await websocket.send("{ \"op\": \"advertise_service\",\
                      \"type\": \"roboy_communication_cognition/FindObject\",\
                      \"service\": \"/roboy/cognition/vision/FindObject\"\
                    }")

        i = 1  # counter for the service request IDs

        # wait for the service request, generate the answer, and send it back
        while True:
            try:
                # pdb.set_trace()
                request = await websocket.recv()
                type = json.loads(request)["args"]["type"]

                srv_response = {}
                answer = {}
                # find object function must be implemented here
                answer["found"] = False
                answer["x"] = 0
                answer["y"] = 0
                answer["z"] = 0

                srv_response["values"] = answer
                srv_response["op"] = "service_response"
                srv_response["id"] = "service_request:/roboy/cognition/vision/FindObject:" + str(i)
                srv_response["result"] = True
                srv_response["service"] = "/roboy/cognition/vision/FindObject"
                i += 1

                await websocket.send(json.dumps(srv_response))

                # print ("Got here somehow" + str(srv_response))

            except Exception as e:
                logging.exception("Oopsie! Got an exception in FindObjectSrv")

logging.basicConfig(level=logging.INFO)
asyncio.get_event_loop().run_until_complete(findobject_service_callback())