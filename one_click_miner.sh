#!/bin/bash

# Stop the script if any command fails
set -e

# Update and Upgrade the System
echo "Updating and Upgrading the system..."
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
echo "Installing Docker..."
sudo apt-get install -y docker.io

# Start and Enable Docker
echo "Starting and enabling Docker..."
sudo systemctl start docker
sudo systemctl enable docker

# Install Docker Compose
echo "Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.5/docker-compose-linux-x86_64" -o /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

# Clone Git Repositories
echo "Cloning Git repositories..."
git clone https://github.com/Formless-Technologies/blockchain-node-subnet
git clone https://github.com/opentensor/subtensor

echo "Starting local subtensor node..."
sudo ./subtensor/scripts/run/subtensor.sh -e docker --network mainnet --node-type lite

echo "Environment setup complete!"
