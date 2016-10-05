"""
Module for formatting text
"""
from termcolor import colored

CHECK = u'\u2713'
X_MARK = u'\2717'

class Formatter(object):
    """
    Text formatter
    """
    @staticmethod
    def color_text(text, color, textAttrs=[]):
        """
        returns text with given color and attributes
        """
        return colored(text, color, attrs=textAttrs)

    @staticmethod
    def print_heading(text):
        heading = colored(text, "blue", attrs=['bold'])
        print heading

    @staticmethod
    def get_check():
        return colored(CHECK.encode('utf-8'), "green", attrs=['bold'])

    @staticmethod
    def get_xmark():
        return colored(X_MARK.encode('utf-8'), "red", attrs=['bold'])

    @staticmethod
    def print_err(msg):
        formatted_msg = colored(msg, "red", attrs=['bold'])
        print formatted_msg

    @staticmethod
    def get_input_msg(msg):
        return colored(msg, "yellow", attrs=['bold'])

    @staticmethod
    def print_status(msg):
        formatted_msg = colored(msg, "green", attrs=['concealed'])
        print formatted_msg

    @staticmethod
    def print_option(num, msg):
        prompt = "{0}) {1}".format(num, msg)
        formatted_prompt = colored(prompt, "white", attrs=['bold'])
        print(formatted_prompt)
