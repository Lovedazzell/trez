from django.contrib import admin
from . models import UserCollection ,MazorCollection ,Transtions , Notification, TimeCapture,CountdownSeconds


@admin.register(UserCollection)
class AdminUserCollection(admin.ModelAdmin):
    list_display = ['id','content_name','sub_content_name','iscolor','ref_name','gems',
    'created','expired','won','won_money','unique_key']


@admin.register(MazorCollection)
class AdminMazorCollection(admin.ModelAdmin):
    list_display = ['id','color','number','num_color','created','unique_key']


@admin.register(Transtions)
class AdminTransition(admin.ModelAdmin):
    list_display = ['user','transtion_id','created','status','desc','money','fluctuate_gems','updates_gems']

@admin.register(Notification)
class AdminNotification(admin.ModelAdmin):
    list_display= ['title','notification','is_seen','created']

@admin.register(TimeCapture)
class AdminTimeCapture(admin.ModelAdmin):
    list_display= ['id','time','created','key']


@admin.register(CountdownSeconds)
class AdminCountdownSeconds(admin.ModelAdmin):
    list_display= ['id','sec']