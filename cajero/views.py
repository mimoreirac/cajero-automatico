from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.db import connection
from .forms import DepositAccountForm, DepositAmountForm
from .models import Cuentas, Clientes

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
    return render(request, 'retiros.html')

def payment(request):
    return render(request, 'pagos.html')

def check_balance(request):
    return render(request, 'saldo.html')