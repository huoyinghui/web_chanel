#!/usr/bin/env python

from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/room/(?P<room_name>\w+)/$', consumers.ChatConsumer),
]


def main():
    pass


if __name__ == '__main__':
    main()
