#!/bin/bash

# install MATE desktop
sudo apt-add-repository ppa:ubuntu-mate-dev/xenial-mate
sudo apt-get update
sudo apt-get install mate
# install X2GO Server
sudo add-apt-repository ppa:x2go/stable
sudo apt-get update
sudo apt-get install x2goserver x2goserver-xsession
sudo apt-get install x2gomatebindings
