import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_ID = self.scope['url_route']['kwargs']['roomId'] # obtaining the 'roomId' parameter from the guestChatRoom routing of its websocket connection
        self.room_group_name = 'chatRoom_%s' % self.room_ID # creating the group name based on the roomID
        
        self.accept()
    
    def disconnect(self, close_code):
        pass
    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.send(text_data=json.dumps({
            'message': message
        }))

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # async def connect(self):
    #     self.room_ID = self.scope['url_route']['kwargs']['roomId'] # obtaining the 'roomId' parameter from the guestChatRoom routing of its websocket connection
    #     self.room_group_name = 'chatRoom_%s' % self.room_ID # creating the group name based on the roomID
        
    #     # joining room group
    #     await self.channel_layer.group_add(
    #         self.room_group_name,
    #         self.channel_name
    #     )
    #     await self.accept()
    
    # # leaving group
    # async def disconnect(self, close_code):
    #     await self.channel_layer.group_discard(
    #         self.room_group_name,
    #         self.channel_name
    #     )
    
    # # receiving message from WebSocket
    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']
        
    #     # sending message to the room group
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             'type': 'chat_message',
    #             'message': message
    #         }
    #     )
    
    # # receiving message from the room group (custom made type used in receive.group_send['type'])
    # async def chat_message(self, event):
    #     message = event['message']
        
    #     # sending message to the websocket
    #     await self.send(
    #         text_data=json.dumps(
    #             {
    #                 'message':message
    #             }
    #         )
    #     )
