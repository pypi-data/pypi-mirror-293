from typing import Iterable
from datetime import datetime

class MersenneTwister:
    def __init__(self, seed=None):
        # Initialize the generator with a given seed or current time
        self.index = 624  # Index to track the current position in the mt array
        self.mt = [0] * 624  # Array to hold the state of the generator
        self.seed = seed  # User-defined seed

        if self.seed is None:
            # If no seed is provided, use the current time as the seed
            now = datetime.now()
            # Combine hours, minutes, and seconds to create a seed value
            self.seed = now.hour + now.minute + now.second

        # Initialize the first value of the state vector
        self.mt[0] = self.seed

        # Fill the state vector with values based on the seed
        for i in range(1, 624):
            # Mathematical formula to initialize each element in the mt array
            self.mt[i] = (1812433253 * (self.mt[i - 1] ^ (self.mt[i - 1] >> 30)) + i) & 0xffffffff

    def extract_number(self):
        # Extract a random number; if all numbers have been extracted, twist the state
        if self.index >= 624:
            self._twist()  # Transform the state to generate new numbers

        y = self.mt[self.index]  # Get the number at the current index
        self.index += 1  # Move to the next index
        # Apply a series of bit-wise operations to temper the extracted number
        y ^= (y >> 11)
        y ^= (y << 7) & 0x9d2c5680
        y ^= (y << 15) & 0xefc60000
        y ^= (y >> 18)
        # Return the final random number as a 32-bit integer
        return y & 0xffffffff

    def extract_number_in_range(self, low, high):
        # Returns a random number within a specified range [low, high)
        if low >= high:
            raise ValueError("Low must be less than high.")  # Ensure valid range
        random_number = self.extract_number()  # Extract a random number
        return low + (random_number % (high - low))  # Map to the specified range

    def randfloat(self):
        """Generate a random floating-point number in the range [0.0, 1.0)."""
        # Return a floating-point number normalized between 0 and 1
        return self.extract_number() / 0xffffffff  # Divide by maximum 32-bit integer

    def _twist(self):
        # Generates the next state for the Mersenne Twister algorithm
        for i in range(624):
            # Combine bits from the current and next state to create new state
            y = (self.mt[i] & 0x80000000) + (self.mt[(i + 1) % 624] & 0x7fffffff)
            self.mt[i] = self.mt[(i + 397) % 624] ^ (y >> 1)  # Apply transformation based on Mersenne Twister algorithm
            if y % 2 != 0:  # If the last bit of y is 1
                self.mt[i] ^= 0x9908b0df  # Apply an additional transformation

        self.index = 0  # Reset index for the next extraction cycle

# Global generator initialized with default seed
mt = MersenneTwister()  # Create an instance of the MersenneTwister

def set_seed(s: int):
    """Sets the seed for the random number generator."""
    global mt  # Access the global MersenneTwister instance
    mt.__init__(seed=s)  # Reinitialize the generator with the new seed

def randint(a: int, b: int):
    """Returns a random integer between a and b, inclusive of a and exclusive of b."""
    return mt.extract_number_in_range(a, b)  # Generate a random integer in the specified range

def random():
    """Returns a random floating-point number in the range [0.0, 1.0)."""
    return mt.randfloat()  # Generate a random float between 0 and 1

def rand(n:int=1):
    """returns a list containing n random numbers."""
    l = []
    for _ in range(n):
        l.append(mt.extract_number())
    return l

def randn():
    """returns a random number. similar to rand(1), but instead of a list, it returns a number."""
    return mt.extract_number()

def choice(c: Iterable):
    """Returns a random element from the provided iterable."""
    return c[mt.extract_number_in_range(0, len(c))]  # Select a random element from the iterable
