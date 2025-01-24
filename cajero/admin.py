from django.contrib import admin
from .models import Catalogo, Clientes, Cuentas, Tarjetas, Transacciones

# Register your models here.
@admin.register(Catalogo)
@admin.register(Clientes)
@admin.register(Cuentas)
@admin.register(Tarjetas)
@admin.register(Transacciones)

class CatalogoAdmin(admin.ModelAdmin):
    pass

class ClientesAdmin(admin.ModelAdmin):
    pass

class CuentasAdmin(admin.ModelAdmin):
    pass

class TarjetasAdmin(admin.ModelAdmin):
    pass

class TransaccionesAdmin(admin.ModelAdmin):
    pass