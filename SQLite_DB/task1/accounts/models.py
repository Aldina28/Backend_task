from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Custom user manager to manage user creation and management(Acts as an interface through which django models interact with database)
class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The email is not given.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

# Custom user model inheriting from AbstractBaseUser       
class CustomUser(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True, null=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128, null=True)
    name = models.CharField(max_length=255, blank=True, default='')
    phone = models.IntegerField()
    

    USERNAME_FIELD = 'email' 

    objects = UserManager()


