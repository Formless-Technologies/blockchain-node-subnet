# The MIT License (MIT)
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
import bittensor as bt
from neurons.validator import Validator
import asyncio
import websockets
import json

validator_instance = None

async def handle_rpc(websocket, path):
    global validator_instance
    try:
        async for message in websocket:
            json_rpc_request = json.loads(message)
            print(f"Received request: {json_rpc_request}")
            
            try:

                synapse_response = validator_instance.organic_miner_subtensor_rpc(json_rpc_request)
                # Before relaying, match IDs
                synapse_response['id'] = json_rpc_request['id']
                await websocket.send(json.dumps(synapse_response))

            except Exception as e:
                print(f"Error occurred: {e}")
                await asyncio.sleep(0.05)


    except websockets.ConnectionClosed:
        print('Connection Closed')


def create_validator():
    global validator_instance
    validator_instance = Validator()
    validator_instance.run_in_background_thread()


def cleanup():
    global validator_instance
    validator_instance.stop_run_thread()
    validator_instance = None


async def main():
    create_validator()
    async with websockets.serve(handle_rpc, "localhost", 8765):
        print("Server started at ws://localhost:8765")
        try:
            await asyncio.Future()  # run forever
        finally:
            cleanup()


# Main
if __name__ == "__main__":
    asyncio.run(main())