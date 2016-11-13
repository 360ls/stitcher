"""
Module responsible for checking the effectiveness and accuracy of enforced fps.
"""

from __future__ import absolute_import, division, print_function
import time
from textformatter import TextFormatter


def main():
    """
    Responsible for printing information about accuracy of enforced fps.
    """
    compare_sleep_to_fps()

def compare_sleep_to_fps(fps=30, accuracy=0.1):
    """
    Compares sleep duration to provided objective fps.
    """
    duration = 1.0 / fps
    total_loops, total_errors = (0, 0)
    residual_average = 0

    while True:
        first_time = time.time()
        time.sleep(duration)
        second_time = time.time()
        elapsed_time = second_time - first_time
        residual = (elapsed_time / duration) - 1
        TextFormatter.print_info("Slept %f compared to expected %f." % (elapsed_time, duration))
        if residual > accuracy:
            total_errors += 1
            TextFormatter.print_error("The fps is too inaccurate.")
        residual_average = ((residual_average * total_loops) + residual) / (total_loops + 1)
        TextFormatter.print_info("Total Number of Loops: %d" % total_loops)
        TextFormatter.print_info("Residual Average for those Loops: %f" % residual_average)
        total_loops += 1

if __name__ == "__main__":
    main()
