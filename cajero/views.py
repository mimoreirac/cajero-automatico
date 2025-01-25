from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    return render(request, 'index.html')

def deposit(request):
    return render(request, 'depositos.html')

def withdrawal(request):
    return render(request, 'retiros.html')

def payment(request):
    return render(request, 'pagos.html')

def check_balance(request):
    return render(request, 'saldo.html')