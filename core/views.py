from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from core.forms import ConfiguracionForm
from core.models import ConfiguracionEcoparque
from core.utilidades import rolRequerido
from cuentas.models import Usuario
from experiencias.models import Categoria, Experiencia, Inscripcion

# Create your views here.
def inicio(request):
  destacadas = Experiencia.objects.filter(activa=True, categoria__activo=True,
                                          fecha_hora__gte=timezone.now(), estado='programada')[:6]
  categorias = Categoria.objects.filter(activo=True)
  data = {'destacadas': destacadas, 'categorias': categorias,
          'configuracion': ConfiguracionEcoparque.obtener()}
  return render(request, 'core/inicio.html', data)


@login_required(login_url='login')
def panel(request):
  usuario = request.user
  ahora = timezone.now()
  data = {}
  if usuario.rol == 'admin':
    data['total_usuarios'] = Usuario.objects.count()
    data['total_guias'] = Usuario.objects.filter(rol='guia').count()
    data['total_turistas'] = Usuario.objects.filter(rol='turista').count()
    data['total_categorias'] = Categoria.objects.count()
    data['total_experiencias'] = Experiencia.objects.count()
    data['total_reservas'] = Inscripcion.objects.count()
    data['reservas_pendientes'] = Inscripcion.objects.filter(estado_pago='pendiente').count()
    data['proximas'] = Experiencia.objects.filter(fecha_hora__gte=ahora).exclude(
      estado__in=['finalizada', 'suspendida'])[:5]
  elif usuario.rol == 'guia':
    propias = Experiencia.objects.filter(creador=usuario)
    data['total_experiencias'] = propias.count()
    data['experiencias_activas'] = propias.filter(activa=True).count()
    data['total_inscritos'] = Inscripcion.objects.filter(experiencia__creador=usuario).count()
    data['inscritos_pendientes'] = Inscripcion.objects.filter(
      experiencia__creador=usuario, estado_pago='pendiente').count()
    data['proximas'] = propias.filter(fecha_hora__gte=ahora).exclude(
      estado__in=['finalizada', 'suspendida'])[:5]
  else:
    reservas = Inscripcion.objects.filter(usuario=usuario)
    data['total_reservas'] = reservas.count()
    data['reservas_pendientes'] = reservas.filter(estado_pago='pendiente').count()
    data['reservas_confirmadas'] = reservas.filter(estado_pago='confirmado').count()
    vistas = []
    for id in request.session.get('vistas_recientes', []):
      for experiencia in Experiencia.objects.filter(id=id):
        vistas.append(experiencia)
    data['vistas_recientes'] = vistas
  return render(request, 'core/panel.html', data)


@rolRequerido('admin')
def configuracion(request):
  config = ConfiguracionEcoparque.obtener()
  form = ConfiguracionForm(instance=config)
  if request.method == 'POST':
    form = ConfiguracionForm(request.POST, instance=config)
    if form.is_valid():
      form.save()
      messages.success(request, 'Configuración del ecoparque actualizada.')
      return HttpResponseRedirect(reverse('configuracion'))
  data = {'form': form, 'object': config}
  return render(request, 'core/configuracion.html', data)


@rolRequerido('admin')
def reportes(request):
  reservas = Inscripcion.objects.all()
  totalCupos = 0
  totalAsistentes = 0
  ingresosConfirmados = 0
  ingresosPendientes = 0
  puntajes = []
  for reserva in reservas:
    totalCupos += reserva.cantidad
    totalAsistentes += reserva.asistentes
    if reserva.estado_pago == 'confirmado':
      ingresosConfirmados += reserva.total
    else:
      ingresosPendientes += reserva.total
    if reserva.puntaje:
      puntajes.append(reserva.puntaje)

  porExperiencia = []
  for experiencia in Experiencia.objects.all():
    lista = Inscripcion.objects.filter(experiencia=experiencia)
    cupos = 0
    asistentes = 0
    ingresos = 0
    puntos = []
    for r in lista:
      cupos += r.cantidad
      asistentes += r.asistentes
      if r.estado_pago == 'confirmado':
        ingresos += r.total
      if r.puntaje:
        puntos.append(r.puntaje)
    ocupacion = 0
    if experiencia.cupo_maximo:
      ocupacion = round(cupos * 100 / experiencia.cupo_maximo)
    promedio = None
    if puntos:
      promedio = round(sum(puntos) / len(puntos), 1)
    porExperiencia.append({'experiencia': experiencia, 'cupos': cupos, 'ocupacion': ocupacion,
                           'asistentes': asistentes, 'ingresos': ingresos, 'promedio': promedio})

  porCategoria = []
  for categoria in Categoria.objects.all():
    cantidad = 0
    cupos = 0
    ingresos = 0
    for fila in porExperiencia:
      if fila['experiencia'].categoria_id == categoria.id:
        cantidad += 1
        cupos += fila['cupos']
        ingresos += fila['ingresos']
    porCategoria.append({'categoria': categoria, 'experiencias': cantidad,
                         'cupos': cupos, 'ingresos': ingresos})

  promedioGeneral = None
  if puntajes:
    promedioGeneral = sum(puntajes) / len(puntajes)
  data = {
    'total_usuarios': Usuario.objects.count(),
    'total_guias': Usuario.objects.filter(rol='guia').count(),
    'total_turistas': Usuario.objects.filter(rol='turista').count(),
    'total_experiencias': Experiencia.objects.count(),
    'total_reservas': reservas.count(),
    'total_cupos': totalCupos,
    'total_asistentes': totalAsistentes,
    'ingresos_confirmados': ingresosConfirmados,
    'ingresos_pendientes': ingresosPendientes,
    'total_valoraciones': len(puntajes),
    'promedio_general': promedioGeneral,
    'por_experiencia': porExperiencia,
    'por_categoria': porCategoria,
  }
  return render(request, 'core/reportes.html', data)
