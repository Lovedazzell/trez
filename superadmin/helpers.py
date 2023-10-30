
# returning live data to admin interface

def live_syncronize_data():
    from django.db.models import Sum , Q
    from core.models import UserCollection 
    live_sync_data = {}

    green_total = UserCollection.objects.filter(Q(content_name= 'green') & Q(expired = False)).aggregate(Sum('gems'))
    blue_total = UserCollection.objects.filter(Q(content_name= 'blue') & Q(expired = False)).aggregate(Sum('gems'))
    

    # Adding sum of blue in dictionary
    if  blue_total['gems__sum'] != None:
        live_sync_data['blue'] = blue_total['gems__sum']
    else:
        live_sync_data['blue'] = 0


    # Adding sum of green in dictionary
    if  green_total['gems__sum'] != None:
        live_sync_data['green'] = green_total['gems__sum']
    else:
        live_sync_data['green'] = 0



    for i in range(10):
        
        # Making green number sum dictionary
        green_num = UserCollection.objects.filter(Q(sub_content_name= 'green') & Q(expired = False)& Q(content_name = i)).aggregate(Sum('gems'))
        if  green_num['gems__sum'] != None:
            live_sync_data[f'green{i}'] = green_num['gems__sum']
        else:
            live_sync_data[f'green{i}'] = 0


        # Making blue number sum dictionary
        blue_num = UserCollection.objects.filter(Q(sub_content_name= 'blue') & Q(expired = False)& Q(content_name = i)).aggregate(Sum('gems'))
        if  blue_num['gems__sum'] != None:
            live_sync_data[f'blue{i}'] = blue_num['gems__sum']
        else:
            live_sync_data[f'blue{i}'] = 0

    return live_sync_data



# Money analysis

def admin_money_analysis(spec_date):
    from core.models import Transtions
    from django.db.models import Sum , Q
    from core.models import UserCollection
    
    # Total cash flow
    total_fluctuation  = 0

    fetch_total_fluctuation = UserCollection.objects.filter(created__date = spec_date).aggregate(Sum('gems'))

    if fetch_total_fluctuation['gems__sum'] != None:
        total_fluctuation  += fetch_total_fluctuation['gems__sum']

    # Total winning amount  
    total_color = Transtions.objects.filter(Q(created__date = spec_date) &  Q(desc = 'Win color')).aggregate(Sum('fluctuate_gems'))
    total_number = Transtions.objects.filter(Q(created__date = spec_date) &  Q(desc = 'Win number')).aggregate(Sum('fluctuate_gems'))
    total_reffer = Transtions.objects.filter(Q(created__date = spec_date) &  Q(desc = 'reffer bonus')).aggregate(Sum('fluctuate_gems'))
        
    
    total_spend_win = 0
    
    money_list = [total_color ,total_number , total_reffer ]

    for i in money_list:
        if i['fluctuate_gems__sum'] != None:
            total_spend_win  += i['fluctuate_gems__sum']
            

    # Total bank entries 

    bank_entries = Transtions.objects.filter(Q(created__date = spec_date) &  Q(desc = 'PhonePay') & Q(status = True)).aggregate(Sum('fluctuate_gems'))

    total_bank_entries = 0

    if bank_entries['fluctuate_gems__sum'] != None:
        total_bank_entries += bank_entries['fluctuate_gems__sum']


    # Total Earning

    total_earning = 0

    if total_fluctuation != None:
        total_earning = total_fluctuation - total_spend_win

    # total_withdraw

    bank_withdraw = Transtions.objects.filter(Q(created__date = spec_date) &  Q(desc = 'Withdraw Money')).aggregate(Sum('fluctuate_gems'))

    total_bank_withdraw = 0

    if bank_withdraw['fluctuate_gems__sum'] != None:
        total_bank_withdraw += bank_withdraw['fluctuate_gems__sum']


    # Return Value

    final_data = {'cash_flow':total_fluctuation, 
                    'earning':total_earning, 'withdraw': total_bank_withdraw ,
                    'bank_transitions':total_bank_entries , 'user_winning_amount':total_spend_win }

    return final_data


# ticket no generator
def ticket_no():
    import random
    import string
    num = string.digits
    combine = list(num)
    random.shuffle(combine)
    final_id = ''.join(combine)[:9]

    from .models import FeedBack
    if FeedBack.objects.filter(ticket = final_id).exists():
        final_id = ticket_no()
        
    return final_id