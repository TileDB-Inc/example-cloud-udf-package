# Libraries don't need to be imported directly by the module that contains
# the function being registered; this one is only referred to indirectly.

# As mentioned in important_functions.py, stdlib imports are allowed.
from typing import Type


def int_type() -> Type[int]:
    return int
