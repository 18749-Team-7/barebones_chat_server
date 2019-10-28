# Barebones single-server multiple-client UDP chat server

## Introduction
Barebones implementation of a single-server multiple-client UDP chat server for the 18-749 (Building Reliable Distributed Systems) project. Operation is as simple as can be: users connect to the server with a username and begin chatting. That's it! 

## Table of contents
<!--ts-->
   * [Dependencies](#dependencies)
   * [Running the code](#running)
<!--te-->

<a name="dependencies"></a>
## Dependencies
```
Python 3
```

<a name="running"></a>
## Running the code
- Start up the server:
```
sudo python3 server.py
```
- Start up the client(s):
```
python3 client.py -ip <IP ADDRESS> -u <USERNAME>
```
