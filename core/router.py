from .consumers import  *
from django.urls import path


ws_patterns =[
path('ws/live_sync/',LiveSync.as_asgi()),
path('ws/gems/<gem_id>',UserGems.as_asgi()),
path('ws/noti/',NotificationSocket.as_asgi()),
path('ws/latest_history',LatestHistorySocket.as_asgi()),
path('ws/countdown',CountDown.as_asgi()),

]