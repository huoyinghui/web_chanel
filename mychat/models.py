from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
User = get_user_model()


class Message(models.Model):
    """
    app活动分类:
        1.运动活动
        2.主题活动
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='message',
        help_text='用户',
        null=True,
        blank=True,
    )
    message = models.TextField(_('message'), max_length=1024, help_text='内容')

    is_deleted = models.BooleanField(_('is_deleted'),
                                     default=False, help_text=u'是否删除')
    create_time = models.DateTimeField(_('create time'),
                                       help_text='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(_('update time'),
                                       help_text='更新时间', auto_now=True)

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Message')

    def __str__(self):
        return str(self.id)
