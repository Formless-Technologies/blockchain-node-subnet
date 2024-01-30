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

# Bittensor
import bittensor as bt

# Bittensor Validator Template:
from template.protocol import MinerSubtensorRPCSynapse
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


    def challenge_miner(self):
        # Choose random miners to challenge their RPC results. #TODO Change from 1 miner
        miner_uids = get_random_uids(self, k=32)

        # Choose a random RPC query to challenge miners with
        chain_getBlockHash_challenge_query = {"jsonrpc": "2.0", "method": "chain_getBlockHash", "params": [random.randrange(self.subtensor.get_current_block())], "id": 1}
        chain_getFinalizedHead_challenge_query = {"jsonrpc": "2.0", "method": "chain_getFinalizedHead", "params": [], "id": 1}
        chain_system_version_challenge_query = {"jsonrpc": "2.0", "method": "system_version", "params": [], "id": 1}
        rpc_challenges = [chain_getBlockHash_challenge_query, chain_getFinalizedHead_challenge_query, chain_system_version_challenge_query]
        chosen_challenge_rpc = random.choice(rpc_challenges)

        # Query your own Subtensor node to find ground truth answer
        ground_truth = self.subtensor.substrate.rpc_request(method=chosen_challenge_rpc['method'], params=chosen_challenge_rpc['params'])

        # The dendrite client queries the network.
        responses = self.dendrite.query(
            # Send the query to selected miner axons in the network.
            axons=[self.metagraph.axons[uid] for uid in miner_uids],
            # Construct a block hash query.
            synapse=MinerSubtensorRPCSynapse(rpc_query=chosen_challenge_rpc),
            deserialize=True,
        )

        # Log the results for monitoring purposes.
        bt.logging.info(f"Received responses: {responses}")
        # Log the results for monitoring purposes.
        bt.logging.info(f"Expected response: {ground_truth}")

        # Adjust the scores based on responses from miners.
        rewards = get_rewards(self, expected=ground_truth, responses=responses)
        
        bt.logging.info(f"Scored responses: {rewards}")
        # Update the scores based on the rewards.
        self.update_scores(rewards, miner_uids)

        time.sleep(5)


    def organic_miner_subtensor_rpc(self, query):
        # Choose random miners to send RPC request.
        miner_uids = get_random_uids(self, k=1)

        # The dendrite client queries the network.
        responses = self.dendrite.query(
            # Send the query to selected miner axons in the network.
            axons=[self.metagraph.axons[uid] for uid in miner_uids],
            # Construct a block hash query.
            synapse=MinerSubtensorRPCSynapse(rpc_query=query),
            deserialize=True,
        )

        # Log the results for monitoring purposes.
        bt.logging.info(f"Received miner rpc response: {responses}")

        return responses[0]



# The main function parses the configuration and runs the validator.
if __name__ == "__main__":
    with Validator() as validator:
        while True:
            bt.logging.info("Validator running...", time.time())
            time.sleep(5)
