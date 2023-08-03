from django import forms
from ..models.user import User

class EmailForm(forms.ModelForm):

    class Meta:
        model=User
        
        fields =['email']
        required=['email']
        labels={
            'email':('Email'),
        }