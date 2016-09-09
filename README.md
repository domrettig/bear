# bear
Simple command line chat client

## setup
1. Clone this repo

2. On the server, run `python3 server.py` in background

2. On client, create a file called `secret.py` in the `bear` dir containing `HOST = "SERVERIPHERE"`

3. Run `python3 main.py` to start a client connection

## commands
`!exit` in the client to quit program

`!here` to list current users logged into server

## setting up encryption
1. Install pycrypto, `pip3 install pycrypto`

2. In `main.py`, set `encryption=True` in `Client` constructor

3. In `secret.py`, set `KEY="SOME16BYTEKEY"` and `IV="SOME16BYTEIV"`, these need to be the same on all clients connected to one server
