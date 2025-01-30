from django import forms
from .models import Cuentas, Catalogo

class DepositAccountForm(forms.Form):
    cuenta_id = forms.CharField(label='Número de Cuenta', max_length=10, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    cedula = forms.CharField(label='Cédula', max_length=10, widget=forms.TextInput(attrs={'autocomplete': 'off'}))

class DepositAmountForm(forms.Form):
    amount = forms.DecimalField(label='Monto',max_digits=12, decimal_places=2, min_value=0.01, widget=forms.TextInput(attrs={'autocomplete': 'off'}))

class WithdrawalCardForm(forms.Form):
    card_number = forms.CharField(label='Número de Tarjeta', max_length=16, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    pin = forms.CharField(label='PIN', max_length=4, widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))

class WithdrawalAmountForm(forms.Form):
    amount = forms.DecimalField(label='Monto a Retirar', max_digits=12, decimal_places=2, min_value=0.01, widget=forms.TextInput(attrs={'autocomplete': 'off'}))

class PaymentServiceForm(forms.Form):
    SERVICIO_CHOICES = [
        (9, 'Agua'),
        (10, 'Luz'),
        (11, 'Internet'),
    ]
    servicio = forms.ChoiceField(label='Servicio a Pagar', choices=SERVICIO_CHOICES, widget=forms.Select)
    cedula = forms.CharField(label='Cédula', max_length=10, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    cuenta_id = forms.CharField(label='Número de Cuenta', max_length=10, widget=forms.TextInput(attrs={'autocomplete': 'off'}))

class PaymentAmountForm(forms.Form):
    amount = forms.DecimalField(label='Monto a Pagar', max_digits=12, decimal_places=2, min_value=0.01, widget=forms.TextInput(attrs={'autocomplete': 'off'}))

class CheckBalanceForm(forms.Form):
    card_number = forms.CharField(label='Número de Tarjeta', max_length=16, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    pin = forms.CharField(label='PIN', max_length=4, widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))