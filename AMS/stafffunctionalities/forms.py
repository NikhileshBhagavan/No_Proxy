from django import forms

from home.models import *

class ModifyForm(forms.ModelForm):
    class Meta:
        model=Absentdates
        fields=['dates_of_absent']
        widgets = {
        'date_of_absent':forms.DateInput(attrs={'type':'date'}),
    }
        