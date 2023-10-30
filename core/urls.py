from django.urls import path,include
from froala_editor import views
from . import views


urlpatterns = [
    path('',views.Profile.as_view(),name = 'profile'),
    path('profile/',views.Profile.as_view(),name = 'profile'),

    path('tmc/',views.ThreeMinutesCount.as_view(),name = 'tmc'),
   
    path('settings/',views.Settings.as_view(),name = 'settings'),
    path('market/',views.MarketPlace.as_view(),name = 'market'),
    path('notifications/',views.Notifications.as_view(),name = 'notifications'),
    path('transitions/',views.UserTransitions.as_view(),name = 'transitions'),

    

    path('reffer_data/',views.RefferData.as_view(),name = 'reffer_data'),
    path('tran_detail/<int:pk>/',views.TransitionDetail.as_view(),name = 'tran_detail'),

    

    path('notifi_dis/<int:pk>/',views.NotificationDisplay.as_view(),name = 'notifi_dis'),
 
    

    path('gemshistory/',views.UserGems.as_view(),name = 'gemshistory'),
    path('world_history/',views.WorldHistory.as_view(),name = 'world_history'),


    path('froala_editor/',include('froala_editor.urls'))
]

