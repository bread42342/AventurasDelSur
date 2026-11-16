import calendar
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from core.utilidades import rolRequerido
from experiencias import forms
from experiencias.models import Categoria, Experiencia, Inscripcion

# Create your views here.
@rolRequerido('admin')
def categoriaData(request):
  categorias = Categoria.objects.all()
  data = {'categorias': categorias}
  return render(request, 'experiencias/categoriaLista.html', data)


@rolRequerido('admin')
def categoriaRegistro(request):
  form = forms.CategoriaForm()
  if request.method == 'POST':
    form = forms.CategoriaForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'Categoría creada correctamente.')
      return HttpResponseRedirect(reverse('categoria_lista'))
  data = {'form': form}
  return render(request, 'experiencias/categoriaFormulario.html', data)


@rolRequerido('admin')
def editarCategoria(request, id):
  categoria = get_object_or_404(Categoria, id=id)
  form = forms.CategoriaForm(instance=categoria)
  if request.method == 'POST':
    form = forms.CategoriaForm(request.POST, instance=categoria)
    if form.is_valid():
      form.save()
      messages.success(request, 'Categoría actualizada correctamente.')
      return HttpResponseRedirect(reverse('categoria_lista'))
  data = {'form': form, 'object': categoria}
  return render(request, 'experiencias/categoriaFormulario.html', data)


@rolRequerido('admin')
def eliminarCategoria(request, id):
  categoria = get_object_or_404(Categoria, id=id)
  error = ''
  if request.method == 'POST':
    try:
      categoria.delete()
      messages.success(request, 'Categoría eliminada.')
      return HttpResponseRedirect(reverse('categoria_lista'))
    except ProtectedError:
      error = 'No se puede eliminar: hay experiencias asociadas a esta categoría. Desactívala en su lugar.'
  data = {'object': categoria, 'error': error}
  return render(request, 'experiencias/categoriaConfirmarBorrar.html', data)


def experienciasDelUsuario(request):
  if request.user.rol == 'admin':
    return Experiencia.objects.all()
  return Experiencia.objects.filter(creador=request.user)


@rolRequerido('admin', 'guia')
def experienciaData(request):
  experiencias = experienciasDelUsuario(request)
  data = {'experiencias': experiencias}
  return render(request, 'experiencias/experienciaLista.html', data)


@rolRequerido('admin', 'guia')
def experienciaRegistro(request):
  form = forms.ExperienciaForm(initial={'creador': request.user})
  if request.user.rol != 'admin':
    del form.fields['creador']
  if request.method == 'POST':
    form = forms.ExperienciaForm(request.POST)
    if request.user.rol != 'admin':
      del form.fields['creador']
    if form.is_valid():
      experiencia = form.save(commit=False)
      if request.user.rol != 'admin':
        experiencia.creador = request.user
      experiencia.save()
      messages.success(request, 'Experiencia creada correctamente.')
      return HttpResponseRedirect(reverse('experiencia_lista'))
  data = {'form': form}
  return render(request, 'experiencias/experienciaFormulario.html', data)


@rolRequerido('admin', 'guia')
def editarExperiencia(request, id):
  experiencia = get_object_or_404(experienciasDelUsuario(request), id=id)
  form = forms.ExperienciaForm(instance=experiencia)
  if request.user.rol != 'admin':
    del form.fields['creador']
  if request.method == 'POST':
    form = forms.ExperienciaForm(request.POST, instance=experiencia)
    if request.user.rol != 'admin':
      del form.fields['creador']
    if form.is_valid():
      form.save()
      messages.success(request, 'Experiencia actualizada correctamente.')
      return HttpResponseRedirect(reverse('experiencia_lista'))
  data = {'form': form, 'object': experiencia}
  return render(request, 'experiencias/experienciaFormulario.html', data)


@rolRequerido('admin')
def eliminarExperiencia(request, id):
  experiencia = get_object_or_404(Experiencia, id=id)
  if request.method == 'POST':
    experiencia.delete()
    messages.success(request, 'Experiencia eliminada.')
    return HttpResponseRedirect(reverse('experiencia_lista'))
  data = {'object': experiencia}
  return render(request, 'experiencias/experienciaConfirmarBorrar.html', data)


@login_required(login_url='login')
def catalogo(request):
  experiencias = Experiencia.objects.filter(activa=True, categoria__activo=True,
                                            estado='programada', fecha_hora__gte=timezone.now())
  reservadas = []
  for reserva in Inscripcion.objects.filter(usuario=request.user):
    reservadas.append(reserva.experiencia_id)
  data = {'experiencias': experiencias, 'reservadas': reservadas}
  return render(request, 'experiencias/catalogo.html', data)


