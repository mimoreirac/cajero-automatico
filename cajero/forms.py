from django import forms
from .models import Cuentas

class DepositAccountForm(forms.Form):
    cuenta_id = forms.CharField(label='Número de Cuenta', max_length=20, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    cedula = forms.CharField(label='Cédula', max_length=10, widget=forms.TextInput(attrs={'autocomplete': 'off'}))

class DepositAmountForm(forms.Form):
    amount = forms.DecimalField(label='Monto',max_digits=12, decimal_places=2, min_value=0.01, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
