from django import forms
from django.forms import formset_factory, BaseFormSet

import re

from .validator import whitespace_validator


class QuestionForm(forms.Form):
    title = forms.CharField(max_length=256, validators=[whitespace_validator], required=True)


class ChoiceForm(forms.Form):
    choice_text = forms.CharField(max_length=256, validators=[whitespace_validator], required=True)


class BaseChoiceFormSet(BaseFormSet):
    def __init__(self, choice_text, *args, **kwargs):
        self._choice_text = choice_text
        super().__init__(*args, **kwargs)

    def clean(self):
        if any(self.errors):
            return

        for form in self.forms:
            if not re.findall(form.choice_text):
                forms.ValidationError('type at least one letter')
