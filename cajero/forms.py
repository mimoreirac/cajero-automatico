from django import forms
from .models import Cuentas

class DepositAccountForm(forms.Form):
    cuenta_id = forms.CharField(max_length=20)
    cedula = forms.CharField(max_length=10)

class DepositAmountForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01)
