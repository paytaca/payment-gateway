from .models import User
from django import forms
from django.forms import ModelForm

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'full_name',
            'email',
            'username',
            'password',
        )
        
class WalletForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'xpub_key',
		    'wallet_hash',
        )