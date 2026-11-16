from django import forms
from django.db.models import Q
from core.utilidades import estiloBootstrap
from experiencias.models import Categoria, Experiencia, Inscripcion


class CategoriaForm(forms.ModelForm):
  class Meta:
    model = Categoria
    fields = ['nombre', 'descripcion', 'activo']
    widgets = {'descripcion': forms.Textarea(attrs={'rows': 3})}

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    estiloBootstrap(self)


class ExperienciaForm(forms.ModelForm):
  class Meta:
    model = Experiencia
    fields = ['titulo', 'descripcion', 'categoria', 'precio', 'cupo_maximo', 'fecha_hora', 'activa', 'creador']
    widgets = {
      'descripcion': forms.Textarea(attrs={'rows': 4}),
      'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['categoria'].queryset = Categoria.objects.filter(
      Q(activo=True) | Q(pk=self.instance.categoria_id))
    self.fields['creador'].queryset = self.fields['creador'].queryset.filter(rol__in=['admin', 'guia'])
    self.fields['creador'].required = True
    estiloBootstrap(self)


class ValoracionForm(forms.ModelForm):
  class Meta:
    model = Inscripcion
    fields = ['puntaje']

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['puntaje'].choices = Inscripcion.PUNTAJE_CHOICES
    self.fields['puntaje'].required = True
    estiloBootstrap(self)


class InscripcionForm(forms.ModelForm):
  class Meta:
    model = Inscripcion
    fields = ['cantidad', 'estado_pago']

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    estiloBootstrap(self)

  def clean_cantidad(self):
    cantidad = self.cleaned_data['cantidad']
    experiencia = self.instance.experiencia
    otros = experiencia.inscritos - self.instance.cantidad
    if cantidad < 1:
      raise forms.ValidationError('Indica una cantidad de cupos válida.')
    if otros + cantidad > experiencia.cupo_maximo:
      raise forms.ValidationError('Supera el cupo máximo de la experiencia.')
    return cantidad
