
from django import forms
from .models import *
class QueryFormResponse(forms.ModelForm):
    class Meta:
        model=Query
        fields=['answer']
        widgets = {
            'answer': forms.Textarea(attrs={'placeholder': '    Please enter your response here'}),
            
        }
class QueryFormRequest(forms.ModelForm):
    class Meta:
        model=Query
        fields=['question']
        widgets = {
            'question': forms.Textarea(attrs={'placeholder': '    Please enter your question here'}),
            
        }
   