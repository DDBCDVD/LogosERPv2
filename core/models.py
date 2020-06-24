from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    user_image = models.ImageField(
        upload_to='users', blank=True,
        null=True, verbose_name="Imagen de Perfil",
        default='default/default_avatar.png')


class Crum(models.Model):
    user_creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='+',
        null=True, blank=True,
        verbose_name='Ultimo usuario en modificar')
    user_updater = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='+',
        null=True, blank=True,
        verbose_name='Ultimo usuario en modificar')
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True,
        verbose_name='Fecha Creacion')
    date_updated = models.DateTimeField(
        auto_now=True, null=True, blank=True,
        verbose_name='Fecha Modificación')

    class Meta:
        abstract = True
