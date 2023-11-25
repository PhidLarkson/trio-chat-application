import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Room
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_name


        # await self.get_room()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        # self.message.reply_channel.send({"accept": True})

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        room = text_data_json['room']

        await self.save_message(sender, room, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'room': room,
            }
        )
    
    async def chat_message(self, event):

        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': event['message'],
            'sender': event['sender']
        }))

    @sync_to_async
    def get_room(self):
        return Room.objects.get(id=self.room_name)

    @sync_to_async
    def save_message(self, sender, room, message):
        room = Room.objects.get(id=room)
        user = User.objects.get(username=sender)

        message = Message.objects.create(sender=user, room=room, content=message)
