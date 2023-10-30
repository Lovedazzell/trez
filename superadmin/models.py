from django.db import models
from authentication.models import User
from core.models import Transtions
# Create your models here.




class FeedBack(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=70,null=True,blank=True)
    content = models.CharField(max_length=500,null=True,blank=True)
    ticket = models.CharField(max_length=50,null=True,blank=True)
    reason = models.CharField(max_length=50,null=True,blank=True)
    closed =  models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class FailedRecord(models.Model):
    tran = models.CharField(max_length = 100,null = True , blank = True)
    event = models.CharField(max_length = 100,null = True , blank = True)
 
    pay_id = models.CharField(max_length = 80,default='null')
   
    # request open status
    open = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add=True)




class ManualWithdraw(models.Model):
    user = models.ForeignKey(Transtions ,on_delete=models.CASCADE,related_name='tran')
    open_status = models.BooleanField(default=True)
    fund_name = models.CharField(max_length=100,null=True,blank=True)
    fund_account = models.CharField(max_length=100,null=True,blank=True)
    fund_ifsc = models.CharField(max_length=100,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True ,null=True, blank=True)
    