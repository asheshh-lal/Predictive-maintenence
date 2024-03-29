from django import forms
from . models import Dash

class FailureForm(forms.Form):
    type_of_failure = Dash.objects.values_list('type_of_failure', flat=True).distinct()
    failure_choices = [(choice, choice) for choice in type_of_failure]
    Failure = forms.ChoiceField(choices=failure_choices)
    
class ApprovalForm(forms.Form):
    # type_of_machine = Dash.objects.values_list('Type', flat=True).distinct()
    TYPE_CHOICES = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
    )
    Type = forms.ChoiceField(choices=TYPE_CHOICES, label='Type of Machine (0-L,1-M,2-L)')
    Rotational_speed_rpm=forms.IntegerField()
    Torque_Nm=forms.IntegerField()
    Tool_wear_min=forms.IntegerField()
    Air_temperature=forms.IntegerField()
    Process_temperature=forms.IntegerField()

class ApprovalForm2(forms.Form):
    # type_of_machine = Dash.objects.values_list('Type', flat=True).distinct()
    TYPE_CHOICES = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
    )
    Type = forms.ChoiceField(choices=TYPE_CHOICES, label='Type of Machine (0-L,1-M,2-L)')
    Rotational_speed_rpm=forms.IntegerField()
    Torque_Nm=forms.IntegerField()
    Tool_wear_min=forms.IntegerField()
    Air_temperature=forms.IntegerField()
    Process_temperature=forms.IntegerField()