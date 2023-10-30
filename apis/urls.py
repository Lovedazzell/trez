from django.urls import path
from . import views




urlpatterns = [
    
    path('payment_v/',views.PaymentVerify,name = 'payment_v'),
    path('spent_gems/',views.spent_gems,name = 'spent_gems'),
    path('support/',views.support,name = 'support'),


    path('profile_update/',views.profile_update,name = 'profile_update'),
   
    
    path('add_beneficery/',views.add_beneficery,name = 'add_beneficery'),


    path('add_reff/',views.add_refference_code,name = 'add_reff'),
    path('money_record/',views.money_record,name = 'money_record'),
]





