#!/usr/bin/env python

import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import (
    WebsocketConsumer, AsyncJsonWebsocketConsumer,
    AsyncWebsocketConsumer,
    AsyncConsumer,
)


class ChatConsumer(AsyncWebsocketConsumer):
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
        username = self.user.username if self.user.username else '匿名'
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
