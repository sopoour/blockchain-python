# 1) Import the random function and generate both a random number between 0 and 1 as well as a random number between 1 and 10.
from random import random, randint

random_float = random()

random_int = randint(1, 10)

print(f"Random number between 0 and 1: {random_float:2.2}")
print("Random number between 1 and 10: ", random_int)

# 2) Use the datetime library together with the random number to generate a random, unique value.
from datetime import datetime

rand_uni_value = str(datetime.now().strftime("%H:%M:%S")) + " - " + f"{random_float:2.2}"

print("Random unique value:", rand_uni_value)