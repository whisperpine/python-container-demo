# Python Container Demo

A demo project to show how to build container images for a python project with
best practices.

## Reference

- [astral-sh/uv-docker-example](https://github.com/astral-sh/uv-docker-example).
- [Using uv in Docker - uv docs](https://docs.astral.sh/uv/guides/integration/docker/).

## Tech Stack Selection

- The dev environment is managed by [nix flakes](https://nixos.wiki/wiki/Flakes).
- The python package and project manager is [uv](https://github.com/astral-sh/uv).

## Prerequisites

- Linux or macOS with [nixpkgs](https://github.com/NixOS/nixpkgs) installed,
and with `flakes` and `nix-command` features enabled.
- A tool that can build container images.
In this demo, [docker](https://www.docker.com/) is preferred.

## Nix Dev Environment

[nix-direnv](https://github.com/nix-community/nix-direnv) is highly recommended
to improve the quality of life working with nix managed dev environment. Besides
other benefits (e.g. caching), nix-direnv automatically runs `nix develop` every
time you `cd` to the project. All you need to do is to initialize each project
once with `direnv allow` command.

```sh
# `dirnev allow` needs to be run only once.
# After that, when you `cd` in, nix dev env will be automatically loaded.
cd THIS_REPO && dirnev allow
# Check if the dev environment loads as expected.
python --version && which python
```

Without the help of [nix-direnv](https://github.com/nix-community/nix-direnv),
the `nix develop` needs to be run manually every time:

```sh
# `nix develop` needs to be run every time you `cd` in.
cd THIS_REPO && nix develop
# Check if the dev environment loads as expected.
python --version && which python
```

## Python Packages

[uv](https://github.com/astral-sh/uv)
is an extremely fast Python package and project manager.
It's a drop-in replacement of `pip`, `pyenv`, `virtualenv` and more.
In this repo, `uv` is used both in the building stage and dev stage:

- During the building stage, `uv`'s official container image is used to
install all the dependencies.
- During the dev stage, `uv` command will be available when
[nix dev environment](#nix-dev-environment) is loaded.

```sh
# install dependencies specified in uv.lock
uv sync               
# add or remove dependencies
uv add PACKAGE_NAME
uv remove PACKAGE_NAME
```

## Python Version

Although `uv` can handle python versions properly in virtual environment,
the package management mechanism of nix conflicts with `uv`'s.
Hence, use `flake.nix` to manage python version.

```nix
# modify "python313" to change python version.
packages = with pkgs; [ python313 ];
```

To make `uv` notice the altered python version,
change [pyproject.toml](./pyproject.toml) as well.
Don't forget to change the base image tags in [Dockerfile](./Dockerfile) accordingly
(both of the base image tags need to be changed).

## Build Container Image

Suppose `docker` is used to build container image.

```sh
# build image and print the result
sh ./build.sh
```

## Docker Compose

Despite that `docker compose` is often used to deploy containerized app,
it can also be quite useful to facilitate local development.
And [compose.yaml](./compose.yaml) herein is a simple showcase.

```sh
# Build and start the containerized app, and watch if there is a change.
# If any changes detected in local file system, auto rebuild and restart.
docker compose watch
```
