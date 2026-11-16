from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Usuario(AbstractUser):
  ROLES_CHOICES = (
    ('admin', 'Administrador'),
    ('guia', 'Guía / Operador'),
    ('turista', 'Turista / Cliente'),
  )

  rol = models.CharField(max_length=20, choices=ROLES_CHOICES, default='turista')

  def __str__(self):
    return f"{self.get_full_name() or self.username} ({self.get_rol_display()})"


class Perfil(models.Model):
  usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil')
  telefono = models.CharField(max_length=20, blank=True)
  documento = models.CharField(max_length=20, blank=True, verbose_name='RUT / Documento')
  ciudad = models.CharField(max_length=80, blank=True)

  def __str__(self):
    return f"Perfil de {self.usuario.username}"
