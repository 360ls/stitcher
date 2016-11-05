"""
Module for formatting text - typically used in conjunction with the command line interface.
"""
from termcolor import colored

CHECK = u'\u2713'
X_MARK = u'\u2717'

class Formatter(object):
    """
    Text formatter
    """

    @staticmethod
    def color_text(text, color, text_attributes):
        """
        Returns text with defined color and text_attributes.
        """
        return colored(text, color, attrs=text_attributes)

    @staticmethod
    def print_heading(text):
        """
        function for printing headings
        """
        heading = colored(text, "blue", attrs=['bold'])
        print heading

    @staticmethod
    def get_check():
        """
        returns checkmark symbol
        """
        return colored(CHECK.encode('utf-8'), "green", attrs=['bold'])

    @staticmethod
    def get_xmark():
        """
        returns x symbol
        """
        return colored(X_MARK.encode('utf-8'), "red", attrs=['bold'])

    @staticmethod
    def print_err(msg):
        """
        function for printing error message
        """
        formatted_msg = colored(msg, "red", attrs=['bold'])
        print formatted_msg

    @staticmethod
    def get_input_msg(msg):
        """
        function for printing prompt for input
        """
        return colored(msg, "yellow", attrs=['bold'])

    @staticmethod
    def print_status(msg):
        """
        function for printing status message
        """
        formatted_msg = colored(msg, "green", attrs=['concealed'])
        print formatted_msg

    @staticmethod
    def print_option(num, msg):
        """
        function for printing option message
        """
        prompt = "{0}) {1}".format(num, msg)
        formatted_prompt = colored(prompt, "white", attrs=['bold'])
        print formatted_prompt

    @staticmethod
    def print_pair(key, val):
        """
        function for printing key value pair
        """
        adjusted_key = ("{0}:".format(key)).ljust(15)
        formatted_key = colored(adjusted_key, "cyan", attrs=['bold'])
        formatted_val = colored(val, "magenta", attrs=['bold'])
        print "{0}{1}".format(formatted_key, formatted_val)
