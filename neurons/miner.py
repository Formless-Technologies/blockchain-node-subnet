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
import typing
import bittensor as bt

# Bittensor Miner Template:
import template

# import base miner class which takes care of most of the boilerplate
from template.base.miner import BaseMinerNeuron


class Miner(BaseMinerNeuron):

    def __init__(self, config=None):
        super(Miner, self).__init__(config=config)


    # Receives an rpc request from a validator and processes it on local subtensor node.
    async def validator_rpc_request(
        self, synapse: template.protocol.MinerSubtensorRPCSynapse
    ) -> template.protocol.MinerSubtensorRPCSynapse:
        query = synapse.rpc_query

        if(query['method'] == 'author_submitAndWatchExtrinsic'):
            print(f"Received watch extrinsic")
            def result_handler(message, update_nr, subscription_id):
                # Check if extrinsic is included and finalized
                if 'params' in message and type(message['params']['result']) is dict:

                    # Convert result enum to lower for backwards compatibility
                    message_result = {k.lower(): v for k, v in message['params']['result'].items()}

                    if 'inblock' in message_result:
                        self.subtensor.substrate.rpc_request('author_unwatchExtrinsic', [subscription_id])
                        return message
            
            synapse.response = self.subtensor.substrate.rpc_request(method=query['method'], params=query['params'], result_handler=result_handler)
            print(f"RETURNING RESULT: {synapse.response}")
            return synapse

        else:
            synapse.response = self.subtensor.substrate.rpc_request(method=query['method'], params=query['params'])
            return synapse
        

    # Determines whether a given Synapse request should be blacklisted
    async def validator_rpc_blacklist(
        self, synapse: template.protocol.MinerSubtensorRPCSynapse
    ) -> typing.Tuple[bool, str]:

        if synapse.dendrite.hotkey not in self.metagraph.hotkeys:
            # Ignore requests from unrecognized entities.
            bt.logging.trace(
                f"Blacklisting unrecognized hotkey {synapse.dendrite.hotkey}"
            )
            return True, "Unrecognized hotkey"

        bt.logging.trace(
            f"Not Blacklisting recognized hotkey {synapse.dendrite.hotkey}"
        )
        return False, "Hotkey recognized!"
    


# This is the main function, which runs the miner.
if __name__ == "__main__":
    with Miner() as miner:
        while True:
            bt.logging.info("Miner running...", time.time())
            time.sleep(5)
