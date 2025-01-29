# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Max

class AccountNumberSequence:
    @staticmethod
    def get_next_account_number():
        # Get the latest account number from the database
        latest = Cuentas.objects.aggregate(Max('numero_cuenta'))['numero_cuenta__max']
        if not latest:
            # If no accounts exist, start with 0100000001
            return '0100000001'
        
        # Extract the numeric part and increment
        numeric_part = int(latest[2:]) + 1
        # Format back to 10 digits (2 digit prefix + 8 digit number)
        return f'01{numeric_part:08d}'

def validate_cedula(cedula):
    """
    Valida el número de cédula

    Args:
        cedula: String.

    Returns:
        True si la cédula es válida, False de otra manera.

    Raises:
        ValidationError: Si la cédula no es un string de 10 dígitos.
    """
    if not isinstance(cedula, str) or not cedula.isdigit() or len(cedula) != 10:
        raise ValidationError("La cédula debe ser un número de 10 dígitos.")

    sum_even = 0
    sum_odd = 0
    check_digit = int(cedula[9])

    for i in range(9):
        digit = int(cedula[i])
        if (i + 1) % 2 == 0:
            sum_even += digit
        else:
            temp = digit * 2
            if temp > 9:
                temp -= 9
            sum_odd += temp

    calculated_check = ((sum_odd + sum_even) // 10 + 1) * 10 - (sum_odd + sum_even)
    if calculated_check == 10:
        calculated_check = 0

    return calculated_check == check_digit

class Catalogo(models.Model):
    catalogo_id = models.AutoField(primary_key=True)
    nombre_catalogo = models.CharField(unique=True, max_length=100, blank=True, null=True)
    nombre_item = models.CharField(unique=True, max_length=100, blank=True, null=True)
    raiz = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catalogo'

    def __str__(self):
        return f"{self.nombre_catalogo}" if self.nombre_catalogo else f"{self.nombre_item}"
    


class Clientes(models.Model):
    client_id = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=100, blank=True, null=True)
    cedula = models.CharField(unique=True, max_length=10)

    class Meta:
        managed = False
        db_table = 'clientes'

    def clean(self):
        if not validate_cedula(self.cedula):
            raise ValidationError({'cedula': "Cédula inválida."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
    


class Cuentas(models.Model):
    cuenta_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Clientes, models.DO_NOTHING, blank=True, null=True)
    tipo_cuenta = models.ForeignKey(Catalogo, models.DO_NOTHING, db_column='tipo_cuenta', blank=True, null=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    numero_cuenta = models.CharField(unique=True, max_length=10, blank=True,  # Allow blank in forms
        default=AccountNumberSequence.get_next_account_number)
    
    class Meta:
        managed = False
        db_table = 'cuentas'

    def __str__(self):
        return f"Account {self.numero_cuenta}" if self.numero_cuenta else f"Account {self.cuenta_id}"
    
    def save(self, *args, **kwargs):
        if not self.numero_cuenta:
            self.numero_cuenta = AccountNumberSequence.get_next_account_number()
        super().save(*args, **kwargs)
    


class Tarjetas(models.Model):
    tarjeta_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Clientes, models.DO_NOTHING, blank=True, null=True)
    cuenta = models.ForeignKey(Cuentas, models.DO_NOTHING, blank=True, null=True)
    pin = models.CharField(max_length=4)
    pin_cambiado = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tarjetas'

    def __str__(self):
        return self.tarjeta_id
    


class Transacciones(models.Model):
    transaccion_id = models.AutoField(primary_key=True)
    cuenta = models.ForeignKey(Cuentas, models.DO_NOTHING, blank=True, null=True)
    tipo_transaccion = models.ForeignKey(Catalogo, models.DO_NOTHING, db_column='tipo_transaccion', blank=True, null=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    hora = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transacciones'

    def __str__(self):
        return f"{self.tipo_transaccion} por {self.monto}"
    
