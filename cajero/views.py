from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.db import connection, transaction
from django.urls import reverse
from django.contrib import messages
from .forms import DepositAccountForm, DepositAmountForm, WithdrawalCardForm, WithdrawalAmountForm, PaymentServiceForm, PaymentAmountForm
from .models import Cuentas, Clientes, Tarjetas, Catalogo

# Create your views here.
def index(request):
    return render(request, 'index.html')

def deposit(request):
    if request.method == 'POST':
        form = DepositAccountForm(request.POST)
        if form.is_valid():
            cuenta_id = form.cleaned_data['cuenta_id']
            cedula = form.cleaned_data['cedula']

            # Validamos que la cuenta y la cedula coincidan
            try:
                cuenta = Cuentas.objects.get(numero_cuenta=cuenta_id)
                cliente = Clientes.objects.get(cedula=cedula)
                if cuenta.client.client_id == cliente.client_id:
                    # Si coinciden, proceder a la pagina de confirmacion
                    request.session['cuenta_id'] = cuenta_id
                    request.session['cedula'] = cedula
                    return redirect('cajero:confirm_deposit')
                else:
                    form.add_error(None, 'Los datos son incorrectos.')
            except Cuentas.DoesNotExist:
                form.add_error('cuenta_id', 'La cuenta no existe.')
            except Clientes.DoesNotExist:
                form.add_error('cedula', 'Cedula no existe.')

    else:
        form = DepositAccountForm()

    return render(request, 'depositos.html', {'form': form})

@transaction.atomic
def confirm_deposit(request):
    cuenta_id = request.session.get('cuenta_id')
    cedula = request.session.get('cedula')

    if not cuenta_id or not cedula:
        # Regresa a la pagina de depositos si los datos no existen
        return redirect('cajero:deposit')

    if request.method == 'POST':
        form = DepositAmountForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            cuenta = Cuentas.objects.get(numero_cuenta=cuenta_id)

            with connection.cursor() as cursor:
                cursor.execute('CALL deposito(%s, %s);', [cuenta.cuenta_id, amount]) # Usa el procedure de la base de datos

            del request.session['cuenta_id']
            del request.session['cedula']
            return redirect('cajero:index')  # Necesito una pagina de transaccion exitosa.

    else:
        form = DepositAmountForm()

    return render(request, 'deposito_confirmar.html', {'form': form, 'cuenta_id': cuenta_id, 'cedula': cedula})


def withdrawal(request):
    if request.method == 'POST':
        form = WithdrawalCardForm(request.POST)
        if form.is_valid():
            card_number = form.cleaned_data['card_number']
            pin = form.cleaned_data['pin']

            # Validar tarjeta y PIN
            try:
                tarjeta = Tarjetas.objects.get(numero_tarjeta=card_number)
                if tarjeta.check_pin(pin):
                    # Si el PIN es correcto, procede al retiro
                    request.session['card_number'] = card_number
                    return redirect('cajero:confirm_withdrawal')
                else:
                    form.add_error('pin', 'PIN incorrecto.')
            except Tarjetas.DoesNotExist:
                form.add_error('card_number', 'La tarjeta no existe.')
    else:
        form = WithdrawalCardForm()

    return render(request, 'retiros.html', {'form': form})

@transaction.atomic
def confirm_withdrawal(request):
    card_number = request.session.get('card_number')

    if not card_number:
        return redirect('cajero:withdrawal')

    if request.method == 'POST':
        form = WithdrawalAmountForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            tarjeta = Tarjetas.objects.get(numero_tarjeta=card_number)

            try:
                with connection.cursor() as cursor:
                    cursor.execute('CALL retiro(%s, %s);', [tarjeta.tarjeta_id, amount])
            except Exception as e:
                messages.error(request, str(e))
                return render(request, 'retiro_confirmar.html', {'form': form, 'card_number': card_number})

            del request.session['card_number']
            return redirect('cajero:index')  # Redirect to success page or index

    else:
        form = WithdrawalAmountForm()

    return render(request, 'retiro_confirmar.html', {'form': form, 'card_number': card_number})

def payment(request):
    if request.method == 'POST':
        form = PaymentServiceForm(request.POST)
        if form.is_valid():
            servicio = form.cleaned_data['servicio']
            cedula = form.cleaned_data['cedula']
            cuenta_id = form.cleaned_data['cuenta_id']

            # Validar cedula y cuenta
            try:
                cuenta = Cuentas.objects.get(numero_cuenta=cuenta_id)
                cliente = Clientes.objects.get(cedula=cedula)
                if cuenta.client.client_id == cliente.client_id:
                    # Guardar datos en la sesion y proceder a confirmar
                    request.session['servicio'] = servicio
                    request.session['cedula'] = cedula
                    request.session['cuenta_id'] = cuenta_id
                    return redirect('cajero:confirm_payment')
                else:
                    form.add_error(None, 'Los datos son incorrectos.')
            except Cuentas.DoesNotExist:
                form.add_error('cuenta_id', 'La cuenta no existe.')
            except Clientes.DoesNotExist:
                form.add_error('cedula', 'Cédula no existe.')
    else:
        form = PaymentServiceForm()

    return render(request, 'pagos.html', {'form': form})

@transaction.atomic
def confirm_payment(request):
    servicio = request.session.get('servicio')
    cedula = request.session.get('cedula')
    cuenta_id = request.session.get('cuenta_id')

    if not servicio or not cedula or not cuenta_id:
        return redirect('cajero:payment')

    if request.method == 'POST':
        form = PaymentAmountForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            cuenta = Cuentas.objects.get(numero_cuenta=cuenta_id)

            try:
                with connection.cursor() as cursor:
                    cursor.execute('CALL pagos(%s, %s, %s);', 
                                 [cuenta.cuenta_id, int(servicio), amount])
                    
                del request.session['servicio']
                del request.session['cedula']
                del request.session['cuenta_id']
                return redirect('cajero:index')
                
            except Exception as e:
                messages.error(request, f'Error en la transacción: {str(e)}')
                servicio_nombre = dict(PaymentServiceForm.SERVICIO_CHOICES).get(int(servicio))
                return render(request, 'pago_confirmar.html', {
                    'form': form, 
                    'servicio_nombre': servicio_nombre, 
                    'cedula': cedula, 
                    'cuenta_id': cuenta_id
                })

    else:
        form = PaymentAmountForm()
    
    servicio_nombre = dict(PaymentServiceForm.SERVICIO_CHOICES).get(int(servicio))
    return render(request, 'pago_confirmar.html', {
        'form': form, 
        'servicio_nombre': servicio_nombre, 
        'cedula': cedula, 
        'cuenta_id': cuenta_id
    })

def check_balance(request):
    return render(request, 'saldo.html')