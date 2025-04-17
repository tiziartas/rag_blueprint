#!/bin/bash

# ===============================================================
# RAG Blueprint Initialization Script
# ===============================================================
# Purpose: Sets up and initializes the RAG environment
# Usage: ./init.sh --env <environment_name>
# Example: ./init.sh --env dev
# ===============================================================

# ===== ENVIRONMENT SETUP =====

# Read environment name from command line arguments
if [ "$1" = "--env" ] && [ -n "$2" ]; then
    env="$2"
    echo "Environment: $env"
else
    echo "Please provide the environment name as an argument. E.g. './init.sh --env dev'"
    exit 1
fi

# ===== BUILD CONFIGURATION =====

# Setup initialization variables
# Creating unique build name with timestamp to avoid conflicts
current_epoch=$(date +%s)
build_name="build-${current_epoch}"

# Configure logging paths
log_dir="build/workstation/logs"
log_file="${log_dir}/${build_name}.log"
mkdir -p $log_dir

# ===== PREREQUISITES CHECK =====

# Verify virtual environment is activated
# This ensures all dependencies are installed in the proper environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Please activate the virtual environment before running the initialization script."
    exit 2
fi

# Check if UV package manager is available
# UV is used for faster Python dependency management
if ! command -v uv &> /dev/null; then
    echo "UV is not installed. Please install uv and try again."
    exit 3
fi

# ===== DEPENDENCY INSTALLATION =====

# Install required packages using UV package manager
echo "Installing required packages"

# Sync all packages including optional extras
uv sync --all-extras

# ===== INITIALIZATION EXECUTION =====

# Run initialization in background process with logging
echo "Running initialization script in the background. You can find live logs at ${log_file}"

# Execute Python runner with appropriate parameters
# --build-name: Unique identifier for this build
# --log-file: Where to output detailed logs
# --env: Target environment for deployment
# --docker-compose-file: Path to the Docker Compose file
# --init: Flag to trigger initialization procedures
nohup python build/workstation/runner.py \
    --build-name $build_name \
    --log-file $log_file  \
    --env $env \
    --docker-compose-file "build/workstation/docker/docker-compose.base.yml" \
    --init \
    > $log_file &

# Capture and display the background process ID for reference
nohup_pid=$!
echo "Process ID: $nohup_pid"
