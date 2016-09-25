def read_int(prompt):
    try:
        input = int(raw_input(prompt))
        print ""
        return input
    except ValueError:
        print "Please enter a number."
