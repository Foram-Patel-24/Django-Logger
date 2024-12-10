from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

# Create your models here.
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    )

    id = models.BigAutoField(primary_key=True)
    last_login = models.DateTimeField(_("last login"), null=True)
    email = models.EmailField(_("email address"), unique=True)
    is_active = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS_CHOICES,max_length=10, default='active' )  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.IntegerField(default=0)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",  # Custom related_name to avoid conflict
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",  # Custom related_name to avoid conflict
        blank=True
    )

    objects = UserManager()  

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [] 
    
    class Meta:
        db_table = "User"
        ordering = ["-id"]