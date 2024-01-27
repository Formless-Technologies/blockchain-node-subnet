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

import typing
import bittensor as bt

# (developer): Formless Technologies

class SubtensorQueryBlockHashSynapse(bt.Synapse):
    """
    Requests the block hash of the specific block on the Bittensor network.

    Attributes:
    - block_to_retrieve: An integer value of the block to retrieve the hash of.
    - block_hash: The retrieved block hash of the specific block, when filled, represents the response from the miner.
    """

    # Required request input, filled by sending dendrite caller.
    block_hash_to_retrieve: int

    # Optional request output, filled by recieving axon.
    block_hash: typing.Optional[str] = None

    def deserialize(self) -> str:
        """
        Deserialize the output. This method retrieves the response from
        the miner in the form of block_hash, deserializes it and returns it
        as the output of the dendrite.query() call.

        Returns:
        - str: The deserialized response
        """
        return self.block_hash
