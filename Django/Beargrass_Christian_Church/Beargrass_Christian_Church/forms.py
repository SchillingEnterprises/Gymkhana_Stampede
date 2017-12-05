from django import forms


def must_be_empty(value):
    if value:
        raise forms.ValidationError('is not empty')
