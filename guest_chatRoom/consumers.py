import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync
from guest_chatRoom.views import room_messages

from users.models import CustomUser  # package for converting async methods to sync
from .models import Message, GuestChatRoom

class ChatConsumer(WebsocketConsumer):
    
    # fetching the json of messages that will be displayed in chat_detail
    def fetch_messages(self, data):
        # messages = Message.last_10_messages(self)
        room = GuestChatRoom.objects.get(id=self.room_ID)
        messages = Message.objects.filter(room=room)
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)
    
    def new_message(self, data):
        user_id = self.scope["user"].id
        sender = CustomUser.objects.get(id=user_id)
        room = GuestChatRoom.objects.get(id=self.room_ID)
        message = Message.objects.create(
            room = room,
            sender = sender,
            content = data['message']
        )
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)
    
    # returning all json format of message
    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result
    
    # converting each message to json format
    def message_to_json(self, message):
        return {
            'sender': message.sender.first_name,
            'content': message.content,
            'timestamp': str(message.timestamp),
        }
    
    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
    }
        
    def connect(self):
        self.room_ID = self.scope['url_route']['kwargs']['roomId'] # obtaining the 'roomId' parameter from the guestChatRoom routing of its websocket connection
        self.room_group_name = 'chatRoom_%s' % self.room_ID # creating the group name based on the roomID
        
        
        # converting asynchronous channel_layer to synchronous and joining the room group...  
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()
    
    def disconnect(self,close_code): # disconnect from the websocket connection
        # leaving the room
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    
    
    # the receive function receives data from any command given in the command dictionary
    def receive(self, text_data): # receiving message from the websocket
        data = json.loads(text_data)
        self.commands[data['command']](self, data)
        
        
    def send_chat_message(self, message):
        # sending message to room
        
        # room = GuestChatRoom.objects.get(id=self.room_ID)
        # Message.objects.create(content=message, sender=self.scope["user"], room=room)
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )
    # receiving older messages from the group
    def send_message(self, message):
        self.send(text_data=json.dumps(message))
    
    # receiving new message from the group
    def chat_message(self, event): # creating a custom event for each channel in the channel layer
        message = event['message']
        user_id = self.scope["user"].id
        sender = CustomUser.objects.get(id=user_id)
        
        #sending message to the Websocket
        self.send(text_data=json.dumps(message))
    
    # def store_message(self, message):
    #     room = GuestChatRoom.objects.get(id=self.room_ID)
    #     Message.objects.create(content=message, sender=self.scope["user"], room=room)
    
    # def fetch_messages(self, message):
    #     room = GuestChatRoom.objects.get(id=self.room_ID)
    #     room_messages = Message.objects.filter(room=room)
        
        
        # room = GuestChatRoom.objects.get(id=self.room_ID)
        # message = Message.objects.create(content=message, sender=sender, room=room)
        # message.save()
        
    
    
    
    
    
    
    
    
    # 2nd consumer edition
    # def connect(self):
    #     self.room_ID = self.scope['url_route']['kwargs']['roomId'] # obtaining the 'roomId' parameter from the guestChatRoom routing of its websocket connection
    #     self.room_group_name = 'chatRoom_%s' % self.room_ID # creating the group name based on the roomID
        
    #     self.accept()
    
    # def disconnect(self, close_code):
    #     pass
    
    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']
    #     self.send(text_data=json.dumps({
    #         'message': message
    #     }))

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # 1st consumer edition
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
