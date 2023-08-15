#!/bin/bash

# Installing docker
sudo apt update
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Install other dependencies
sudo apt install -y build-essential python3-dev

# Install poetry
curl -sSL https://install.python-poetry.org | python3 -
export PATH="/home/vmadmin/.local/bin:$PATH"

# Clone project repositories
#git clone https://github.com/sklempna/vector-db-benchmark.git
git clone https://github.com/chroma-core/chroma.git
cd vector-db-benchmark/
poetry install