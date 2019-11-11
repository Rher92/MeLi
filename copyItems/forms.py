from django import forms
from django.contrib import admin

from .models import Account

class CopyForm(forms.Form):
    from_account = forms.CharField(max_length=30)
    to_account = forms.CharField(max_length=30)

    def clean(self):
        cleaned_data = super(CopyForm, self).clean()
        from_account = cleaned_data.get('from_account')
        to_account = cleaned_data.get('to_account')

        accounts = [from_account, to_account]
        for account in accounts:
            if not Account.objects.filter(name=account):
                raise forms.ValidationError('No existe la cuenta con el nombre:{}'.format(account))  
        if to_account == to_account:
            raise forms.ValidationError('Verificar las cuentas, NO se puede copiar la misma cuenta')

        
class UpdateForm(forms.Form):
    account = forms.CharField(max_length=30)

    def clean(self):
        cleaned_data = super(UpdateForm, self).clean()
        account = cleaned_data.get('account')

        if not Account.objects.filter(name=account):
            raise forms.ValidationError('No existe la cuenta con el nombre:{}'.format(account))  