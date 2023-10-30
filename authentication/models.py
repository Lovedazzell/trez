from django.db import models
from django.contrib.auth.models import AbstractUser
from . manager import UserManager
# Create your models here.




class User(AbstractUser):

    profile_image = models.ImageField(default='profile/profile.png',upload_to = 'profile')
    mobile = models.BigIntegerField(null=True,blank=True)
    email = models.EmailField(unique=True,null=True,blank=True)
    username = models.CharField(null = True,blank=True,max_length=50)
    gems = models.FloatField(default=0)


    # for refferance
    reffer_code = models.CharField(max_length=30,null=True,blank=True)
    Reffer_money = models.FloatField(default=0)
    reffer_by = models.CharField(max_length=30,default='none')

    # for verification
    email_token = models.CharField(max_length=300,null =True,blank =True)
    is_verified = models.BooleanField(default = False)
    not_google_verified =  models.BooleanField(default = False)

    # razorpay_contact
    unique_key = models.CharField(max_length=100,null =True,blank =True)

    REQUIRED_FIELDS = []
    objects = UserManager()
    USERNAME_FIELD = 'email'
    
    
