<div align="center">

# **Blockchain Node Subnet**

<div align="left">

## Bittensor

Bittensor is a blockchain protocol that hosts multiple self-contained incentive mechanisms called subnets. Subnets are playing fields in which:

- Subnet **Miners** do some form of computational work, and
- Subnet **Validators** produce consensus about the quality of the work in order for the protocol to reward the Miners.

## Blockchain Node Subnet Information

With that in mind, this subnet aims to reward **Miners** for running and providing access to blockchain nodes (a piece of software that connects to a blockchain network and verifies and transmits transactions).

**Validators** ensure that **Miners** have ongoing, up-to-date access to a blockchain node by frequently sending challenges to the Miners about the history of the network, as well as sending them transactions and then ensuring that the Miner has posted the transaction to the network.


### Running a miner / validator

The main files related to mining / validating are:

- neurons/miner.py
- neurons/validator.py - for running a validator in 'challenge' only mode.
- neurons/rpc_validator.py - for running a websocket server and validator to relay organic rpc calls to miners.

### Reward Mechanism

The reward mechanism code is located in template/validator/reward.py

Currently it compares synthetic rpc call responses from miners to the ground truth answer of the validators local node. 

If the miners response correctly matches the validators it is rewarded a single point. If the miners response is incorrect it is deducted 3 points. 

Once per Epoch (100 blocks), the points are reset and the weights of each miner are set proportional to the relative amount of points they have earned compared to all other miners.


## Roadmap

### T+1 Month after Launch

- Fine-tune reward mechanism

- Monitoring Subnet stability

- Launch of ws://subtensor.formless.tech public node

## T+3 Months after Launch 

- Ethereum Node RPC Access

- Bounty Rewards for Bugs / Protocol Oversights

## ~T+6 Months after Launch

- Bitcoin Node Access

## Planned Features

- Miners with Block Creation / Proposing access can offer MEV / Flashbot services for large boost to rewards

- Archival Data Nodes Miner Support

- Different rewards for different types of RPC calls