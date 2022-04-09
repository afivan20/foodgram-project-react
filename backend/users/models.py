from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(
        "Эл. почта",
        help_text="Эл. почта пользователя",
        blank=False,
        unique=True
    )
    first_name = models.CharField(
        "Имя", help_text="Имя пользователя", max_length=150, blank=False
    )
    last_name = models.CharField(
        "Фамилия",
        help_text="Фамилия пользователя",
        max_length=150,
        blank=False
    )

    password = models.CharField(max_length=150)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("id",)

    def __str__(self):
        return self.username




class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name="follower",
        on_delete=models.CASCADE,
        help_text="Выберите пользователя",
        verbose_name="Пользователь",
    )
    author = models.ForeignKey(
        User,
        related_name="following",
        on_delete=models.CASCADE,
        verbose_name="Подписан",
        help_text="Выберите на кого подписан пользователь",
    )

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"
        ordering = ("-id",)
        constraints = (
            models.UniqueConstraint(
                fields=("user", "author"),
                name="unique-in-module"
            ),
        )

    def __str__(self):
        return f"{self.user.username}_follows_{self.author.username}"
