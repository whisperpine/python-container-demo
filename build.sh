#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Set the name and tag for later usage.
container_name_tag="python-container-demo:latest"

# Build the container image.
echo ":: building container image..."
docker build -t $container_name_tag .

echo
# List container images with given name.
docker images $container_name_tag
echo
