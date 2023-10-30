from django.shortcuts import render
from django.http import HttpResponseRedirect
import json
from django.contrib.auth.decorators import login_required
from .helpers import live_syncronize_data ,admin_money_analysis
from django.utils.decorators import method_decorator
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from authentication.helpers import super_user_required
from django.views.generic.base import TemplateView 
from datetime import date
from authentication.models import User
from .models import FeedBack,FailedRecord, ManualWithdraw
import requests
from core.models import Transtions
from django.conf import settings
import xlwt
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse

# Create your views here.


# live data fro superuser
@login_required
@super_user_required
def live_data(request):
    if request.user.is_superuser:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'live_data_group',{
                'type':'live_sync',
                'value': json.dumps(live_syncronize_data())
            }
        )
        return render(request,'superadmin/live_data.html',{'data':live_syncronize_data()})
    else:
        return HttpResponseRedirect('/profile/')


@method_decorator(login_required,name = 'dispatch')
@method_decorator(super_user_required,name = 'dispatch')
class MoneyAnalysis(TemplateView):
    template_name = 'superadmin/money_analysis.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = admin_money_analysis(date.today())
        return context
    
class CustomDayDetail(TemplateView):
    template_name = 'superadmin/custom_day_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(login_required,name = 'dispatch')
@method_decorator(super_user_required,name = 'dispatch')
class AdminSupport(TemplateView):
    template_name = 'superadmin/support.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data']= FeedBack.objects.filter(closed = False)
        return context


@method_decorator(login_required,name = 'dispatch')
@method_decorator(super_user_required,name = 'dispatch')
class SupportDetail(TemplateView):
    template_name = 'superadmin/support_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data']= FeedBack.objects.get(id = kwargs['pk'])
        return context

    def post(self,request,pk):
        data = FeedBack.objects.get(id = pk)
        data.reason = request.POST['reason']
        data.closed = True
        data.save()
        return HttpResponseRedirect('/suad/admin_support/')


# proceed refund
@method_decorator(login_required,name = 'dispatch')
@method_decorator(super_user_required,name = 'dispatch')
def process_refund(request,order_id):
      
    report = FailedRecord.objects.get(tran = order_id)
    tran_data =Transtions.objects.get(transtion_id = order_id)
    if tran_data.status == False:
        report.open = False
        tran_data.status  = True

        # transition fees
        fees =  int(tran_data.fluctuate_gems) * 3/100
        # subtract fees from amount
        after_fees = int(tran_data.fluctuate_gems) - fees
       
        tran_data.fees = fees

        # getting current user
        payment_user = User.objects.get(email = str(tran_data.user))

        # update user gems
        payment_user.gems += after_fees
        payment_user.save()

        # updating closing balance
        tran_data.fluctuate_gems = after_fees 
        tran_data.updates_gems = payment_user.gems

        tran_data.save()
        report.save()

    return HttpResponseRedirect('/suad/admin_refund/')
    




# get specific refund detail
@method_decorator(login_required,name = 'dispatch')
@method_decorator(super_user_required,name = 'dispatch')
class RefundDetail(TemplateView):
    template_name = 'superadmin/refund_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context



# admin refund start page
@method_decorator(login_required,name = 'dispatch')
@method_decorator(super_user_required,name = 'dispatch')
class AdminRefund(TemplateView):
    template_name = 'superadmin/admin_refund.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# manual refund start page
@method_decorator(login_required,name = 'dispatch')
@method_decorator(super_user_required,name = 'dispatch')
class ManualUserWithdraw(TemplateView):
    template_name = 'superadmin/manual_withdraw.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data"] = ManualWithdraw.objects.filter(open_status = True)
        return context
    

# confirm manual withdraw 
@method_decorator(login_required,name = 'dispatch')
@method_decorator(super_user_required,name = 'dispatch')
class ConfirmWithdrawStatus(TemplateView):
    template_name = 'superadmin/confirm_withdraw.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data"] = ManualWithdraw.objects.get(id = kwargs['pk'])
        return context
    
    def post(self,request,pk):
        close_ticket = ManualWithdraw.objects.get(id = pk)
        close_ticket.open_status = False
        close_ticket.save()
        return HttpResponseRedirect('/suad/withdraw_mn/')
        
     


# download feedback xml 
@method_decorator(login_required,name = 'dispatch')
@method_decorator(super_user_required,name = 'dispatch')
def download_feedback(request):
    # content-type of response
	response = HttpResponse(content_type='application/ms-excel')

	#decide file name
	response['Content-Disposition'] = 'attachment; filename="Feedback_data.xls"'

	#creating workbook
	wb = xlwt.Workbook(encoding='utf-8')

	#adding sheet
	ws = wb.add_sheet("sheet1")

	# Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	# headers are bold
	font_style.font.bold = True

	#column header names, you can use your own headers here
	columns = ['Email', 'Title', 'Complaint', 'Ticket', 'Close Reason','Closed','Created','Updated']

	#write column headers in sheet
	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	# Sheet body, remaining rows
	font_style = xlwt.XFStyle()

	#get your data, from database or from a text file...
	data = FeedBack.objects.all() #dummy method to fetch data.
	for my_row in data:
		row_num = row_num + 1
		ws.write(row_num, 0, str(my_row.user), font_style)
		ws.write(row_num, 1, my_row.title, font_style)
		ws.write(row_num, 2, my_row.content, font_style)
		ws.write(row_num, 3, '#'+str(my_row.ticket), font_style)
		ws.write(row_num, 4, my_row.reason, font_style)
		ws.write(row_num, 5, my_row.closed, font_style)
		ws.write(row_num, 6, str(my_row.created), font_style)
		ws.write(row_num, 7, str(my_row.updated ), font_style)

	wb.save(response)
	return response

   