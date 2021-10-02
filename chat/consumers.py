import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


"""
a websocket consumer that accepts websocket connection,
receives message from the client, and echoes the message back to the client
"""
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name'] # binding the room_name from ChatConsumer routing to self.room
        self.room_group_name = 'chat_%s' %  self.room_name
        
        # adding channel to group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
    
    def disconnect(self, close_code):
        # removing channel from group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    
    def receive(self, text_data):
        text_data_json = json.loads(text_data) # deserializing the text data from json format and converting to python object
        message = text_data_json['message']
        
        #sending message to the room group
        async_to_sync(self.channel_layer.group_send)( # making async channels method synchronous
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }

        )
        
    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

        # self.send(text_data=json.dumps( # serializing the text data to json format for sending
        #     {
        #         'message': message
        #     }
        # ))
