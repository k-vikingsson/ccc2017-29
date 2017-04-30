#!/bin/bash

# Navigate to home directory
cd ~

# Download source
wget "http://apache.mirror.serversaustralia.com.au/couchdb/source/2.0.0/apache-couchdb-2.0.0.tar.gz"
tar -xvzf apache-couchdb-2.0.0.tar.gz

# Install dependencies
sudo apt-get --no-install-recommends -y install build-essential pkg-config erlang libicu-dev libmozjs185-dev libcurl4-openssl-dev

# Build source
cd ~/apache-couchdb-2.0.0/
./configure
make release

sudo adduser --system --shell /bin/bash --group --gecos "CouchDB Administrator" couchdb

# Prepare couchDB
sudo cp -r ./rel/couchdb/ /home/couchdb/
sudo chown -R couchdb:couchdb /home/couchdb/couchdb
sudo find /home/couchdb/couchdb -type d -exec chmod 0770 {} \;

# Setup firewall rules
sudo ufw allow 22/tcp
sudo ufw enable
sudo ufw allow 5984/tcp
sudo ufw allow 4369/tcp
sudo ufw allow 9100:9200/tcp

#sudo chmod 0644 /home/couchdb/couchdb/etc/*

# Setup cluster
#sudo apt-get -y install curl
#sudo curl -X PUT http://localhost:5984/_users
#sudo curl -X PUT http://localhost:5984/_replicator
#sudo curl -X PUT http://localhost:5984/_global_changes

# Start CouchDB
#sudo -i -u couchdb couchdb/bin/couchdb
# cd ~/couchdb
# ./bin/couchdb
