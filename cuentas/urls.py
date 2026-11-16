from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
  path('ingresar/', views.IngresoView.as_view(), name='login'),
  path('salir/', LogoutView.as_view(), name='logout'),
  path('registro/', views.registro, name='registro'),
  path('perfil/', views.miPerfil, name='perfil'),
  path('usuarios/', views.usuarioData, name='usuario_lista'),
  path('guias/', views.guiaData, name='guia_lista'),
  path('usuarios/nuevo/', views.usuarioRegistro, name='usuario_crear'),
  path('usuarios/<int:id>/editar/', views.editarUsuario, name='usuario_actualizar'),
  path('usuarios/<int:id>/eliminar/', views.eliminarUsuario, name='usuario_borrar'),
]