@login_required(login_url='login')
def experienciaDetalle(request, id):
  experiencias = Experiencia.objects.all()
  if request.user.rol == 'turista':
    experiencias = experiencias.filter(activa=True, categoria__activo=True)
  experiencia = get_object_or_404(experiencias, id=id)
  vistas = []
  for vista in request.session.get('vistas_recientes', []):
    if vista != experiencia.id:
      vistas.append(vista)
  request.session['vistas_recientes'] = ([experiencia.id] + vistas)[:5]
  reserva = Inscripcion.objects.filter(usuario=request.user, experiencia=experiencia).first()
  valoraciones = experiencia.inscripciones.filter(puntaje__isnull=False)
  data = {'experiencia': experiencia, 'reserva': reserva, 'valoraciones': valoraciones,
          'promedio': experiencia.promedio_valoracion}
  return render(request, 'experiencias/experienciaDetalle.html', data)


@rolRequerido('turista')
@require_POST
def reservar(request, id):
  experiencia = get_object_or_404(Experiencia, id=id, activa=True, categoria__activo=True)
  if experiencia.estado != 'programada':
    messages.error(request, f'Esta ruta no admite reservas: está {experiencia.get_estado_display().lower()}.')
  elif experiencia.ya_paso:
    messages.error(request, 'Esta experiencia ya se realizó.')
  elif Inscripcion.objects.filter(usuario=request.user, experiencia=experiencia).exists():
    messages.warning(request, 'Ya tienes una reserva para esta experiencia.')
  elif experiencia.cupos_disponibles <= 0:
    messages.error(request, 'No quedan cupos disponibles.')
  else:
    try:
      cantidad = int(request.POST.get('cantidad', 1))
    except ValueError:
      cantidad = 0
    if cantidad < 1:
      messages.error(request, 'Indica una cantidad de cupos válida.')
    elif cantidad > experiencia.cupos_disponibles:
      messages.error(request, f'Solo quedan {experiencia.cupos_disponibles} cupos disponibles.')
    else:
      Inscripcion.objects.create(usuario=request.user, experiencia=experiencia, cantidad=cantidad)
      messages.success(request, 'Reserva registrada. Tu pago queda pendiente de confirmación.')
      return HttpResponseRedirect(reverse('mis_reservas'))
  return HttpResponseRedirect(reverse('experiencia_detalle', args=[id]))


@rolRequerido('admin')
def inscripcionData(request):
  inscripciones = Inscripcion.objects.all()
  data = {'inscripciones': inscripciones}
  return render(request, 'experiencias/inscripcionLista.html', data)


@rolRequerido('admin')
def editarInscripcion(request, id):
  inscripcion = get_object_or_404(Inscripcion, id=id)
  form = forms.InscripcionForm(instance=inscripcion)
  if request.method == 'POST':
    form = forms.InscripcionForm(request.POST, instance=inscripcion)
    if form.is_valid():
      form.save()
      messages.success(request, 'Reserva actualizada correctamente.')
      return HttpResponseRedirect(reverse('inscripcion_lista'))
  data = {'form': form, 'object': inscripcion}
  return render(request, 'experiencias/inscripcionFormulario.html', data)


@rolRequerido('admin')
def eliminarInscripcion(request, id):
  inscripcion = get_object_or_404(Inscripcion, id=id)
  if request.method == 'POST':
    inscripcion.delete()
    messages.success(request, 'Reserva eliminada.')
    return HttpResponseRedirect(reverse('inscripcion_lista'))
  data = {'object': inscripcion}
  return render(request, 'experiencias/inscripcionConfirmarBorrar.html', data)


@rolRequerido('turista')
def misReservas(request):
  reservas = Inscripcion.objects.filter(usuario=request.user)
  data = {'reservas': reservas}
  return render(request, 'experiencias/misReservas.html', data)


@rolRequerido('turista')
@require_POST
def cancelarReserva(request, id):
  reserva = get_object_or_404(Inscripcion, id=id, usuario=request.user)
  if reserva.estado_pago == 'confirmado':
    messages.error(request, 'Una reserva con pago confirmado no se puede cancelar desde aquí.')
  else:
    reserva.delete()
    messages.success(request, 'Reserva cancelada.')
  return HttpResponseRedirect(reverse('mis_reservas'))


@rolRequerido('turista')
@require_POST
def pagarReserva(request, id):
  reserva = get_object_or_404(Inscripcion, id=id, usuario=request.user)
  if reserva.estado_pago == 'confirmado':
    messages.info(request, 'Esta reserva ya está pagada.')
  elif not reserva.puede_pagar:
    messages.error(request, 'No se puede pagar: la ruta está suspendida o finalizada.')
  else:
    reserva.estado_pago = 'confirmado'
    reserva.save()
    messages.success(request, 'Pago registrado. Tu reserva quedó confirmada.')
  return HttpResponseRedirect(reverse('mis_reservas'))


@rolRequerido('turista')
def valorar(request, id):
  reserva = get_object_or_404(Inscripcion, id=id, usuario=request.user)
  if not reserva.puede_valorar:
    raise PermissionDenied
  form = forms.ValoracionForm(instance=reserva)
  if request.method == 'POST':
    form = forms.ValoracionForm(request.POST, instance=reserva)
    if form.is_valid():
      form.save()
      messages.success(request, 'Gracias por valorar tu experiencia.')
      return HttpResponseRedirect(reverse('mis_reservas'))
  data = {'form': form, 'object': reserva}
  return render(request, 'experiencias/valoracionFormulario.html', data)


