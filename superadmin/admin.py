from django.contrib import admin
from . models import FeedBack,FailedRecord,ManualWithdraw
# Register your models here.


admin.site.register(FeedBack)
admin.site.register(FailedRecord)
admin.site.register(ManualWithdraw)