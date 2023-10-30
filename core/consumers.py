import json
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer ,InvalidChannelLayerError


# send live data to admin

class LiveSync(WebsocketConsumer):

    def connect(self):
        self.room_name = 'live_data'
        self.room_group_name = 'live_data_group'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name , self.channel_name
        )
        self.accept()
        
     
    def receive(self,text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{
                'type':'live_sync',
                'payload':text_data
            }
        )

    def live_sync(self,event):
        data = json.loads(event['value'])
        self.send(text_data=json.dumps({
            'payload':data
        }))

    def websocket_disconnect(self, message):
        """
        Called when a WebSocket connection is closed. Base level so you don't
        need to call super() all the time.
        """
        try:
            for group in self.groups:
                async_to_sync(self.channel_layer.group_discard)(
                    group, self.channel_name
                )
        except AttributeError:
            raise InvalidChannelLayerError(
                "BACKEND is unconfigured or doesn't support groups"
            )
        self.disconnect(message["code"])
        raise StopConsumer()

    def disconnect(self):
        pass
     


class CountDown(WebsocketConsumer):

    def connect(self):
        self.room_name = 'live_count'
        self.room_group_name = 'live_count_group'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name , self.channel_name
        )
        self.accept()
      
     
    def receive(self,text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{
                'type':'countdown_data',
                'payload':text_data
            }
        )

    def countdown_data(self,event):
        data = json.loads(event['value'])
        self.send(text_data=json.dumps({
            'payload':data
        }))


    def websocket_disconnect(self, message):
        """
        Called when a WebSocket connection is closed. Base level so you don't
        need to call super() all the time.
        """
        try:
            for group in self.groups:
                async_to_sync(self.channel_layer.group_discard)(
                    group, self.channel_name
                )
        except AttributeError:
            raise InvalidChannelLayerError(
                "BACKEND is unconfigured or doesn't support groups"
            )
        self.disconnect(message["code"])
        raise StopConsumer()

    def disconnect(self):
        pass
     


# return recent spends to user
class UserGems(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['gem_id']      
        self.room_group_name = 'gems_%s'%self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name , self.channel_name
        )

        self.accept()
      
     
    def receive(self,text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{
                'type':'gems_data',
                'payload':text_data
            }
        )

    def gems_data(self,event):
        spend = json.loads(event['value'])
        self.send(text_data=json.dumps({
            'payload':spend
        }))

    def websocket_disconnect(self, message):
        """
        Called when a WebSocket connection is closed. Base level so you don't
        need to call super() all the time.
        """
        try:
            for group in self.groups:
                async_to_sync(self.channel_layer.group_discard)(
                    group, self.channel_name
                )
        except AttributeError:
            raise InvalidChannelLayerError(
                "BACKEND is unconfigured or doesn't support groups"
            )
        self.disconnect(message["code"])
        raise StopConsumer()

    def disconnect(self):
        pass
     

class NotificationSocket(WebsocketConsumer):

    def connect(self):
        self.room_name = 'all_user_notify'      
        self.room_group_name = 'all_user_notify_group'


        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name , self.channel_name
        )
       
      
        self.accept()

     

    def receive(self,text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{
                'type':'notify_data',
                'payload':text_data
            }
        )

    def notify_data(self,event):
        notification_data= json.loads(event['value'])
        self.send(text_data=json.dumps({
            'payload':notification_data
        }))
        
    def websocket_disconnect(self, message):
        """
        Called when a WebSocket connection is closed. Base level so you don't
        need to call super() all the time.
        """
        try:
            for group in self.groups:
                async_to_sync(self.channel_layer.group_discard)(
                    group, self.channel_name
                )
        except AttributeError:
            raise InvalidChannelLayerError(
                "BACKEND is unconfigured or doesn't support groups"
            )
        self.disconnect(message["code"])
        raise StopConsumer()

    def disconnect(self,code):
        pass
        


class LatestHistorySocket(WebsocketConsumer):

    def connect(self):
        self.room_name = 'latest_history_room'    
        self.room_group_name = 'latest_history_group'


        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name , self.channel_name
        )
       
      
        self.accept()

     

    def receive(self,text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{
                'type':'latest_data',
                'payload':text_data
            }
        )

    def latest_data(self,event):
        latest_notification_data= json.loads(event['value'])
        self.send(text_data=json.dumps({
            'payload':latest_notification_data
        }))
        

    def websocket_disconnect(self, message):
        """
        Called when a WebSocket connection is closed. Base level so you don't
        need to call super() all the time.
        """
        try:
            for group in self.groups:
                async_to_sync(self.channel_layer.group_discard)(
                    group, self.channel_name
                )
        except AttributeError:
            raise InvalidChannelLayerError(
                "BACKEND is unconfigured or doesn't support groups"
            )
        self.disconnect(message["code"])
        raise StopConsumer()

    def disconnect(self):
       pass