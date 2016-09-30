"""
This function scans from user input, guaranteeing that a number is entered into the terminal.
"""

def read_int(prompt):
    try:
        num_input = int(raw_input(prompt))
        print ""
        return num_input
    except ValueError:
        print "Please enter a number."
