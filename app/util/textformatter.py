"""
Module for formatting text - typically used in conjunction with the command line interface.
"""
from __future__ import print_function
from termcolor import colored

CHECK = u'\u2713'
X_MARK = u'\u2717'

class TextFormatter(object):
    """
    Text formatter for displaying different kinds of formatted text.
    """

    @staticmethod
    def color_text(text, color, text_attributes=None):
        """
        Returns text with defined color and text_attributes.
        """
        if text_attributes is None:
            return colored(text, color, attrs=[])
        else:
            return colored(text, color, attrs=text_attributes)

    @staticmethod
    def print_heading(heading_text):
        """
        Prints a blue, bold heading.
        """
        heading = colored(heading_text, "blue", attrs=['bold'])
        print(heading)
        TextFormatter.print_spacer()

    @staticmethod
    def print_err(msg):
        """
        Prints error message.
        """
        error_msg = colored(msg, "red", attrs=['bold'])
        print(error_msg)

    @staticmethod
    def print_status(msg):
        """
        Prints status message.
        """
        status_msg = colored(msg, "green", attrs=['concealed'])
        print(status_msg)

    @staticmethod
    def print_option(num, msg):
        """
        Prints option message.
        """
        prompt = "{0}) {1}".format(num, msg)
        formatted_option = colored(prompt, "white", attrs=['bold'])
        print(formatted_option)

    @staticmethod
    def print_pair(key, val):
        """
        Prints a key value pair.
        """
        adjusted_key = ("{0}:".format(key)).ljust(15)
        formatted_key = colored(adjusted_key, "cyan", attrs=['bold'])
        formatted_val = colored(val, "magenta", attrs=['bold'])
        print("{0}{1}".format(formatted_key, formatted_val))

    @staticmethod
    def print_spacer():
        """
        Prints separator line.
        """
        print ("\n--------------------\n")

    @staticmethod
    def get_check():
        """
        Returns check-mark symbol.
        """
        return colored(CHECK.encode('utf-8'), "green", attrs=['bold'])

    @staticmethod
    def get_xmark():
        """
        Returns x-mark symbol.
        """
        return colored(X_MARK.encode('utf-8'), "red", attrs=['bold'])

    @staticmethod
    def get_input_msg(msg):
        """
        Returns message prompt for user input.
        """
        return colored(msg, "yellow", attrs=['bold'])
