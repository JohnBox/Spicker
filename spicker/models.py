from django.db import models
from django.contrib.auth.models import User
from django.utils.text import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='profile',
                                verbose_name = _('user'))
    contacts = models.ManyToManyField('self',
                                      symmetrical=True,
                                      related_name='contacts',
                                      related_query_name='contact',
                                      verbose_name=_('contacts'))
    avatar = models.ImageField(_('avatar'), upload_to='avatar/')


class GroupMember(models.Model):
    profile = models.ForeignKey(Profile,
                                on_delete=models.CASCADE,
                                related_name='member',
                                verbose_name=_('profile'))
    group = models.ForeignKey('Group',
                              on_delete=models.CASCADE,
                              related_name='group',
                              verbose_name=_('group'))


class Group(models.Model):
    members = models.ManyToManyField(Profile,
                                     through=GroupMember,
                                     through_fields=('group', 'profile'),
                                     related_name='groups',
                                     verbose_name=_('members'))
    creator = models.ForeignKey(Profile,
                                on_delete=models.DO_NOTHING,
                                verbose_name=_('creator'))
    created = models.DateTimeField(_('created'), auto_now_add=True)


class Message(models.Model):
    group = models.ForeignKey(Group,
                              on_delete=models.CASCADE,
                              related_name='message',
                              verbose_name=_('group'))
    creator = models.ForeignKey(Profile,
                                on_delete=models.DO_NOTHING,
                                related_name='creator',
                                verbose_name=_('creator')),
    text = models.TextField(_('message text'))
    created = models.DateTimeField(_('created'), auto_now_add=True)


class Content(models.Model):
    class Meta:
        abstract = True
    message = models.ForeignKey(Message,
                                on_delete=models.CASCADE,
                                verbose_name=_('message'))


class FileContent(Content):
    file = models.FileField(_('message file'), upload_to='files/')


class ImageContent(Content):
    image = models.ImageField(_('message image'), upload_to='images/')


class VideoCall(models.Model):
    group = models.ForeignKey(Group,
                              on_delete=models.CASCADE,
                              related_name='video_call',
                              verbose_name=_('group'))
    created = models.DateTimeField(_('created'), auto_now_add=True)
    finished = models.DateTimeField(_('finished'), blank=True, default=None)
    duration = models.DurationField(_('duration'), blank=True, default=None)
