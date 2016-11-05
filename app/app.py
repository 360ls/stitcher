""" Primary handler for python output as input to the electron application. """

from __future__ import print_function
import sys
from flask import Flask

APP = Flask(__name__)

@APP.route("/")
def home():
    """ Displays boilerplate output to the electron application. """
    run_cli()
    return "This just demonstrates that a python script can be run with a proper electron instance."



def run_cli():
    """ Runs the command line interface for displaying stitching and streaming functionality. """
    print('hey there')

if __name__ == "__main__":
    run_cli()
    sys.stdout.flush()
    APP.run()
