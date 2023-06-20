from django import forms
from .models import Claim

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

#-------------------------Form-------------------------

class ClaimForm(forms.ModelForm):

    class Meta:
        model = Claim
        fields = '__all__'  