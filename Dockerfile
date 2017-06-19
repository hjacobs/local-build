FROM ubuntu:16.04

# install same software as on Ubuntu 16.04 AMI used for building
RUN apt-get update && apt-get install -y software-properties-common
