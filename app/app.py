""" Primary handler for python output as input to the electorn application. """

from __future__ import print_function
import sys
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Displaying from Python script."

if __name__ == "__main__":
    print('Python script for main app is active.')
    sys.stdout.flush()
    app.run()
