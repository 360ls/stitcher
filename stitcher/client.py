"""
This module is responsible for setting up the client-socket pairing for streaming of video output. It is simply a script and does not contain any classes or function declarations.
"""

#!/usr/bin/env python

import socket
import sys
import cv2
import pickle
import numpy as np
import struct
from utils.configuration import Configuration

def main(): 
    """ The main function for the client.py script. """

    config = Configuration()

    HOST = ''
    PORT = config.port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket created'

    s.bind((HOST, PORT))
    print 'Socket bind complete'
    s.listen(10)
    print 'Socket now listening'

    conn, addr = s.accept()

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

        frame=pickle.loads(frame_data)
        cv2.imshow("Result", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            sys.exit(0)

if __name__ == "__main__":
    """ Ensures that script is only run when called explicitly. """
    main()
