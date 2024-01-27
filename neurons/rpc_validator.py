# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# (developer): Formless Technologies
# Copyright © 2023 Formless Technologies

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.


import time

# Bittensor
import bittensor as bt
from neurons.validator import Validator
import asyncio
import websockets
import json

async def handle_rpc(websocket, path):
    async for message in websocket:
        json_rpc_request = json.loads(message)
        response = validator.do_subtensor_miner_rpc(json_rpc_request)
        await websocket.send(json.dumps(response))

start_server = websockets.serve(handle_rpc, "localhost", 8765)

# The main function parses the configuration and runs the rpc validator.
if __name__ == "__main__":
    with Validator() as validator:
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
        while True:
            bt.logging.info("Validator running...", time.time())
            time.sleep(5)