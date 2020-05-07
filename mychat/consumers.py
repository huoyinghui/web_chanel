#!/usr/bin/env python

import json

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import (
    WebsocketConsumer, AsyncJsonWebsocketConsumer,
    AsyncWebsocketConsumer,
    AsyncConsumer,
)
from django.contrib.auth.models import AnonymousUser

from mychat.models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def _save_message(self, message):
        if isinstance(self.user, AnonymousUser):
            user = None
        else:
            user = self.user
        obj, create = Message.objects.get_or_create(
            user=user,
            message=message,
        )
        print(f'obj:{obj} create:{create}')
        return obj

    async def save_message(self, message):
        await self._save_message(message)

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope["user"]
        print(f'connect: {self.room_name} user:{self.user}')

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        print(f'disconnect: {close_code}')
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print(f'receive:{self.user}: {text_data}')
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.save_message(message)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.get_user_name(),
            }
        )

    def get_user_name(self):
        if isinstance(self.user, AnonymousUser):
            username = str(self.user)
        else:
            username = self.user.username
        return username

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['sender']
        print(f'chat_message: {message}')
        print(f'sender: {username}')
        # Send message to WebSocket

        await self.send(text_data=json.dumps({
            'message': message,
            'user': username,
        }))


def main():
    pass


if __name__ == '__main__':
    main()
