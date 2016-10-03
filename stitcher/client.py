#!/usr/bin/env python

"""
Client that displays frames from socket
"""

from __future__ import absolute_import
import pickle
import socket
import struct
import sys
import cv2
from stitcher.configuration import Configuration

def main():
    """ The main function for the client.py script. """

    config = Configuration()

    host = ''
    port = config.port

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket created'

    soc.bind((host, port))
    print 'Socket bind complete'
    soc.listen(10)
    print 'Socket now listening'

    conn = soc.accept()[0]

    data = ""
    payload_size = struct.calcsize("L")
    while True:
        while len(data) < payload_size:
            data += conn.recv(4096)
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]
        while len(data) < msg_size:
            data += conn.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data)
        cv2.imshow("Result", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            sys.exit(0)

if __name__ == "__main__":
    main()
