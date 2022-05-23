from django.core.exceptions import ValidationError


def none_str_validator(string):
    if string is None:
        raise ValidationError('type at least one letter')
