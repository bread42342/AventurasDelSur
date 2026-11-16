from django.urls import path
from . import views

urlpatterns = [
  path('categorias/', views.categoriaData, name='categoria_lista'),
  path('categorias/nueva/', views.categoriaRegistro, name='categoria_crear'),
  path('categorias/<int:id>/editar/', views.editarCategoria, name='categoria_actualizar'),
  path('categorias/<int:id>/eliminar/', views.eliminarCategoria, name='categoria_borrar'),

  path('gestion/', views.experienciaData, name='experiencia_lista'),
  path('gestion/nueva/', views.experienciaRegistro, name='experiencia_crear'),
  path('gestion/<int:id>/editar/', views.editarExperiencia, name='experiencia_actualizar'),
  path('gestion/<int:id>/eliminar/', views.eliminarExperiencia, name='experiencia_borrar'),

  path('calendario/', views.calendario, name='calendario'),
  path('gestion/<int:id>/grupo/', views.grupoDetalle, name='grupo_detalle'),
  path('gestion/<int:id>/visitantes/', views.visitantesRegistro, name='visitantes_registro'),
  path('gestion/<int:id>/estado/', views.cambiarEstado, name='ruta_estado'),

  path('catalogo/', views.catalogo, name='catalogo'),
  path('<int:id>/', views.experienciaDetalle, name='experiencia_detalle'),
  path('<int:id>/reservar/', views.reservar, name='experiencia_reservar'),

  path('reservas/', views.inscripcionData, name='inscripcion_lista'),
  path('reservas/<int:id>/editar/', views.editarInscripcion, name='inscripcion_actualizar'),
  path('reservas/<int:id>/eliminar/', views.eliminarInscripcion, name='inscripcion_borrar'),

  path('mis-reservas/', views.misReservas, name='mis_reservas'),
  path('mis-reservas/<int:id>/valorar/', views.valorar, name='reserva_valorar'),
  path('mis-reservas/<int:id>/cancelar/', views.cancelarReserva, name='reserva_cancelar'),
  path('mis-reservas/<int:id>/pagar/', views.pagarReserva, name='reserva_pagar'),
]
