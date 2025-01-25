from django.urls import path
from . import views

app_name = 'cajero'

urlpatterns = [
    path('', views.index, name='index'),
    path('depositos/', views.deposit, name='deposit'),
    path('retiros/', views.withdrawal, name='withdrawal'),
    path('pagos/', views.payment, name='payment'),
    path('saldo/', views.check_balance, name='check_balance'),
]