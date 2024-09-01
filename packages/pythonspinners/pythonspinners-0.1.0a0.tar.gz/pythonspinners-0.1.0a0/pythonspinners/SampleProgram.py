import time

def sample_usage(name, age, occupation=None, location=None):
    """
    A sample function to demonstrate the usage of the above created animation.
    """
    print(f"Hello, {name}! You are {age} years old.")
    if occupation:
        print(f"You work as a {occupation}.")
    if location:
        print(f"You live in {location}.")
    time.sleep(5)
