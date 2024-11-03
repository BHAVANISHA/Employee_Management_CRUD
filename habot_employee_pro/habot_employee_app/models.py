from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Permission, Group


class UserManager( BaseUserManager ):
    def create_user(self,
                    user_email: str,
                    password: str,
                    is_staff=False,
                    is_superuser=True,
                    **extra_fields

                    ) -> "Users":
        if not user_email:
            raise ValueError( "User must have an email" )

        users = self.model( user_email=user_email, **extra_fields )
        users.set_password( password )
        users.is_active = True
        users.is_staff = is_staff
        users.is_superuser = is_superuser
        users.save()

        return users


    def create_superuser(
            self, user_email, password, **extra_fields
    ) -> "Users":
        extra_fields.setdefault( 'is_staff', True )
        extra_fields.setdefault( 'is_superuser', True )
        extra_fields.setdefault( 'is_active', True )
        users = self.create_user(
            user_email,
            password,
            **extra_fields
        )
        users.save()
        return users


class Users( AbstractUser ):
    username = models.CharField( max_length=255, null=True, blank=True )
    password = models.CharField( max_length=255 )
    last_login = models.DateTimeField( blank=True, null=True )
    is_superuser = models.IntegerField( null=True )
    first_name = models.CharField( max_length=100, blank=True, null=True )
    last_name = models.CharField( max_length=100, blank=True, null=True )
    email = models.CharField( max_length=254, null=True )
    is_staff = models.IntegerField(default=1)
    token = models.CharField( max_length=255, blank=True, null=True )
    is_active = models.IntegerField(default=1)
    date_joined = models.DateTimeField( auto_now_add=True )
    user_id = models.CharField( primary_key=True, default=None, max_length=10 )
    user_name = models.CharField( max_length=255, blank=True, null=True )
    user_phone = models.CharField( max_length=255, blank=True, null=True )
    status = models.CharField( max_length=255, null=True )
    is_verified = models.CharField( max_length=255,default=0 )
    reg_date = models.DateTimeField( auto_now_add=True )
    user_email = models.CharField( unique=True, max_length=255 )
    dob = models.DateField( blank=True, null=True )
    user_password = models.CharField( max_length=255 )
    gender = models.CharField( max_length=10, blank=True, null=True )
    first_login = models.IntegerField( blank=True, null=True )
    address = models.CharField( max_length=100, blank=True, null=True )
    city = models.CharField( max_length=100, blank=True, null=True )
    state = models.CharField( max_length=100, blank=True, null=True )
    postal_code = models.CharField( max_length=100, blank=True, null=True )
    country = models.CharField( max_length=100, blank=True, null=True )

    USERNAME_FIELD = 'user_email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    # Override groups and user_permissions with unique related_name
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',  # Custom related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # Custom related_name
        blank=True
    )

class Employee(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(unique=True,blank=False)
    department = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)

class HabotAuthtoken( models.Model ):
    digest = models.CharField( primary_key=True, max_length=128 )
    token_key = models.CharField( max_length=8 )
    created = models.DateTimeField()
    expiry = models.DateTimeField( blank=True, null=True )
    user_id = models.CharField(max_length=12)
