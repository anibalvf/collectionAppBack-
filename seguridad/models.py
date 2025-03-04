from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import os
from django.db.models.aggregates import Count


from django.contrib.auth.signals import user_logged_in


class Usuarios(User):

    class Meta:
        proxy = True
        ordering = ('first_name', )



class User_Detalle(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="detalle", blank=False, null=False, help_text="usuario", verbose_name=_('usuario'))
    nif = models.CharField(_('NIF'), max_length=255, null=True, blank=True)
    fecha_nacimiento = models.DateField(_('Fecha de Nacimiento'), null=True, blank=True)
    tipo_via = models.CharField(_('Tipo de Vía'), max_length=50, null=True, blank=True)
    direccion = models.CharField(_('Dirección'), max_length=250, null=True, blank=True)
    codigo_postal = models.CharField(_('Código Postal'), max_length=20, null=True, blank=True)
    telefono_1 = models.CharField(_('Teléfono 1'), max_length=15, null=True, blank=True)
    telefono_2 = models.CharField(_('Teléfono 2'), max_length=15, blank=True, null=True)
    email = models.EmailField(_('Email'), null=True, blank=True)
    numero_ss = models.CharField(_('Número de la Seguridad Social'), max_length=50, null=True, blank=True)
    iban = models.CharField(_('IBAN'), max_length=50, null=True, blank=True)

    def __str__(self):
        return self.usuario.username

    class Meta:
        verbose_name = _('Detalle de usuario')
        verbose_name_plural = _('Detalles de usuarios')
    class PrivacyMeta:
        fields = ['telefono']

class SessionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40)
    start_time = models.DateTimeField()
    last_activity = models.DateTimeField(null=True)
    duration = models.DurationField()
    

    def __str__(self):
        return f"{self.user.username} - {self.session_key}"