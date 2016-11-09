""" Module for handling response to invalid incoming camera feed. """

def get_main_color(frame, num_colors=1048):
    """ Returns the main color of the provided frame. """
    colors = frame.getcolors(num_colors)
    max_occurence = 0
    mode = 0
    try:
        for color in colors:
            if color[0] > max_occurence:
                (max_occurence, mode) = color
        return mode
    except TypeError:
        raise Exception("Too many colors in the image. Please provide a larger number of colors.")
