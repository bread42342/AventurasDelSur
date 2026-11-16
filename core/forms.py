from django import forms
from core.models import ConfiguracionEcoparque
from core.utilidades import estiloBootstrap, validarCelular


class ConfiguracionForm(forms.ModelForm):
  class Meta:
    model = ConfiguracionEcoparque
    fields = ['nombre', 'descripcion', 'direccion', 'telefono', 'correo',
              'horario_apertura', 'horario_cierre', 'politica_cancelacion']
    widgets = {
      'descripcion': forms.Textarea(attrs={'rows': 3}),
      'politica_cancelacion': forms.Textarea(attrs={'rows': 3}),
      'horario_apertura': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
      'horario_cierre': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
      'telefono': forms.TextInput(attrs={'placeholder': '+56 9 XXXX XXXX'}),
    }

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    estiloBootstrap(self)

  def clean_telefono(self):
    return validarCelular(self.cleaned_data['telefono'])

  def clean(self):
    datos = super().clean()
    apertura = datos.get('horario_apertura')
    cierre = datos.get('horario_cierre')
    if apertura and cierre and cierre <= apertura:
      self.add_error('horario_cierre', 'El cierre debe ser posterior a la apertura.')
    return datos
