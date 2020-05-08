#!/usr/bin/env python


from django.urls import path

from . import views

urlpatterns = [
    path('', views.video_index, name='video_index'),
    path('feed/', views.video_feed, name='video_feed'),
]


def main():
    pass


if __name__ == '__main__':
    main()
