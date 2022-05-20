from django.test import TestCase
from django.core.exceptions import ValidationError

import validator


# Create your tests here.
def whitespace(strings: list):
    for i, s in enumerate(strings):
        try:
            validator.whitespace_validator(s)
        except ValidationError:
            print(f"test case {i} is not valid")


strings = ['asdf', '   ', 'qweasf', ' sdaf', 'asdf ', ' ']

whitespace(strings)
