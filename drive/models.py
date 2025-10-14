from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, username, password, role='default', **extra_fields):
        """Cria um usuário personalizado no sistema"""
        if not password:
            raise ValueError("O uso de uma senha é obrigatório!")
        
        user = self.model(username=username, role=role, **extra_fields)
        user.set_password(password)
        user.save()

    def create_superuser(self, username, password, **extra_fields):
        """Cria um super usuário"""
        extra_fields.setdefault('is_active', 'True')
        extra_fields.setdefault('is_staff', 'True')
        extra_fields.setdefault('is_superuser', 'True')
        return self.create_user(username, password, role='admin', **extra_fields)

# Modelo de usuário personalizado
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('manager', 'Gerente'),
        ('default', 'Padrão'),
    )

    username = models.CharField(max_length=150, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class Arquivo(models.Model):
    file_name = models.CharField(max_length=200)
    extension = models.CharField()
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    file_weight = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        self.file_name
