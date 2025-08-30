import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from circles.models import Circle


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.circle_id = self.scope['url_route']['kwargs']['circle_id']
        self.circle_group_name = f'chat_{self.circle_id}'

        await self.channel_layer.group_add(
            self.circle_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.circle_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        profile = self.scope['user'].profile

        new_message = await self.save_message(self.circle_id, profile, message)

        await self.channel_layer.group_send(
            self.circle_group_name,
            {
                'type': 'chat_message',
                'content': new_message.content,
                'profile': profile.user.username,
                'timestamp': new_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps({
                'profile': event['profile'],
                'content': event['content'],
                'timestamp': event['timestamp']
            })
        )

    @database_sync_to_async
    def save_message(self, circle_id, profile, content):
        circle = Circle.objects.get(id=circle_id)
        return Message.objects.create(
            circle=circle,
            profile=profile,
            content=content
        )
