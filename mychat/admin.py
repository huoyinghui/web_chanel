from django.contrib import admin

from mychat.models import (
    Message,
)
# Register your models here.


@admin.register(Message)
class AppActivityTypeAdmin(admin.ModelAdmin):
    search_fields = ('id',)
    ordering = ('id',)
    list_display = ['id', 'user', 'message',
                    'is_deleted', 'create_time', 'update_time'
                    ]
