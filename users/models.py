from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        verbose_name="Имя пользователя",
        max_length=20,
        unique=True,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        verbose_name="Email", unique=True, blank=False, null=False
    )
    tg_chat_id = models.CharField(
        max_length=30, verbose_name="tg_chat_id", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