MESES = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
         'Noviembre', 'Diciembre']


def experienciaDelGuia(request, id):
  experiencia = get_object_or_404(Experiencia, id=id)
  if experiencia.creador_id != request.user.id:
    raise PermissionDenied
  return experiencia


@rolRequerido('guia')
def calendario(request):
  hoy = timezone.localdate()
  try:
    anio, mes = (int(valor) for valor in request.GET.get('mes', '').split('-'))
    primero = datetime.date(anio, mes, 1)
  except ValueError:
    primero = hoy.replace(day=1)
  anterior = (primero - datetime.timedelta(days=1)).replace(day=1)
  siguiente = (primero + datetime.timedelta(days=32)).replace(day=1)
  zona = timezone.get_current_timezone()
  inicio = datetime.datetime.combine(primero, datetime.time.min, tzinfo=zona)
  fin = datetime.datetime.combine(siguiente, datetime.time.min, tzinfo=zona)
  porDia = {}
  for experiencia in Experiencia.objects.filter(creador=request.user, fecha_hora__gte=inicio, fecha_hora__lt=fin):
    dia = timezone.localtime(experiencia.fecha_hora).date()
    porDia.setdefault(dia, []).append(experiencia)
  semanas = []
  for semana in calendar.Calendar(firstweekday=0).monthdatescalendar(primero.year, primero.month):
    fila = []
    for dia in semana:
      fila.append({'fecha': dia, 'en_mes': dia.month == primero.month, 'hoy': dia == hoy,
                   'experiencias': porDia.get(dia, [])})
    semanas.append(fila)
  data = {
    'semanas': semanas,
    'titulo': f'{MESES[primero.month - 1]} {primero.year}',
    'anterior': anterior.strftime('%Y-%m'),
    'siguiente': siguiente.strftime('%Y-%m'),
    'dias_semana': ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
  }
  return render(request, 'experiencias/calendario.html', data)


@rolRequerido('guia')
def grupoDetalle(request, id):
  experiencia = experienciaDelGuia(request, id)
  inscripciones = list(experiencia.inscripciones.all())
  cupos = 0
  asistentes = 0
  confirmados = 0
  for i in inscripciones:
    cupos += i.cantidad
    asistentes += i.asistentes
    if i.estado_pago == 'confirmado':
      confirmados += i.cantidad
  data = {'experiencia': experiencia, 'inscripciones': inscripciones, 'cupos_reservados': cupos,
          'asistentes': asistentes, 'confirmados': confirmados, 'estados': experiencia.estados_siguientes}
  return render(request, 'experiencias/grupoDetalle.html', data)


@rolRequerido('guia')
@require_POST
def cambiarEstado(request, id):
  experiencia = experienciaDelGuia(request, id)
  nuevo = request.POST.get('estado')
  if nuevo in dict(experiencia.estados_siguientes):
    experiencia.estado = nuevo
    experiencia.save()
    messages.success(request, f'Estado de la ruta actualizado: {experiencia.get_estado_display()}.')
  else:
    messages.error(request, 'No se puede cambiar la ruta a ese estado.')
  return HttpResponseRedirect(reverse('grupo_detalle', args=[id]))


@rolRequerido('guia')
def visitantesRegistro(request, id):
  experiencia = experienciaDelGuia(request, id)
  puedeRegistrar = experiencia.estado in ('en_curso', 'finalizada')
  if request.method == 'POST':
    if not puedeRegistrar:
      messages.error(request, 'Inicia la ruta antes de registrar visitantes.')
      return HttpResponseRedirect(reverse('grupo_detalle', args=[id]))
    inscripciones = list(experiencia.inscripciones.all())
    valores = {}
    for inscripcion in inscripciones:
      try:
        valor = int(request.POST.get(f'asistentes_{inscripcion.id}', 0))
      except ValueError:
        valor = -1
      if valor < 0 or valor > inscripcion.cantidad:
        messages.error(request, 'Cada cantidad debe estar entre 0 y los cupos reservados.')
        data = {'experiencia': experiencia, 'inscripciones': experiencia.inscripciones.all(),
                'puede_registrar': puedeRegistrar}
        return render(request, 'experiencias/visitantesRegistro.html', data)
      valores[inscripcion.id] = valor
    for inscripcion in inscripciones:
      inscripcion.asistentes = valores[inscripcion.id]
      inscripcion.save()
    messages.success(request, 'Visitantes registrados correctamente.')
    return HttpResponseRedirect(reverse('grupo_detalle', args=[id]))
  data = {'experiencia': experiencia, 'inscripciones': experiencia.inscripciones.all(),
          'puede_registrar': puedeRegistrar}
  return render(request, 'experiencias/visitantesRegistro.html', data)
