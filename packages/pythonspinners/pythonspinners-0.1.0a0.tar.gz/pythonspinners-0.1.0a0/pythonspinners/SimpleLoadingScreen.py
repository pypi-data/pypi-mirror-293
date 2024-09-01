"""
This file contains a class that creates a very simple loading screen on the terminal window. You can pass a function
as an argument to the constructor, and its arguments using args, or keyword args using kwargs. You can run the file to understand its effect.
"""

import threading
import time
import sys

from SampleProgram import sample_usage 

class SimpleLoadingScreen:
    def __init__(self, function, args=(), kwargs={}):
        """
        The constructor accepts the function, and its args and kwargs. Sets them as attributes,
        Starts a thread to run the function concurrently, and loads the animation.
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
        The goey of the marshmello. Does the animation on the screen, as long as the function is executing.
        """
        loading_chars = "|/-\\"
        idx = 0
        while not self.done:
            sys.stdout.write("\r" + loading_chars[idx])
            sys.stdout.flush()
            idx = (idx + 1) % len(loading_chars)
            time.sleep(0.1)

        sys.stdout.write("\rDone          \n")
        

if __name__ == "__main__":
    loading_screen = SimpleLoadingScreen(sample_usage, args=("John Doe", 24), kwargs={"occupation": "Software Engineer","location": "World"})

