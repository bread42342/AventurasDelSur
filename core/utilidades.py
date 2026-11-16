import re
from functools import wraps
from django import forms
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


def rolRequerido(*roles):
  def decorador(vista):
    @wraps(vista)
    def envoltura(request, *args, **kwargs):
      if not request.user.is_authenticated:
        return redirect_to_login(request.get_full_path())
      if request.user.rol not in roles:
        raise PermissionDenied
      return vista(request, *args, **kwargs)
    return envoltura
  return decorador


def estiloBootstrap(form):
  for campo in form.fields.values():
    if isinstance(campo.widget, forms.CheckboxInput):
      campo.widget.attrs['class'] = 'custom-control-input'
    else:
      campo.widget.attrs['class'] = 'form-control'


def validarCelular(valor):
  numero = re.sub(r'[\s\-()]', '', valor or '')
  if not numero:
    return ''
  coincidencia = re.fullmatch(r'(?:\+?56)?(9\d{8})', numero)
  if not coincidencia:
    raise forms.ValidationError('Ingresa un celular chileno válido: +56 9 XXXX XXXX.')
  return '+56' + coincidencia.group(1)
