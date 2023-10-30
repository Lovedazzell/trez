from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from authentication.helpers import verification_required 
from django.views.generic.base import TemplateView
from core . helpers import order_id , custom_id
import requests
from hashlib import sha256
import base64
import math
from superadmin.models import FailedRecord , ManualWithdraw 
from core. models import Transtions
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from authentication.models import User
from django.conf  import settings
from apis.models import FundAccount
import json
from django.views.decorators.csrf import csrf_exempt
from authentication.tasks import email_to_user
import requests

from requests.auth import HTTPBasicAuth

# Create your views here.



# Add gems in profile
@method_decorator(csrf_exempt,name = 'dispatch')
@method_decorator(login_required,name = 'dispatch')
@method_decorator(verification_required,name = 'dispatch')
class AddGems(TemplateView):
    template_name = 'intg/addgems.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def post(self,request):
        if request.user.mobile and request.user.username:
            if int(request.POST.get('amount')) >= 99:      

                if self.request.user.unique_key:
                    merchant_id = request.user.unique_key
                else:
                    merchant_id = custom_id('Trez')
                    # creating merchant user unique id
                    user = User.objects.get(email = request.user.email)
                    user.unique_key = merchant_id
                    user.save()


                amount =  int(request.POST.get('amount'))*100
                data_amount =  int(request.POST.get('amount'))

                tran_id = order_id()

                url ="https://api.phonepe.com/apis/hermes/pg/v1/pay"

                data = {
                "merchantId": "TREZUNTONLINE",
                "merchantTransactionId": tran_id,
                "merchantUserId": merchant_id,
                "amount": amount,
                "redirectUrl": "http://127.0.0.1:8000/apis/payment_v/",
                "redirectMode": "POST",
                "callbackUrl": "https://3ad3-103-41-27-78.ngrok-free.app/intg/phone_pay/",
                "mobileNumber": request.user.mobile,
                "paymentInstrument": {
                    "type": "PAY_PAGE"
                }
                }

                # converting data to string
                convert_to_string = json.dumps(data)

                encoded_string = base64.b64encode(convert_to_string.encode('utf-8'))

                # decoded byte to string
                decoded_string = encoded_string.decode()

                payload = {
                    "request":decoded_string
                    }   
                
                x_verify = sha256(encoded_string+'/pg/v1/pay'.encode()+settings.SALT_KEY.encode()).hexdigest()+'###'+ settings.SALT_INDEX

                print(x_verify)

                headers = {
                    "accept": "application/json",
                    "Content-Type": "application/json",
                    "X-VERIFY": x_verify
                    }

                response = requests.post(url,headers=headers,json=payload)

                # converting response to json object
                object_data = json.loads(response.text)
                if object_data['code'] == 'PAYMENT_INITIATED':
                    
                    redirect_url  =object_data['data']['instrumentResponse']['redirectInfo']['url']

                    if object_data['code'] == 'PAYMENT_INITIATED':
                        tran_data = Transtions(user = request.user, desc = 'PhonePay', transtion_id = tran_id,
                        money = 'credit' ,fluctuate_gems = data_amount  )
                        tran_data.save()


                    return HttpResponseRedirect(redirect_url)
                else:
                    return HttpResponseRedirect('/intg/addgems/')
            else:
                return HttpResponseRedirect('/intg/addgems/')
        else:
                messages.error(request, " Please add your mobile number before add gems")
                return HttpResponseRedirect('/auth/edit_profile/')



# withdraw request 
@method_decorator(csrf_exempt,name = 'dispatch')
@method_decorator(login_required,name = 'dispatch')
@method_decorator(verification_required,name = 'dispatch')
class SendMoneyToUser(TemplateView):
    template_name   = 'intg/send_money_to_user.html'

    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['data'] = FundAccount.objects.get(pk = kwargs['pk']) 
        return context

    def post(self,request,pk):
        fund_data = FundAccount.objects.get(id = pk)
             
        if int(request.user.gems) >= 500 and int(request.POST.get('amount')) >= 500  and int(request.POST.get('amount')) <= int(request.user.gems):
            
            withdraw_tran_id = order_id() #generate orderid

          

            fees = int(request.POST.get('amount')) * 3/100


            # subtract fees from amount
            after_fees = int(request.POST.get('amount')) - fees

                
            # getting current user
            payment_user = User.objects.get(email = request.user.email)

            payment_user.gems -= int(request.POST.get('amount'))
            payment_user.save()


            tran_data = Transtions(user = request.user, desc = 'Withdraw Money',fees = fees ,transtion_id = withdraw_tran_id , money = 'debit' ,fluctuate_gems = after_fees  ,status = True , updates_gems =  payment_user.gems )

            tran_data.save()

            manual_transfer = ManualWithdraw(user = tran_data ,fund_name = fund_data.name ,fund_account= fund_data.bank_account,fund_ifsc= fund_data.ifsc )
            manual_transfer.save()

            return HttpResponseRedirect('/apis/payment_v/')
           

        elif  int(request.user.gems) < 500:
            return HttpResponseRedirect(f'/intg/send_money_to/{pk}/')

        elif  int(request.POST.get('amount')) < 500:
            messages.error(request, " Minimum withdraw limit is 500!")
            return HttpResponseRedirect(f'/intg/send_money_to/{pk}/')

        elif  int(request.POST.get('amount')) > int(request.user.gems):
            messages.error(request, "amount should be less than avaliable gems")
            return HttpResponseRedirect(f'/intg/send_money_to/{pk}/')



# withdraw page 
@method_decorator(login_required,name = 'dispatch')
@method_decorator(verification_required,name = 'dispatch')
class WithDraw(TemplateView):
    template_name   = 'intg/withdraw.html'

    def get_context_data(self, *args,**kwargs):
        context= super().get_context_data(*args,**kwargs)
        context['data'] = FundAccount.objects.filter(user__email = self.request.user.email) 
        return context



# add beneficary account
@method_decorator(login_required,name = 'dispatch')
@method_decorator(verification_required,name = 'dispatch')
class AddBeneficary(TemplateView):
    template_name =  'intg/addbenificary.html'

    def get_context_data(self, *args,**kwargs):
        context= super().get_context_data(*args,**kwargs)
        return context



# payment gateway webhook
@csrf_exempt
def phone_pay(request):
    try:
        print(request.headers['X-Verify'])
        print(request.headers)
        print(request.body)
        decoded_data = request.body.decode()
        converted_json_data = json.loads(decoded_data)
        response = base64.b64decode(converted_json_data['response']).decode()
        json_response = json.loads(response)
        print(json_response)
        tran_id = json_response['data']['merchantTransactionId']

        if Transtions.objects.filter(transtion_id = tran_id).exists():

            # getting transition
            tran   = Transtions.objects.get(transtion_id = tran_id)
            fluc_gems = tran.fluctuate_gems

            # extraction fees
            fees =  math.ceil(fluc_gems - (fluc_gems/100 * 98))
            tran.fees = fees

            # getting updates fluctuated number
            real_fluctuated = fluc_gems - fees
            tran.fluctuate_gems = real_fluctuated

            # getting user
            user = User.objects.get(email = tran.user)

            # adding updated gems to user gems
            print('gems',user.gems)
            user.gems += real_fluctuated 
            print('gems',user.gems)

            # updating closing gems
            tran.updates_gems = user.gems

            tran.status = True  


            print('user',user)
            
            print(fees)
            print(real_fluctuated)

            tran.save()
            user.save()
            msg = "Request Received"
    except Exception as e:
        msg  = "Bad Request"
        
    return JsonResponse({'status':200,'message':msg})
    



   


        