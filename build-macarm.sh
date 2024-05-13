#!/bin/bash

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew install docker --cask

sudo chown -R $(whoami) ~/.docker

open --background -a docker

read -p "Click Open on MacOS Docker pop up, then wait for dashboard. Click Re-apply configurations before pressing enter to continue this script"

DESIREDVER=${1-1100}
echo "Building for $DESIREDVER . To use another PS4 Firwmare Version, execute this script as so: $0 <version>"
pwd=$(pwd)
docker build  --build-arg="PS4FWVER=$DESIREDVER" -t pppwn-docker . --platform linux/amd64
docker run -v "$pwd:/host" pppwn-docker
mv stage1.bin stage1
mv stage2.bin stage2

pkill -SIGHUP -f /Applications/Docker.app 'docker serve' 

brew remove docker