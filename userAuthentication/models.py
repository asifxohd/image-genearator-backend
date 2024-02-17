from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser, PermissionsMixin 



class UserAccountManager(BaseUserManager):
    """Custom manager for the custom user model."""

    def create_user(self, username, email, phone_number, password=None):
        """Create a new user with the given username, email, phone number, and password."""
        if not email:
            raise ValueError("Email must be provided")
        if not phone_number:
            raise ValueError("phone_number must be provided")

        email = self.normalize_email(email).lower()
        user = self.model(username=username, email=email, phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password=None, phone_number=None):
        """Create a new superuser with the given username, email, and password."""
        user = self.create_user(
            username=username, email=email, password=password, phone_number=phone_number
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    """Model for managing accounts."""

    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=150)
    phone_number = models.CharField(unique=True, max_length=12)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    objects = UserAccountManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "phone_number")

    def __str__(self) -> str:
        return f"{self.username} with email :- {self.email}"
