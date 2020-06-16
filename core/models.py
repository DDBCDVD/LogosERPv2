from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    user_image = models.ImageField(
        upload_to='users', blank=True,
        null=True, verbose_name="Imagen de Perfil",
        default='default/avatar.png')
