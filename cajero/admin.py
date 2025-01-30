from django.contrib import admin
from django import forms
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator
from .models import Catalogo, Clientes, Cuentas, Tarjetas, Transacciones

# Register your models here.
@admin.register(Catalogo)
class CatalogoAdmin(admin.ModelAdmin):
    pass

@admin.register(Clientes)
class ClientesAdmin(admin.ModelAdmin):
    pass

@admin.register(Cuentas)
class CuentasAdmin(admin.ModelAdmin):
    pass

class TarjetasAdminForm(forms.ModelForm):
    pin = forms.CharField(
        widget=forms.PasswordInput(render_value=True),  # Mask input
        min_length=4,
        max_length=4,
        validators=[RegexValidator(r'^\d{4}$', 'The PIN must be exactly 4 digits.')],
        help_text="Enter a 4-digit PIN."
    )

    class Meta:
        model = Tarjetas
        fields = '__all__'

    def clean_pin(self):
        """Ensure the PIN is exactly 4 digits before hashing."""
        pin = self.cleaned_data.get("pin")
        if not pin.isdigit():
            raise forms.ValidationError("The PIN must be exactly 4 numeric digits.")
        return make_password(pin)  # Hash the PIN before saving

@admin.register(Tarjetas)
class TarjetasAdmin(admin.ModelAdmin):
    form = TarjetasAdminForm
    list_display = ('numero_tarjeta', 'client', 'cuenta', 'pin_cambiado')

@admin.register(Transacciones)
class TransaccionesAdmin(admin.ModelAdmin):
    pass