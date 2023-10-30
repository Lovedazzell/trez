
from django.contrib import admin
from . models import FundAccount
# Register your models here.

@admin.register(FundAccount)
class AdminFundAccount(admin.ModelAdmin):
    list_display= ['id','user','name','bank_account','ifsc']