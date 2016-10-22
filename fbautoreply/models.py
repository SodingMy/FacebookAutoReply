from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible  # only if you need to support Python 2
class FacebookAccount(models.Model):
    user = models.ForeignKey(User)
    account_description = models.CharField(max_length=50)
    facebook_application_id = models.CharField(max_length=50)
    facebook_application_secret = models.CharField(max_length=50)
    ouath_token = models.CharField(max_length=500)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.account_description

@python_2_unicode_compatible  # only if you need to support Python 2
class FacebookFanPage(models.Model):
    facebook_account = models.ForeignKey(FacebookAccount)
    fan_page_description = models.CharField(max_length=50)
    fan_page_id = models.CharField(max_length=30)
    fan_page_access_token = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.fan_page_description
9
@python_2_unicode_compatible  # only if you need to support Python 2
class PredefinedMessage(models.Model):
    user = models.ForeignKey(User)
    list_name = models.CharField(max_length=50)
    list_description = models.CharField(max_length=50)

    def __str__(self):
        return self.list_name

class PredefinedMessageDetail(models.Model):
    predefined_message_detail = models.ForeignKey(PredefinedMessage)
    message = models.CharField(max_length=5000)

class Campaign(models.Model):
    aList = (
        ('1', 'Send replies to inbox messages'),
        ('2', 'Post replies to users comments')
    )
    user = models.ForeignKey(User)
    campaign_name = models.CharField(max_length=50)
    autoresponder_type = models.CharField(max_length=10, choices=aList, null=True)
    facebook_account_to_use = models.ForeignKey(FacebookAccount)
    set_auto_reply_for_fan_page = models.ForeignKey(FacebookFanPage)
    message_list_to_use = models.ForeignKey(PredefinedMessage)
    #reply_only_in_this_hourly_interval
    reply_only_for_this_keyword = models.CharField(max_length=50, null=True)

class ArchiveMessage(models.Model):
    sender_id = models.IntegerField()
    recipient_id = models.IntegerField()
    message_text = models.CharField(max_length=5000)
    response_text = models.CharField(max_length=5000, null=True)

class ResponseMessage(models.Model):
    message_text = models.CharField(max_length=5000)