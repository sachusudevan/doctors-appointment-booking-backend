from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid


class UserManager(BaseUserManager):
	def create_user(self, phone, password=None, otp=None):
		if not phone:
			raise ValueError('Users must have an Phone Number')
		user = self.model(
            phone=phone,
            otp=otp,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, phone, password=None,otp=None):
		user = self.create_user(
			password=password,
            phone=phone,
            otp=otp
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Users(AbstractBaseUser):
    phone = models.CharField(
    	verbose_name="phone", 
        max_length=20, 
        unique=True, 
        blank=True, 
        null=True,
        )
    username = models.CharField(
        max_length=300, 
        blank=True, 
        null=True,
        )
    first_name = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        )
    last_name = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        )
    email = models.EmailField(
    	max_length=255, 
        unique=True, 
        blank=True, 
        null=True,
        )
    date_joined = models.DateTimeField(
        verbose_name='date joined', 
        auto_now_add=True, 
        blank=True,
        null=True,
        )
    last_login = models.DateTimeField(
    	verbose_name='last login', 
        auto_now=True, 
        blank=True, 
        null=True,
        )
    otp = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        )
    is_verified           = models.BooleanField(default=False)
    is_admin              = models.BooleanField(default=False)
    is_active             = models.BooleanField(default=True)
    is_staff              = models.BooleanField(default=False)
    is_superuser          = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'

    objects = UserManager()

    def __str__(self):
        return self.phone

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True
