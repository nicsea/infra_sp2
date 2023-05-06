from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRoles(models.TextChoices):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email for user need to be specified')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        extra_fields['role'] = 'admin'
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(
        'Email',
        max_length=254,
        unique=True,
    )
    role = models.CharField(
        'User role',
        max_length=32,
        choices=UserRoles.choices,
        default=UserRoles.USER,
    )
    bio = models.TextField(
        'Biography',
        blank=True,
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_moderator(self):
        return self.role == UserRoles.MODERATOR
