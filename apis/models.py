from django.db import models
from authentication.models import User
# Create your models here.



class FundAccount(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    fund_account = models.CharField(max_length=15,null=True,blank=True)
    name = models.CharField(max_length=30) 
    bank_account = models.CharField(max_length=30,null=True,blank=True)
    ifsc = models.CharField(max_length=30,null=True,blank=True)
    bankname = models.CharField(max_length=30,null=True,blank=True)

    def __str__(self):
        return str(self.user)
   


