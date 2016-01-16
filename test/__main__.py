from termcolor import colored

def start(text): return colored(text, attrs=["bold"])
def success(text): return colored(text, "green", attrs=["bold"])

print(start("\n-----------------Test 1-----------------"))
from .test1 import *
print(success("-------------Test 1 PASSED--------------\n"))

print(start("\n-----------------Test 2-----------------"))
from .test2 import *
print(success("-------------Test 2 PASSED--------------\n"))
