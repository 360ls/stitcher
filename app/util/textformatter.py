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
    def print_title(title_text):
        """
        Prints a green, bold, underlined blinking title.
        """
        title = colored(title_text, "blue", attrs=['bold'])
        TextFormatter.print_new_line()
        TextFormatter.print_box(title, "=")
        TextFormatter.print_new_line()

    @staticmethod
    def print_heading(heading_text):
        """
        Prints a blue, bold heading.
        """
        heading = colored(heading_text, "green", attrs=['bold'])
        TextFormatter.print_box(heading)

    @staticmethod
    def print_error(msg):
        """
        Prints error message.
        """
        error_msg = colored("[ERR] %s" % msg, "red", attrs=['bold'])
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
    def print_spacer(length=30, character_type="-"):
        """
        Prints separator line.
        """
        print(character_type * length)

    @staticmethod
    def print_new_line():
        """
        Prints new line.
        """
        print("\n")

    @staticmethod
    def print_box(msg, character_type="-"):
        """
        Prints box with defined msg in the middle of the box.
        """
        msg_length = len(msg) - 9
        TextFormatter.print_spacer(msg_length, character_type)
        print("# %s #" % msg)
        TextFormatter.print_spacer(msg_length, character_type)

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
        return colored("\n%s" % msg, "yellow", attrs=['bold'])
