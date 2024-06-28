from django.db import models

class Empleado(models.Model):
    rpe = models.CharField(max_length=5, unique=True)
    nombre = models.CharField(max_length=100)
    adscripcion = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    nombramiento = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nombre

class InventarioEquipo(models.Model):
    MARCA_CHOICES = [
        ('HP', 'HP'),
        ('Dell', 'Dell'),
        ('Lenovo', 'Lenovo'),
    ]

    MODELO_CHOICES = [
        ('ThinkCentre', 'ThinkCentre'),
        ('HP Prodesk 600 G6', 'HP Prodesk 600 G6'),
        ('Probook 440 G7', 'Probook 440 G7'),
        ('ThinkPad', 'ThinkPad'),
    ]

    TIPO_CHOICES = [
        ('Laptop', 'Laptop'),
        ('Desktop', 'Desktop'),
    ]

    ESTADO_CHOICES = [
        ('nuevo', 'Nuevo'),
        ('usado', 'Usado'),
        ('dado de baja', 'Dado de baja'),
    ]

    UBICACION_CHOICES = [
        ('Departamento Compras', 'Departamento Compras'),
        ('Departamento Almacenes y Trafico', 'Departamento Almacenes y Trafico'),
        ('Departamento Proveedores', 'Departamento Proveedores'),
        ('Soporte Tecnico', 'Soporte Tecnico'),
        ('Auxiliaria General', 'Auxiliaria General'),
    ]

    num_serie = models.CharField(max_length=50, unique=True)
    num_inventario = models.CharField(max_length=25, default=0)
    num_activo = models.CharField(max_length=25, default=0)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    especificaciones = models.TextField(blank=True)
    fecha_adquisicion = models.DateField()
    estado = models.CharField(max_length=50, default='nuevo')
    ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=True, blank=True, null=True)
    nombre_equipo = models.CharField(max_length=100, default='Equipo Desconocido')  # Define un valor predeterminado aquí

    def __str__(self):
        return self.num_serie
    
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class AsignacionEquipo(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    equipo = models.ForeignKey(InventarioEquipo, on_delete=models.CASCADE)
    fecha_asignacion = models.DateField()
    detalles = models.TextField(blank=True)

    def clean(self):
        if AsignacionEquipo.objects.filter(equipo=self.equipo).exclude(id=self.id).exists():
            raise ValidationError(_('Este equipo ya está asignado a otro empleado.'))

    def __str__(self):
        return f"{self.empleado} - {self.equipo}"
