import json
from django.shortcuts import render
from django.http import JsonResponse , HttpResponseRedirect
from core.models import UserCollection  ,Transtions,CountdownSeconds
from django.views.decorators.csrf import csrf_exempt
from authentication.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from superadmin. helpers import  live_syncronize_data , ticket_no
import requests
from.models import FundAccount
from authentication.helpers import verification_required
from django.contrib.auth.decorators import login_required
from superadmin.helpers import admin_money_analysis
from django.contrib import messages
from requests.auth import HTTPBasicAuth
from superadmin.models import FeedBack
from authentication.tasks import email_to_user
from django.conf import settings
import requests
import re



# get colors
@csrf_exempt
@login_required
@verification_required
def spent_gems(request):
    if request.method == 'POST':
        check_status = CountdownSeconds.objects.all().first()
        if int(check_status.sec) <= 173:
            player = User.objects.get(email = request.user)
            check = request.POST['total_data']
            if check.isnumeric():
                if int(request.POST['total_data'])  <= int(player.gems):
                    # Adding user gems spending data
                    data = UserCollection(user = request.user ,content_name = request.POST['ydata'],
                    sub_content_name = request.POST['xdata'], gems =  int(request.POST['total_data']))

                    if request.POST['xdata'] == 'color':
                        data.iscolor = True
                    data.save()

                    # Making transition history

                    updated_gems = int(player.gems)  - int(request.POST['total_data'])
                    tran_history = Transtions(user = request.user,status=True ,desc ='Purchase gems',money='debit',fluctuate_gems = float(request.POST['total_data']),
                    updates_gems = float(updated_gems) )
                    tran_history.save()
                    

                    # save updated gems

                    player.gems = updated_gems
                    player.save()

                    # send channel request

                    channel_layer = get_channel_layer()
                    data  = UserCollection.get_user_gem_detail(request.user.reffer_code)
                
                    async_to_sync(channel_layer.group_send)(
                        'gems_%s'% request.user.reffer_code,{
                            'type':'gems_data',
                            'value': json.dumps(data)
                        }
                    )

                    async_to_sync(channel_layer.group_send)(
                        'live_data_group',{
                            'type':'live_sync',
                            'value': json.dumps(live_syncronize_data())
                        }
                    )
                    return JsonResponse({'status':'m-success' ,'message':' Good luck for result'})
                else:
                    return JsonResponse({'status':'m-error','message':'Insufficent gems please add more' })
            else:
                return JsonResponse({'status':'m-error','message':'Something Went Wrong' })
        else:
            message = 'Please wait for countdown start'
            return JsonResponse({'status':'m-error' , 'message':message})





# Payment request handler
@csrf_exempt
def PaymentVerify(request):
    print(request.GET)
    return render(request,'apis/verify.html')




# Add Benificiary
@csrf_exempt
@login_required
@verification_required
def add_beneficery(request):
    name = request.POST['name']
    account = request.POST['account1']
    ifsc = request.POST['ifsc']  

    # update fund account
    update_fund_account = FundAccount(user = request.user, name = name ,
    bank_account = account , ifsc = ifsc  ) 
    
    update_fund_account.save()

    return JsonResponse({'status':'m-success' ,'message':' Beneficiary added successfully'})

        
@csrf_exempt
@login_required
@verification_required
def add_refference_code(request):
    reffer_id = request.POST['value']
 
    # find parent user by reffer id+
    if User.objects.filter(reffer_code = reffer_id).exists():

        # getting  user for empty validation
        parent_user = User.objects.get(reffer_code = reffer_id)
        current_user = User.objects.get(email = request.user.email)

        if reffer_id == current_user.reffer_code:
            return JsonResponse({'status':'m-error','message':' Invalid reffer code '})

        elif  parent_user.reffer_by ==  current_user.reffer_code  :
            return JsonResponse({'status':'m-error','message':' Invalid reffer code '})

        else:
            if current_user.reffer_by == 'none':
                # current user reffer by create
                current_user.reffer_by = reffer_id
                current_user.save()
                email_to_user(parent_user.email,'Congratulations you have new reffer friend',f'<div style="border: 2px solid blue;border-radius: 5px;padding: 10px;"><h1>{current_user.email} join Trezunt by your reffer code</h1><p>Keep share your code to earn more money</p></div>')
                return JsonResponse({'status':'m-success','message':' Reffer code successfully updated'})
            else:
                return JsonResponse({'status':'m-error','message':' User have already register the reffer id '})

    else:
        return JsonResponse({'status':'m-error','message':' Invalid Reffer Code'})
 


@csrf_exempt
@login_required
@verification_required
def money_record(request):
    if request.method == 'POST':
        filter_date = request.POST['selected_date']
        if filter_date != "":
            data = admin_money_analysis(filter_date)
            return JsonResponse({'status':'success','data':data})
        else:
            return JsonResponse({'status':'failed'})


@csrf_exempt
@login_required
@verification_required
def support(request):
    if request.method == 'POST':
        title =request.POST['ttl']
        comment = request.POST['cmt']
        token = ticket_no()
        data = FeedBack(user = request.user ,title = title , content = comment,ticket = token)
        data.save()
        email_to_user(request.user.email,f'Your Ticket has been raised  #{token}',f'<div style="border: 2px solid blue;border-radius: 5px;padding: 10px;"><h1>Thanks For Contact Us</h1><p>Your ticket number is <b style="color: blue;">#{token}</b></p><p>We will procees further conversation in this email</p><p>You will get response ASAP</p></div>')
        return JsonResponse({'status':'m-success','message':'Ticket Raised'})
        


@csrf_exempt
@login_required
@verification_required
def profile_update(request):
    data = request.POST['data']
    input = request.POST['input']

    current_user = User.objects.get(email = request.user.email)
    if input == 'number':
        Pattern = re.compile("[6-9][0-9]{9}")
        if Pattern.match(data) == None:
            return JsonResponse({'status':'m-error','message':'Please provide valid number'})
        else:
            if len(str(data)) == 10:
                current_user.mobile = int(data)
                current_user.save()
                return JsonResponse({'status':'m-success','message':'Number update successfully'})
            else:
                return JsonResponse({'status':'m-error','message':'Please provide valid number'})
    elif input == 'username':
        if len(data) < 3:
            return JsonResponse({'status':'m-error','message':'Please provide valid nick name'})
        else:
            if data.isalpha():
                current_user.username = data
                current_user.save()
                return JsonResponse({'status':'m-success','message':'Nick name update successfully'})
            else:    
                return JsonResponse({'status':'m-error','message':'Numeric not allowed'})
    else:
        return JsonResponse({'status':'m-error','message':'Something went wrong'})


