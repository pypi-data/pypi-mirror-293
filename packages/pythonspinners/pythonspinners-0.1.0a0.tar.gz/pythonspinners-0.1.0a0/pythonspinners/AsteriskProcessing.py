"""
This file contains a class that uses 3 asterisks to create a very commonly found loading animation found on Arch Linux. Again, you can pass a function as an argument, and pass the function's arguments using args and kwargs. You can run the file, a small sample function has been used to demonstrate the effect of the animation.
"""

import threading
import time
import sys

from SampleProgram import sample_usage

class AsteriskProcessing:

    def __init__(self, function, args=(), kwargs={}):
        """
        The constructor accepts any function. Its arguments can be passed using args and kwargs. It sets all of these things as attrubutes. It creates a thread to run the passed function concurrently, and loads the animation on the STDOUT.
        """
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.done = False
        self.thread = threading.Thread(target=self.run_function)
        self.thread.start()
        self.animation()

    def run_function(self):
        """
        Calls the passed function with the passed arguments.
        """
        self.function(*self.args, **self.kwargs)
        self.done = True

    def animation(self):
        """
        The patty of the burger. Does the animation on the screen, as long as the function is executing.
        """
        string_list = [
            "  *****  ",
            " *****   ",
            "*****    ",
            " *****   ",
            "  *****  ",
            "   ***** ",
            "    *****",
        ]
        idx = 0
        while not self.done:
            sys.stdout.write("\r" + string_list[idx])
            sys.stdout.flush()
            idx = (idx + 1) % len(string_list)
            time.sleep(0.2)

        sys.stdout.write("\rDone        \n")

if __name__ == "__main__":
    asterisk_processing = AsteriskProcessing(sample_usage, args=("John Doe", 24), kwargs=({"occupation": "Software Engineer", "location": "World"}))
