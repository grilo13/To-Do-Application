from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        The prototype of create_user() should accept the username field, plus all required fields as arguments.
        Create and save a regular User with the given email and password.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        The prototype of create_superuser() should accept the username field, plus all required fields as arguments.
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


# Create your models here.
class User(AbstractUser):
    email = models.EmailField('Email Address', unique=True)
    username = models.CharField('Username', max_length=100, blank=True)
    photo = models.ImageField(upload_to='users_pictures', default='users_pictures/default_picture.jpg', blank=True)

    USERNAME_FIELD = 'email'  # primary key of user know is email
    REQUIRED_FIELDS = []
    objects = UserManager()
