from django.urls import path
from . import views

urlpatterns = [
  path('', views.inicio, name='inicio'),
  path('panel/', views.panel, name='panel'),
  path('configuracion/', views.configuracion, name='configuracion'),
  path('reportes/', views.reportes, name='reportes'),
]
