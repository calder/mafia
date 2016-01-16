from termcolor import colored

def started(text): return colored(text, attrs=["bold"])
def success(text): return colored(text, "green", attrs=["bold"])

print(started("\n-----------------Test 1-----------------"))
from .test1 import *
print(success("-------------Test 1 PASSED--------------\n"))

print(started("\n-----------------Test 2-----------------"))
from .test2 import *
print(success("-------------Test 2 PASSED--------------\n"))
