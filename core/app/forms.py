from django import forms
from . models import Dash

class FailureForm(forms.Form):
    type_of_failure = Dash.objects.values_list('type_of_failure', flat=True).distinct()
    failure_choices = [(choice, choice) for choice in type_of_failure]
    Failure = forms.ChoiceField(choices=failure_choices)