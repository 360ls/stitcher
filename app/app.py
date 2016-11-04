""" Primary handler for python output as input to the electorn application. """

from __future__ import print_function
import sys
from flask import Flask

APP = Flask(__name__)

@APP.route("/")
def hello():
    """ Displays boilerplate output to the electron application. """
    return "Displaying from Python script."

if __name__ == "__main__":
    print('Python script for main app is active.')
    sys.stdout.flush()
    APP.run()
