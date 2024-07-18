#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e
set -o xtrace

# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y build-essential

# Add NVIDIA's CUDA repository
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin
sudo mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/3bf863cc.pub
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/ /"

# Update package list
sudo apt update

# Install CUDA
sudo apt install -y cuda

# Set up environment variables
echo 'export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}' >> ~/.bashrc

# Apply the changes
source ~/.bashrc

# Verify the installation
nvcc --version

echo "CUDA installation completed successfully!"
