import json
from django.db import models
from authentication.models import User
from django.db.models import Q
from .helpers import order_id
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from froala_editor.fields import FroalaField

# Create your models here.


class TimeCapture(models.Model):
    time = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now=True)
    key = models.CharField(max_length=300,null=True,blank=True)

class CountdownSeconds(models.Model):
    sec = models.IntegerField(null=True,blank=True)

    def save(self,*args,**kwargs):
        channel_layer = get_channel_layer()
        data = {
            'sec':self.sec,
        }
        async_to_sync(channel_layer.group_send)(
                    'live_count_group',{
                        'type':'countdown_data',
                        'value': json.dumps(data)
                    }
                )
        super(CountdownSeconds,self).save(*args,**kwargs)



class UserCollection(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE , related_name='user_relation')
    content_name = models.CharField(max_length=50,null=True,blank=True)
    sub_content_name = models.CharField(max_length=50,null=True,blank=True)
    ref_name = models.CharField(max_length=50,null=True,blank=True)
    iscolor = models.BooleanField(default=False)
    gems = models.IntegerField(default=0)
    created = models.DateTimeField( auto_now_add=True)
    expired = models.BooleanField(default=False)
    won = models.BooleanField(default=False)
    won_money = models.IntegerField(default=0)

    unique_key = models.CharField(max_length=300,default='null')

    def save(self,*args,**kwargs):
        fetch_key = TimeCapture.objects.latest('created')
        self.unique_key = fetch_key.key 
        super(UserCollection,self).save(*args,**kwargs)

    def __str__(self):
        return str(self.user)
    


    @staticmethod
    def get_user_gem_detail(player_id):
        player = UserCollection.objects.filter(user__reffer_code = player_id).order_by('-created').first()
        player_gems = User.objects.get(reffer_code = player_id)
        data ={}
        data['content_name'] = player.content_name
        data['sub_content_name'] = player.sub_content_name
        data['iscolor'] = player.iscolor
        data['gems'] = player.gems
        data['player_gems'] = player_gems.gems
        return data
    
    
class MazorCollection(models.Model):
    color = models.CharField(max_length=30,  null=True , blank=True)
    number = models.IntegerField(null=True,blank=True)
    num_color = models.CharField(max_length=40, null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    unique_key = models.CharField(max_length=300,default='null')

       


class Transtions(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE, related_name = 'transition_relation' )
    transtion_id = models.CharField(max_length= 30,blank = True ,null = True)
    created = models.DateTimeField(auto_now_add = True )
    status = models.BooleanField(default = False)
    # mode of payment
    desc  = models.CharField(max_length = 20, null = True,blank = True)
    # credit or debit
    money = models.CharField(max_length= 20,null=True,blank=True)
    fluctuate_gems = models.FloatField(null =True,blank = True)
    updates_gems = models.FloatField(null =True,blank = True)
    
    fees = models.IntegerField(default=0)
    # webhook events
    refund = models.BooleanField(default = False)


    def __str__(self):
        return str(self.user)

    
    def save(self , *args , **kwargs):
        if self.desc != 'PhonePay' and self.desc != 'Withdraw Money':
            self.transtion_id = order_id()

        super(Transtions,self).save(*args,**kwargs)


class Notification(models.Model):
    title = models.CharField(max_length=70 , null=True , blank=True )
    notification = FroalaField()
    is_seen = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    

    def save(self,*args,**kwargs):
        channel_layer = get_channel_layer()
      
        data = {
            'title':self.title,
        }

        async_to_sync(channel_layer.group_send)(
                    'all_user_notify_group',{
                        'type':'notify_data',
                        'value': json.dumps(data)
                    }
                )


        super(Notification,self).save(*args,**kwargs)


    

