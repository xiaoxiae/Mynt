# Documentation
This document contains information on how Mynt works (both software and hardware-wise). You should read this if you're either generally interested, or would like to contribute.

## Protocol
Mynt client devices communicate with the server that runs on `<TODO: IP>`. It listens on port `9106` (taken from `[ord(c) % 10 for c in 'mynt']`).

When sending a message to the server, use the following format (making sure to end with a newline!):
```
UID | Mynt ID | command
```

The UID can be pretty much anything device-unique, like MAC address (used in my implementation). Mynt ID is the ID of the paired device, so it is properly sent to the other connected paired one. Supported command formats are the following:
- TODO

Command checking is done on the client side, the server is just here to relay the messages from one client to another. This means that if you wish to add custom commands and still use the official Mynt server, go for it!

When getting a message from the server, the user first has to send a message in the following format (again, making sure to end with a newline!):
```
UID | Mynt ID
```

After this, the server will send a single message back and close the connection.

## Resources
Here are links to resources used during the building of the project.

### Hardware
- ADS1115 with Python: https://learn.adafruit.com/adafruit-4-channel-adc-breakouts/python-circuitpython

### Raspberry Pi
- OTG: https://gist.github.com/gbaman/50b6cca61dd1c3f88f41
- uMTP: https://github.com/viveris/uMTP-Responder

### Python 3
- Socket
	- Article: https://pymotw.com/2/socket/tcp.html
	- How-to: https://docs.python.org/3/howto/sockets.html
	- Documentation: https://docs.python.org/3/library/socket.html
- Threading
	- How-to: https://realpython.com/intro-to-python-threading/
	- Documentation: https://docs.python.org/3/library/threading.html
- Async/await
	- Article: https://realpython.com/async-io-python/
	- Coroutines and Tasks: https://docs.python.org/3/library/asyncio-task.html
	- Event Loop: https://docs.python.org/3/library/asyncio-eventloop.html
	- Streams: https://docs.python.org/3/library/asyncio-stream.html
	- Queues: https://docs.python.org/3/library/asyncio-queue.html
	- asyncio module: https://docs.python.org/3/library/asyncio.html
