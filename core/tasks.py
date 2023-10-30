from celery import shared_task
import time
from core.models import TimeCapture,CountdownSeconds
from datetime import datetime
from uuid import uuid4

@shared_task(bind=True)
def money_divider(self,unique_key_id):
    from django.db.models import Sum , Q
    from .models import UserCollection ,TimeCapture
    from authentication.models import User
    import random


    # time capture
    if unique_key_id != 'none':
        last_capture_time =TimeCapture.objects.get(id = unique_key_id)

        # random color variable
        # random_color = ['green','blue']
        random_number = [1,2,3,4,5,6,7,8,9,0]
        random.shuffle(random_number)
        # random.shuffle(random_color)

        # create custom random number if number list has only one  number
        def custom_win_number(real_min_color):

            # create another randowm number if list has only one number
            if real_min_color != '':

                # getting random number
                random.shuffle(random_number)

                # adding both color and number in serialise manner
                new_min_color = str(random_number[0])
                if new_min_color == real_min_color:
                    new_min_color = custom_win_number(real_min_color)
                    
            # create another random muber if list is empty
            else:
                random.shuffle(random_number)
                # random.shuffle(random_color)
                new_min_color = str(random_number[0]) 

            return new_min_color


            
        # Empty dictionary for storing color values
        color_dict = {}


        green_total = UserCollection.objects.filter(Q(unique_key = last_capture_time.key) & Q(content_name= 'green') & Q(expired = False)).aggregate(Sum('gems'))
        blue_total = UserCollection.objects.filter(Q(unique_key = last_capture_time.key) & Q(content_name= 'blue') & Q(expired = False)).aggregate(Sum('gems'))
            

        # suffling random gems if noone select color
        if blue_total['gems__sum'] == None and  green_total['gems__sum'] == None :
            random_gems = [10,20,30,40,50,60,70,80,90]
            random.shuffle(random_gems)
            color_dict['blue'] = random_gems[0]
            random.shuffle(random_gems)
            color_dict['green'] = random_gems[0]

        else:
            # Adding sum of blue in dictionary
            if  blue_total['gems__sum'] != None:
                color_dict['blue'] = blue_total['gems__sum']
            else:
                color_dict['blue'] = 0


            # Adding sum of green in dictionary
            if  green_total['gems__sum'] != None:
                color_dict['green'] = green_total['gems__sum']
            else:
                color_dict['green'] = 0



        # Finding the min color from dictionary
        won_color = min(zip(color_dict.values(), color_dict.keys()))[1]
    
        # Empty dictionary for green numbers
        number_dist = {}
        


        for i in range(10):
            # Making green number sum dictionary
            num_sum = UserCollection.objects.filter(Q(expired = False) & Q(unique_key = last_capture_time.key) & Q(content_name= i) & Q(sub_content_name= 'num')).aggregate(Sum('gems'))
            print('num',num_sum)
            if  num_sum['gems__sum'] != None:
                number_dist[f'{i}'] = num_sum['gems__sum']

        print('number dictionary' ,number_dist)

        # Full record of winning items
        from .models import MazorCollection
        

        # Finding the mix  num from dictionary
        if len(number_dist) >= 2:
            min_color_num = min(zip(number_dist.values(), number_dist.keys()))[1]
            print('real min color',min_color_num)
            full_data = MazorCollection(color = won_color ,number =min_color_num,unique_key = last_capture_time.key)
        elif len(number_dist) == 1:
            real_min_color_num = min(zip(number_dist.values(), number_dist.keys()))[1]
            min_color_num = custom_win_number(real_min_color_num)
            print('real min color',real_min_color_num)
            print('custom win color',min_color_num)
            full_data = MazorCollection(color = won_color ,number =min_color_num,unique_key = last_capture_time.key)
        else:
            min_color_num = custom_win_number('')
            print('custom win color',min_color_num)
            full_data = MazorCollection(color = won_color ,number =min_color_num,unique_key = last_capture_time.key)
    
        full_data.save()
    
        # All Unexpired data
        data = UserCollection.objects.filter(Q(unique_key = last_capture_time.key) & Q(expired = False))

        # Award for color
        for i in data:
            winner = User.objects.get(email = i.user)
            from .models import Transtions
            if i.content_name == won_color:
                addition_gems = i.gems * 80/100
                total_gems = addition_gems + i.gems
                winner.gems += total_gems
                winner.save()
                i.won = True
                i.won_money = total_gems
                i.save()


                tran_history = Transtions(user = winner,status=True ,desc ='Win color' ,money='credit',fluctuate_gems = float(total_gems),
                updates_gems = float(winner.gems) )
                tran_history.save()

                # check if reffer_by id present or not then transfer gems to reffer account
                if winner.reffer_by != 'none':
                    
                    # Getting user bu reffer id
                    reffer_user = User.objects.get(reffer_code = winner.reffer_by)
                    reffer_bonus  = i.gems * 5/100
                    
                    # Adding money to reffer money of user
                    reffer_user.Reffer_money += reffer_bonus

                    # Adding incentive to gems of reffer user
                    reffer_user.gems += reffer_bonus

                    # Total gems after adding incentive bonus


                    reffer_user.save()
                    # Making trantion history
                    reffer_tran_history = Transtions(user = reffer_user,status=True ,desc ='reffer bonus' ,money='credit',fluctuate_gems = reffer_bonus,
                    updates_gems = reffer_user.gems )
                    reffer_tran_history.save()


                
                

        
            serialize_custom_num = min_color_num
        
            if len(number_dist) != 0:
                if i.content_name == serialize_custom_num:
                    n_addition_gems = i.gems * 30/100
                    n_total_gems = n_addition_gems + i.gems+i.gems
                    winner.gems += n_total_gems
                    winner.save()
                    i.won = True
                    i.won_money = n_total_gems
                    i.save()

                    tran_history = Transtions(user = winner,status =True ,desc ='Win number' ,money='credit',fluctuate_gems = float(n_total_gems),
                    updates_gems = float(winner.gems) )
                    tran_history.save()

                    # check if reffer_by id present or not then transfer gems to reffer account
                    if winner.reffer_by != 'none':

                        # Getting user bu reffer id
                        reffer_user = User.objects.get(reffer_code = winner.reffer_by)
                        reffer_bonus  = i.gems * 5/100
                        
                        # Adding money to reffer money of user
                        reffer_user.Reffer_money += reffer_bonus

                        # Adding incentive to gems of reffer user
                        reffer_user.gems += reffer_bonus



                        # Total gems after adding incentive bonus


                        # Making trantion history
                        reffer_tran_history = Transtions(user = reffer_user,status=True ,desc ='reffer bonus' ,money='credit',fluctuate_gems = reffer_bonus,
                        updates_gems = reffer_user.gems )

                        reffer_tran_history.save()
                        reffer_user.save()


                    
        
        for i in data:
            i.expired = True
            i.save()

        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        from core.models import MazorCollection
        import json

        from django.utils.timezone import localtime
        if MazorCollection.objects.all().exists():
            channel_layer = get_channel_layer()
            latest = MazorCollection.objects.latest('created')
            date = localtime(latest.created)
    
            data = {
                'color': latest.color,
                'number':latest.number,
                'created':date.strftime("%I:%M"),
            }

            async_to_sync(channel_layer.group_send)(
                        'latest_history_group',{
                            'type':'latest_data',
                            'value': json.dumps(data)
                        }
                    )
            return "Task completed"
    else:
        return 'Break unique id error'



@shared_task(bind=True)
def countdown_handel(self):
    # fetching last time capture before creating new one
    if TimeCapture.objects.all().exists():
        fetch_id = TimeCapture.objects.latest('created')
        money_divider.delay(fetch_id.id)
    else:
        money_divider.delay('none')
    # creating another key id for next user collection
    eventid = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
    key_data = TimeCapture(key = eventid,time='init')
    key_data.save()
    for i in range(177):
        time.sleep(880/1000)
        if CountdownSeconds.objects.all().exists():
            count = CountdownSeconds.objects.all().first()
            count.sec = i
        else:
            count = CountdownSeconds(sec = i)
        count.save()
    return 'countdown initiated'
    