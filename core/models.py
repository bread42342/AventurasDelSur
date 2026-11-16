import datetime

from django.db import models

# Create your models here.
class ConfiguracionEcoparque(models.Model):
  nombre = models.CharField(max_length=100, default='Aventuras del Sur')
  descripcion = models.TextField(blank=True)
  direccion = models.CharField(max_length=150, blank=True)
  telefono = models.CharField(max_length=20, blank=True)
  correo = models.EmailField(blank=True)
  horario_apertura = models.TimeField(default=datetime.time(9, 0))
  horario_cierre = models.TimeField(default=datetime.time(18, 0))
  politica_cancelacion = models.TextField(blank=True, verbose_name='Política de cancelación')

  class Meta:
    verbose_name = 'Configuración del ecoparque'

  def __str__(self):
    return self.nombre

  @classmethod
  def obtener(cls):
    configuracion, _ = cls.objects.get_or_create(pk=1)
    return configuracion
