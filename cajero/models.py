# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Catalogo(models.Model):
    catalogo_id = models.AutoField(primary_key=True)
    nombre_catalogo = models.CharField(unique=True, max_length=100, blank=True, null=True)
    nombre_item = models.CharField(unique=True, max_length=100, blank=True, null=True)
    raiz = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catalogo'


class Clientes(models.Model):
    client_id = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=100, blank=True, null=True)
    cedula = models.CharField(unique=True, max_length=10)

    class Meta:
        managed = False
        db_table = 'clientes'


class Cuentas(models.Model):
    cuenta_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Clientes, models.DO_NOTHING, blank=True, null=True)
    tipo_cuenta = models.ForeignKey(Catalogo, models.DO_NOTHING, db_column='tipo_cuenta', blank=True, null=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cuentas'


class Tarjetas(models.Model):
    tarjeta_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Clientes, models.DO_NOTHING, blank=True, null=True)
    cuenta = models.ForeignKey(Cuentas, models.DO_NOTHING, blank=True, null=True)
    pin = models.CharField(max_length=4)
    pin_cambiado = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tarjetas'


class Transacciones(models.Model):
    transaccion_id = models.AutoField(primary_key=True)
    cuenta = models.ForeignKey(Cuentas, models.DO_NOTHING, blank=True, null=True)
    tipo_transaccion = models.ForeignKey(Catalogo, models.DO_NOTHING, db_column='tipo_transaccion', blank=True, null=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    hora = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transacciones'
