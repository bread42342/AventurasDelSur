from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class Categoria(models.Model):
  nombre = models.CharField(max_length=80, unique=True)
  descripcion = models.TextField(blank=True)
  activo = models.BooleanField(default=True)

  class Meta:
    ordering = ['nombre']

  def __str__(self):
    return self.nombre


class Experiencia(models.Model):
  ESTADO_CHOICES = (
    ('programada', 'Programada'),
    ('en_curso', 'En curso'),
    ('finalizada', 'Finalizada'),
    ('suspendida', 'Suspendida'),
  )
  TRANSICIONES = {
    'programada': ['en_curso', 'suspendida', 'finalizada'],
    'en_curso': ['finalizada', 'suspendida'],
    'suspendida': ['programada'],
    'finalizada': [],
  }

  titulo = models.CharField(max_length=150)
  descripcion = models.TextField()
  precio = models.PositiveIntegerField(help_text='Precio por persona en pesos chilenos.')
  cupo_maximo = models.PositiveIntegerField(default=10)
  fecha_hora = models.DateTimeField(verbose_name='Fecha y hora')
  categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='experiencias')
  creador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                related_name='experiencias_creadas')
  activa = models.BooleanField(default=True)
  estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='programada', verbose_name='Estado de la ruta')

  class Meta:
    ordering = ['fecha_hora']

  def __str__(self):
    return self.titulo

  @property
  def inscritos(self):
    total = 0
    for inscripcion in self.inscripciones.all():
      total += inscripcion.cantidad
    return total

  @property
  def cupos_disponibles(self):
    return max(self.cupo_maximo - self.inscritos, 0)

  @property
  def ya_paso(self):
    return self.fecha_hora < timezone.now()

  @property
  def estados_siguientes(self):
    permitidos = self.TRANSICIONES[self.estado]
    if self.estado == 'programada' and not self.ya_paso:
      permitidos = ['suspendida']
    return [e for e in self.ESTADO_CHOICES if e[0] in permitidos]

  @property
  def promedio_valoracion(self):
    puntajes = [i.puntaje for i in self.inscripciones.all() if i.puntaje]
    if puntajes:
      return sum(puntajes) / len(puntajes)
    return None


class Inscripcion(models.Model):
  ESTADO_PAGO_CHOICES = (('pendiente', 'Pendiente'), ('confirmado', 'Confirmado'))

  usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inscripciones')
  experiencia = models.ForeignKey(Experiencia, on_delete=models.CASCADE, related_name='inscripciones')
  PUNTAJE_CHOICES = [(i, f'{i} de 5') for i in range(1, 6)]

  cantidad = models.PositiveIntegerField(default=1, verbose_name='Cupos reservados')
  asistentes = models.PositiveIntegerField(default=0, verbose_name='Visitantes presentes')
  puntaje = models.PositiveSmallIntegerField(null=True, blank=True, choices=PUNTAJE_CHOICES)
  fecha_inscripcion = models.DateTimeField(auto_now_add=True)
  estado_pago = models.CharField(max_length=15, choices=ESTADO_PAGO_CHOICES, default='pendiente')

  class Meta:
    ordering = ['-fecha_inscripcion', '-id']
    unique_together = ('usuario', 'experiencia')
    verbose_name = 'Reserva'

  @property
  def puede_valorar(self):
    return self.estado_pago == 'confirmado' and self.experiencia.estado == 'finalizada'

  @property
  def puede_pagar(self):
    return self.estado_pago == 'pendiente' and self.experiencia.estado in ('programada', 'en_curso')

  @property
  def total(self):
    return self.cantidad * self.experiencia.precio

  def __str__(self):
    return f"{self.usuario.username} - {self.experiencia.titulo}"
