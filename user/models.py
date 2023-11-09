# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
#from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_activer', True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True, default='', null=True)
    name = models.CharField(max_length=10, default='', null=True)
    nickname = models.CharField(max_length=50, unique=True, default='', null=True)
    phone = models.IntegerField(unique=True, verbose_name='Phone Number', blank=False, default='', null=True, help_text='Enter 10 digits phone number')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'name' ,'nickname']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    """
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    """
