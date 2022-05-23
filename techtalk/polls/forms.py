from django import forms
from django.forms import BaseFormSet
from django.core.exceptions import ValidationError

from .validator import none_str_validator


class QuestionForm(forms.Form):
    title = forms.CharField(max_length=256, validators=[none_str_validator], required=True)


class ChoiceForm(forms.Form):
    choice_text = forms.CharField(max_length=256, validators=[none_str_validator], required=True)


class BaseChoiceFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return

        for form in self.forms:
            choice_text = form.cleaned_data.get('choice_text')
            print(choice_text)
            if choice_text is None:
                raise ValidationError('choice must contains at least one letter')
