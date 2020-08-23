# Documentation
This document contains information on how Mynt works (both software and hardware-wise). You should read this if you're either generally interested, or would like to contribute.

## Protocol
Mynt client devices communicate with the server that runs on `<TODO: IP>`. It listens to two ports: `9106` (taken from `[ord(c) % 10 for c in 'mynt']`, client -> server communication) and `9107` (server -> client communication).

Each communication session begins with the client sending two lines: its UID (can be pretty much anything; MAC address is used in my implementation) and its Mynt ID.  After that, it either writes to server or listens to the server.

### Client -> Server commands

### Server -> Client commands

## Resources
Here are links to resources used during the building of the project.

### Hardware
- ADS1115 with Python: https://learn.adafruit.com/adafruit-4-channel-adc-breakouts/python-circuitpython

### Raspberry Pi
- OTG: https://gist.github.com/gbaman/50b6cca61dd1c3f88f41
- uMTP: https://github.com/viveris/uMTP-Responder

### Python 3
- Socket
	- How-to: https://pymotw.com/2/socket/tcp.html
	- Documentation: https://docs.python.org/3/library/socket.html
- Threading
	- How-to: https://realpython.com/intro-to-python-threading/
	- Documentation: https://docs.python.org/3/library/threading.html
- Async/await
	- How-to: https://realpython.com/async-io-python/
	- Coroutines and Tasks: https://docs.python.org/3/library/asyncio-task.html
	- Event Loop: https://docs.python.org/3/library/asyncio-eventloop.html
	- Streams: https://docs.python.org/3/library/asyncio-stream.html
	- Queues: https://docs.python.org/3/library/asyncio-queue.html
	- asyncio module: https://docs.python.org/3/library/asyncio.html
