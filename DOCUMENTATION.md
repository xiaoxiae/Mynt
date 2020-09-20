# Documentation
This document contains information on how Mynt works (both software and hardware-wise). You should read this if you're either generally interested in the inner workings of Mynt, or would like to contribute to the project.

## Protocol
Mynt client devices communicate with the server that runs on `<TODO: IP>` and listens on port `9106` (taken from `[ord(c) % 10 for c in 'mynt']`). The source code can be found in `code/server/server.py`.

When sending a message to another Mynt device, use the following message format:
```
<UID> | <Mynt ID> | <command>\n
```

The UID can be pretty much anything device-unique, like MAC address (used in my implementation). Mynt ID is the ID of the paired device, so it is relayed to the other device. Supported command formats are the following:
- TODO

Command checking is done on the client side, the server is just here to relay the messages from one client to another. This means that if you wish to add custom commands and still use the official Mynt server, go for it (but it might be better to create a pull request so other people can benefit from them as well 🙂).

When getting a message from the server, the user first has to send a message in the following format:
```
<UID> | <Mynt ID>\n
```

After this, the server will either close the connection without sending anything if there are no messages for the client, or send one message back and then close the connection if there are some.
