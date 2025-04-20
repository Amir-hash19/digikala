from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
from django.utils.text import slugify

class UserAccountManager(BaseUserManager):
    def create_user(self, email=None, phone=None, password=None, **extra_fields):
        if not email and not phone:
            raise ValueError("The email or phone fields must be set")
        
        if email:
            email = self.normalize_email(email)
            extra_fields["email"] = email

        if phone:    
            extra_fields["phone"] = phone

        user = self.model(**extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
    
        user.save(using=self._db) 
        return user 

    def create_superuser(self, email=None, phone=None, password=None, **extra_fields):
        if not email:
            raise ValueError("SuperUser must have an email")
        if not password:
            raise ValueError("SuperUser Must have a password!")
        
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("SuperUser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("SuperUser must have is_superuser=True")

        return self.create_user(email=email, phone=phone, password=password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone = PhoneNumberField(unique=True, region='IR', blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=70)
    date_joined = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    national_id = models.CharField(max_length=10, unique=True,validators=[RegexValidator(regex=r'^\d{10}$', message="National ID must be 10 digits")])

    GENDER_TYPES = (
        ("F", "FEMALE"),
        ("M", "MALE")
    )
    gender = models.CharField(max_length=20, choices=GENDER_TYPES, null=True, blank=True)

    USER_TYPES = (
        ("normal", "Normal"),
        ("support", "Support"),
        ("admin", "Admin"),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default="normal")

    USERNAME_FIELD = "email" 
    REQUIRED_FIELDS = ["first_name", "last_name"]  
    objects = UserAccountManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.first_name)  
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_short_name(self):
        return f"{self.first_name}"

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"
