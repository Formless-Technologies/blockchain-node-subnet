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

# Bittensor Validator Template:
from template.protocol import SubtensorQueryBlockHashSynapse, DoMinerSubtensorRPCSynapse
from template.validator.reward import get_rewards
from template.utils.uids import get_random_uids
import random

# import base validator class which takes care of most of the boilerplate
from template.base.validator import BaseValidatorNeuron

class Validator(BaseValidatorNeuron):

    def __init__(self, config=None):
        super(Validator, self).__init__(config=config)

        bt.logging.info("load_state()")
        self.load_state()


    async def challenge_miner_history(self):
        # get_random_uids is an example method, but you can replace it with your own.
        miner_uids = get_random_uids(self, k=1)

        block_to_query = random.randrange(self.subtensor.get_current_block())

        # The dendrite client queries the network.
        responses = self.dendrite.query(
            # Send the query to selected miner axons in the network.
            axons=[self.metagraph.axons[uid] for uid in miner_uids],
            # Construct a block hash query.
            synapse=SubtensorQueryBlockHashSynapse(block_hash_to_retrieve=block_to_query),
            deserialize=True,
        )

        # Log the results for monitoring purposes.
        bt.logging.info(f"Received responses: {responses}")

        # Adjust the scores based on responses from miners.
        rewards = get_rewards(self, expected=self.subtensor.get_block_hash(block_to_query), responses=responses)
        
        bt.logging.info(f"Scored responses: {rewards}")
        # Update the scores based on the rewards.
        self.update_scores(rewards, miner_uids)

        time.sleep(60)


    def do_subtensor_miner_rpc(self, query):
        # get_random_uids is an example method, but you can replace it with your own.
        miner_uids = get_random_uids(self, k=1)

        # The dendrite client queries the network.
        responses = self.dendrite.query(
            # Send the query to selected miner axons in the network.
            axons=[self.metagraph.axons[uid] for uid in miner_uids],
            # Construct a block hash query.
            synapse=DoMinerSubtensorRPCSynapse(rpc_query=query),
            deserialize=True,
        )

        # Log the results for monitoring purposes.
        bt.logging.info(f"Received miner rpc response: {responses[0]}")

        return responses[0]



# The main function parses the configuration and runs the validator.
if __name__ == "__main__":
    with Validator() as validator:
        while True:
            bt.logging.info("Validator running...", time.time())
            time.sleep(5)
