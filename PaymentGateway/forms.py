from .models import Account
from django import forms
from django.forms import ModelForm

class UserForm(ModelForm):
    class Meta:
        model = Account
        fields = (
            'full_name',
            'email',
            'username',
            'password',
        )
        
class WalletForm(ModelForm):
    class Meta:
        model = Account
        fields = (
            'xpub_key',
		    'wallet_hash',
        )