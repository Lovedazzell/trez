from django.urls import path

from . import views


urlpatterns = [
    path('addgems/',views.AddGems.as_view(),name = 'addgems'),
    path('withdraw/',views.WithDraw.as_view(),name = 'withdraw'),
    path('send_money_to/<int:pk>/',views.SendMoneyToUser.as_view(),name = 'send_money_to'),
    path('addbenificary/',views.AddBeneficary.as_view(),name = 'addbenificary'),

    # webhook urls
    path('phone_pay/',views.phone_pay),



    
]


