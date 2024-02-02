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

### Setup

<details>
 <summary>Click to show setup instructions</summary>

In order to mine or validate on this subnet you must complete the following steps / setup.

1. Install dependencies

```bash
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install git-all
sudo apt-get install python3-pip
sudo apt-get install python3-venv
```

2. Ensure you have docker & docker-compose installed on your system

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

3. Clone both repositories you will need

```bash
git clone https://github.com/Formless-Technologies/blockchain-node-subnet
git clone https://github.com/opentensor/subtensor
```

4. Start your local subtensor node with docker
```bash
cd subtensor
sudo ./scripts/run/subtensor.sh -e docker --network mainnet --node-type lite
cd ..
```

5. Create a virtual environment for the subnet and install requirements
```
cd blockchain-node-subnet
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
python3 -m pip install -e .
```

6. Ensure you have a Bittensor Cold and Hot wallet created and funded. [Bittensor Wallet Creation Guide](https://docs.bittensor.com/getting-started/wallets)

7. Register a UID on the subnet (Subnet ID is not yet confirmed)
```bash
btcli subnet register --wallet.name coldwallet --wallet.hotkey hotwallet --subtensor.network local
```

8. Start your miner / validator

**Miner**
```bash
python3 neurons/miner.py --netuid x --subtensor.chain_endpoint ws://127.0.0.1:9944 --wallet.name coldwallet --wallet.hotkey hotwallet --logging.debug
```

**Validator**

Validators have the option to either:
- Run a 'challenge' validator, which only sends synthetic challenges to miners and scores them. 

```bash
python neurons/validator.py --netuid x --subtensor.chain_endpoint ws://127.0.0.1:9944 --wallet.name coldwallet --wallet.hotkey hotwallet --logging.debug
```

- Run a 'RPC Relay' Validator, which also runs a Websocket server that can be used as a replacement chain_endpoint or subtensor.network and relays organic RPC calls to miners on the network.

```bash
python neurons/rpc_validator.py --netuid x --subtensor.chain_endpoint ws://127.0.0.1:9944 --wallet.name coldwallet --wallet.hotkey hotwallet --logging.debug
```

</details>

### Reward Mechanism

The reward mechanism code is located in template/validator/reward.py

Currently it compares synthetic rpc call responses from miners to the ground truth answer of the validators local node. 

If the miners response correctly matches the validators it is rewarded a single point. If the miners response is incorrect it is deducted 3 points. 

Once per Epoch (100 blocks), the points are reset and the weights of each miner are set proportional to the relative amount of points they have earned compared to all other miners.


## Roadmap

### Known Issues

- Subscriptions are not yet supported

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