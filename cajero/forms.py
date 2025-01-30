from django import forms
from .models import Cuentas

class DepositAccountForm(forms.Form):
    cuenta_id = forms.CharField(label='Número de Cuenta', max_length=20, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    cedula = forms.CharField(label='Cédula', max_length=10, widget=forms.TextInput(attrs={'autocomplete': 'off'}))

class DepositAmountForm(forms.Form):
    amount = forms.DecimalField(label='Monto',max_digits=12, decimal_places=2, min_value=0.01, widget=forms.TextInput(attrs={'autocomplete': 'off'}))

class WithdrawalCardForm(forms.Form):
    card_number = forms.CharField(label='Número de Tarjeta', max_length=16, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    pin = forms.CharField(label='PIN', max_length=4, widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))

class WithdrawalAmountForm(forms.Form):
    amount = forms.DecimalField(label='Monto a Retirar', max_digits=12, decimal_places=2, min_value=0.01, widget=forms.TextInput(attrs={'autocomplete': 'off'}))