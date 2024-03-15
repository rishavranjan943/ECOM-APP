from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password,first_name,last_name, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        if not password:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name,last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password,first_name,last_name, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password,first_name,last_name ,**extra_fields)

    def create_superuser(self, email, password,first_name,last_name, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active',True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password,first_name,last_name, **extra_fields)

    

class User(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(db_index=True,unique=True,max_length=100)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    is_staff=models.BooleanField(default=True)
    is_active=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)

    objects=CustomUserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name']

    class Meta:
        verbose_name='User'
        verbose_name_plural='Users'


User._meta.get_field('groups').remote_field.related_name = 'user_groups'
User._meta.get_field('user_permissions').remote_field.related_name = 'user_permissions_set'

class Forgot(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    forgot_password_token=models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.user.email