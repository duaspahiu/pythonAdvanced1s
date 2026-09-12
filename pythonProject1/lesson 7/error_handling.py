from idlelib.editor import keynames

from six import text_type
from streamlit import text_input, exception

try:
    result=10/0
except ZeroDivisionError:
    print("00ps you tried to divide by zero ")

fruits = {
    "apple":5,
    "banana":7,
    "orange":3
}

try:
    print(fruits["cherry"])

except keyerror:
    print("the key does not exist in the directory")

text = "hello this is not a number"

try:
    text_to_int = int(Text)
except exception as e:
    print("ka ndodh nje error gjat shendrrimit te tekstit ne number")


try:
    result=10/0
except ZeroDivisionError:
    print("00ps you tried to divide by zero ")
finally:
    print("ky line  of code ekzekutohet gjdo her")
