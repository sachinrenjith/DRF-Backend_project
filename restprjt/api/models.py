from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,username,email,is_doctor,password=None):
        if not email:
            raise ValueError('User need an Email Address!')
        user = self.model(
            email = self.normalize_email(email),           
            username = username,
            is_doctor = is_doctor
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,username,email,password=None,is_doctor=False):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            is_doctor=is_doctor,
            is_staff = True
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_doctor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    objects = UserManager()
    
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['username']  

    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    
    def has_module_perms(self,app_labels):
        return True
    
    
    
    @property
    def is_staff(self):
        return self.is_admin
     

class Doctor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='doctor')
    hospital = models.CharField(max_length=255,null=True,blank=True)
    department = models.CharField(max_length=255,null=True,blank=True)
    is_verified = models.BooleanField(default=False)   
    