from django.core.exceptions import ValidationError

import re


def whitespace_validator(string):
    if not re.findall(r'[A-Za-z]+', string):
        raise ValidationError('type at least one letter')
