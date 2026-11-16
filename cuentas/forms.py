from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.utilidades import estiloBootstrap, validarCelular
from cuentas.models import Perfil, Usuario


def cargarPerfil(form, usuario):
  perfil = Perfil.objects.filter(usuario=usuario).first()
  if perfil:
    form.initial.update(telefono=perfil.telefono, documento=perfil.documento, ciudad=perfil.ciudad)


def guardarPerfil(form, usuario):
  perfil, creado = Perfil.objects.get_or_create(usuario=usuario)
  perfil.telefono = form.cleaned_data['telefono']
  perfil.documento = form.cleaned_data['documento']
  perfil.ciudad = form.cleaned_data['ciudad']
  perfil.save()


class RegistroForm(UserCreationForm):
  telefono = forms.CharField(label='Teléfono', max_length=20, required=False,
                             widget=forms.TextInput(attrs={'placeholder': '+56 9 XXXX XXXX'}))
  documento = forms.CharField(label='RUT / Documento', max_length=20, required=False)
  ciudad = forms.CharField(label='Ciudad', max_length=80, required=False,
                           widget=forms.TextInput(attrs={'autocomplete': 'off'}))

  class Meta(UserCreationForm.Meta):
    model = Usuario
    fields = ('username', 'first_name', 'last_name', 'email')

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for campo in ('first_name', 'last_name', 'email'):
      self.fields[campo].required = True
    estiloBootstrap(self)

  def clean_telefono(self):
    return validarCelular(self.cleaned_data['telefono'])

  def save(self, commit=True):
    usuario = super().save(commit=False)
    usuario.rol = 'turista'
    usuario.save()
    guardarPerfil(self, usuario)
    return usuario


class UsuarioForm(forms.ModelForm):
  telefono = forms.CharField(label='Teléfono', max_length=20, required=False,
                             widget=forms.TextInput(attrs={'placeholder': '+56 9 XXXX XXXX'}))
  documento = forms.CharField(label='RUT / Documento', max_length=20, required=False)
  ciudad = forms.CharField(label='Ciudad', max_length=80, required=False,
                           widget=forms.TextInput(attrs={'autocomplete': 'off'}))
  password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput, required=False)
  password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput, required=False)

  class Meta:
    model = Usuario
    fields = ['username', 'first_name', 'last_name', 'email', 'rol', 'is_active']
    labels = {'is_active': 'Cuenta activa'}

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['first_name'].required = True
    self.fields['last_name'].required = True
    self.fields['email'].required = True
    if self.instance.pk:
      cargarPerfil(self, self.instance)
      self.fields['password1'].help_text = 'Déjala en blanco para no cambiar la contraseña.'
    self.order_fields(['username', 'first_name', 'last_name', 'email', 'rol', 'telefono',
                       'documento', 'ciudad', 'password1', 'password2', 'is_active'])
    estiloBootstrap(self)

  def clean_telefono(self):
    return validarCelular(self.cleaned_data['telefono'])

  def clean(self):
    datos = super().clean()
    if datos.get('password1') != datos.get('password2'):
      self.add_error('password2', 'Las contraseñas no coinciden.')
    elif not self.instance.pk and not datos.get('password1'):
      self.add_error('password1', 'Este campo es obligatorio.')
    return datos

  def save(self, commit=True):
    usuario = super().save(commit=False)
    if self.cleaned_data['password1']:
      usuario.set_password(self.cleaned_data['password1'])
    usuario.is_staff = usuario.rol == 'admin'
    usuario.save()
    guardarPerfil(self, usuario)
    return usuario


class MiPerfilForm(forms.ModelForm):
  telefono = forms.CharField(label='Teléfono', max_length=20, required=False,
                             widget=forms.TextInput(attrs={'placeholder': '+56 9 XXXX XXXX'}))
  documento = forms.CharField(label='RUT / Documento', max_length=20, required=False)
  ciudad = forms.CharField(label='Ciudad', max_length=80, required=False,
                           widget=forms.TextInput(attrs={'autocomplete': 'off'}))

  class Meta:
    model = Usuario
    fields = ['first_name', 'last_name', 'email']

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    cargarPerfil(self, self.instance)
    estiloBootstrap(self)

  def clean_telefono(self):
    return validarCelular(self.cleaned_data['telefono'])

  def save(self, commit=True):
    usuario = super().save(commit=commit)
    guardarPerfil(self, usuario)
    return usuario
