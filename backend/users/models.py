from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CheckConstraint, F, Q, UniqueConstraint

from .constants import MAX_EMAIL_LENGTH


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=MAX_EMAIL_LENGTH,
        unique=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        related_name='subscriber',
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='subscribing',
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('-id',)
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            ),
            CheckConstraint(
                check=~Q(user=F('author')),
                name='self_following',
            ),
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
