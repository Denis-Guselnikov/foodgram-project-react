from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    email = models.EmailField(
        verbose_name='Почта',
        max_length=256,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=256
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=256
    ) 

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Follow(models.Model):
    """Подписка."""
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        db_index=False,
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        db_index=False,
        verbose_name='Автор'
    )

    class Meta:
        unique_together = ('user', 'author')

    def __str__(self):
        return f'Пользователь {self.user} подписан на {self.author}'
