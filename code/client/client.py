"""A module for communicating with the Mynt server."""
from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR
from time import sleep
from uuid import getnode as get_mac

MAX_MESSAGE_SIZE = 1024


def send_data(data: str, sock: socket):
    sock.sendall(data.encode("utf-8") + b"\n")


def receive_data(sock: socket):
    return sock.recv(MAX_MESSAGE_SIZE)


if __name__ == "__main__":
    uid = hex(get_mac())
    mynt_id = "test"

    SEND = False

    # first send some data
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(("localhost", 9106))

    if SEND:
        send_data(f"{uid} | {mynt_id} | test command", sock)
        sock.close()
    else:
        send_data(f"{uid}123 | {mynt_id}", sock)

        print(receive_data(sock))
        sock.close()
