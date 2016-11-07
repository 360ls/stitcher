"""
Primary handler for python output as input to the electron application.
"""

from __future__ import absolute_import, division, print_function
import sys
from flask import Flask, render_template
from .util.validatefeeds import view_valid_camera_feeds


def run_cli():
    """ Runs the command line interface for displaying stitching and streaming functionality. """
    return "Running from script outside of Flask."

APP = Flask(__name__)

@APP.route("/")
def index():
    """ Displays boilerplate output to the electron application. """
    return render_template('index.html', cli_driver=run_cli)

@APP.route('/cli')
def cli_driver():
    """ The route for calling the stitching and streaming command line interface. """
    return render_template('cli.html', cli_driver=run_cli)

if __name__ == "__main__":
    run_cli()
    sys.stdout.flush()
    APP.run()
