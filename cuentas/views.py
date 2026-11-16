from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from core.utilidades import rolRequerido
from cuentas import forms
from cuentas.models import Usuario
from experiencias.models import Experiencia, Inscripcion

# Create your views here.
class IngresoView(LoginView):
  template_name = 'cuentas/login.html'
  redirect_authenticated_user = True

  def form_valid(self, form):
    anterior = form.get_user().last_login
    respuesta = super().form_valid(form)
    self.request.session['ingreso'] = timezone.localtime().strftime('%d/%m/%Y %H:%M')
    if anterior:
      self.request.session['ultimo_acceso'] = timezone.localtime(anterior).strftime('%d/%m/%Y %H:%M')
    else:
      self.request.session['ultimo_acceso'] = 'Primer ingreso'
    return respuesta


def registro(request):
  form = forms.RegistroForm()
  if request.method == 'POST':
    form = forms.RegistroForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'Tu cuenta fue creada. Ya puedes iniciar sesión.')
      return HttpResponseRedirect(reverse('login'))
  data = {'form': form}
  return render(request, 'cuentas/registro.html', data)


@login_required(login_url='login')
def miPerfil(request):
  form = forms.MiPerfilForm(instance=request.user)
  if request.method == 'POST':
    form = forms.MiPerfilForm(request.POST, instance=request.user)
    if form.is_valid():
      form.save()
      messages.success(request, 'Tus datos fueron actualizados.')
      return HttpResponseRedirect(reverse('perfil'))
  data = {'form': form}
  return render(request, 'cuentas/perfil.html', data)


@rolRequerido('admin')
def usuarioData(request):
  usuarios = Usuario.objects.order_by('rol', 'username')
  data = {'usuarios': usuarios}
  return render(request, 'cuentas/usuarioLista.html', data)


@rolRequerido('admin')
def guiaData(request):
  guias = list(Usuario.objects.filter(rol='guia').order_by('username'))
  for guia in guias:
    experiencias = Experiencia.objects.filter(creador=guia)
    reservas = Inscripcion.objects.filter(experiencia__creador=guia)
    cupos = 0
    puntajes = []
    for reserva in reservas:
      cupos += reserva.cantidad
      if reserva.puntaje:
        puntajes.append(reserva.puntaje)
    guia.total_experiencias = experiencias.count()
    guia.proximas = experiencias.filter(fecha_hora__gte=timezone.now()).count()
    guia.total_cupos = cupos
    guia.promedio = None
    if puntajes:
      guia.promedio = round(sum(puntajes) / len(puntajes), 1)
  data = {'guias': guias}
  return render(request, 'cuentas/guiaLista.html', data)


@rolRequerido('admin')
def usuarioRegistro(request):
  inicial = {}
  if request.GET.get('rol') in ('admin', 'guia', 'turista'):
    inicial = {'rol': request.GET.get('rol')}
  form = forms.UsuarioForm(initial=inicial)
  if request.method == 'POST':
    form = forms.UsuarioForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'Usuario creado correctamente.')
      return HttpResponseRedirect(reverse('usuario_lista'))
  data = {'form': form}
  return render(request, 'cuentas/usuarioFormulario.html', data)


@rolRequerido('admin')
def editarUsuario(request, id):
  usuario = get_object_or_404(Usuario, id=id)
  form = forms.UsuarioForm(instance=usuario)
  if request.method == 'POST':
    form = forms.UsuarioForm(request.POST, instance=usuario)
    if form.is_valid():
      form.save()
      messages.success(request, 'Usuario actualizado correctamente.')
      return HttpResponseRedirect(reverse('usuario_lista'))
  data = {'form': form, 'object': usuario}
  return render(request, 'cuentas/usuarioFormulario.html', data)


@rolRequerido('admin')
def eliminarUsuario(request, id):
  usuario = get_object_or_404(Usuario, id=id)
  error = ''
  if request.method == 'POST':
    if usuario == request.user:
      error = 'No puedes eliminar tu propia cuenta.'
    else:
      usuario.delete()
      messages.success(request, 'Usuario eliminado.')
      return HttpResponseRedirect(reverse('usuario_lista'))
  data = {'object': usuario, 'error': error}
  return render(request, 'cuentas/usuarioConfirmarBorrar.html', data)
