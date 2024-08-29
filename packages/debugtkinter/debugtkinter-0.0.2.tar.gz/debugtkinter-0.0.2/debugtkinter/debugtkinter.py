
from random import randint

def funny_addition(a, b):
    if not a or not b:
        print("Please provide two numbers")
    rand = randint(0, 10)
    if rand == 0:
        print(f"lucky! \n {a+b}")
    else:
        print(a + b + rand)


