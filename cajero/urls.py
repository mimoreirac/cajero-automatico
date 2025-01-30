from django.urls import path
from . import views

app_name = 'cajero'

urlpatterns = [
    path('', views.index, name='index'),
    path('depositos/', views.deposit, name='deposit'),
    path('depositos/confirmar/', views.confirm_deposit, name='confirm_deposit'),
    path('retiros/', views.withdrawal, name='withdrawal'),
    path('retiros/confirmar/', views.confirm_withdrawal, name='confirm_withdrawal'),
    path('pagos/', views.payment, name='payment'),
    path('saldo/', views.check_balance, name='check_balance'),
]