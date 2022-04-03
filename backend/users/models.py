
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_ROLES = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    ]
    username = models.SlugField(
        'Имя пользователя',
        help_text='Имя пользователя',
        max_length=150,
        blank=False,
        unique=True
    )
    email = models.EmailField(
        'Эл. почта',
        help_text='Эл. почта пользователя',
        blank=False,
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        help_text='Имя пользователя',
        max_length=150,
        blank=False
    )
    last_name = models.CharField(
        'Фамилия',
        help_text='Фамилия пользователя',
        max_length=150,
        blank=False
    )
    role = models.CharField(
        'Роль',
        help_text='Роль пользователя',
        max_length=150,
        blank=False,
        choices=USER_ROLES,
        default='user',
    )

    password = models.CharField(max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # @property
    # def is_subscribed(self):
    #     if self.username
    # is_subscribed = Follow.objects.filter()

    @property
    def is_admin(self):
        if self.role == 'admin' or self.is_superuser:
            return True

    @property
    def is_moderator(self):
        if self.role == 'moderator' or self.is_superuser:
            return True

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        help_text='Выберите пользователя',
        verbose_name='Пользователь',
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='Подписан',
        help_text='Выберите на кого подписан пользователь',
    )

    class Meta():
        constraints = (models.UniqueConstraint(
            fields=('user', 'author'),
            name='unique-in-module'
        ),)

    def __str__(self):
        return f'{self.user.username} подписан на {self.author.username}'
