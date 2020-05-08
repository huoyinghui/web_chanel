#!/usr/bin/env python


from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('room/<str:room_name>/', views.room, name='room'),
    path('p2p/', views.p2p, name='p2p'),
]


def main():
    pass


if __name__ == '__main__':
    main()
