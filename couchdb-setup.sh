#!/bin/bash

# Place this script in ~/Documents directory.

# Download source
wget "http://apache.mirror.serversaustralia.com.au/couchdb/source/2.0.0/apache-couchdb-2.0.0.tar.gz"
tar -xvzf apache-couchdb-2.0.0.tar.gz

# Install dependencies
sudo apt-get --no-install-recommends -y install build-essential pkg-config erlang libicu-dev libmozjs185-dev libcurl4-openssl-dev

# Build source
cd ~/Documents/apache-couchdb-2.0.0/
./configure
make release

# Start couchDB
cp -r ./rel/couchdb/ ~/Documents/
# cd ~/Documents/couchdb
# ./bin/couchdb
