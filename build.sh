#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Set the name and tag for later usage.
CONTAINER_NAME_TAG="python-container-demo:latest"

# Build the container image.
echo ":: building container image..."
docker build -t $CONTAINER_NAME_TAG .

echo
# List container images with given name.
docker images $CONTAINER_NAME_TAG
echo
