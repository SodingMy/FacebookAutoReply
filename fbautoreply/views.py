from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.shortcuts import render
from fbautoreply.models import FacebookAccount
from fbautoreply.models import FacebookFanPage
from fbautoreply.models import PredefinedMessage
from fbautoreply.models import PredefinedMessageDetail
from fbautoreply.models import Campaign
from fbautoreply.models import ArchiveMessage
from fbautoreply.models import ResponseMessage
import json
import urllib2
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from fbautoreply.serializers import MessageSerializer
import random

# Create your views here.

def home(request):
    return render(request, 'home.html', {})

class FacebookAccountForm(ModelForm):
    class Meta:
        model = FacebookAccount
        fields = ['account_description', 'facebook_application_id', 'facebook_application_secret','ouath_token']
        exclude = ('user','status',)

def facebook_account_list(request, template_name='facebook-resources/facebook-accounts/facebook_account_list.html'):
    if not request.user.is_authenticated():
        return redirect('home')
    facebook_accounts = FacebookAccount.objects.all().filter(user=request.user)
    data = {}
    data['object_list'] = facebook_accounts
    return render(request, template_name, data)

def facebook_account_create(request, template_name='facebook-resources/facebook-accounts/facebook_account_form.html'):
    if not request.user.is_authenticated():
        return redirect('home')
    form = FacebookAccountForm(request.POST or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.user = request.user
        form.save()
        return redirect('facebook_account_list')
    return render(request, template_name, {'form':form})

def facebook_account_update(request, pk, template_name='facebook-resources/facebook-accounts/facebook_account_form.html'):
    if not request.user.is_authenticated():
        return redirect('home')
    facebook_account = get_object_or_404(FacebookAccount, pk=pk)
    form = FacebookAccountForm(request.POST or None, instance=facebook_account)
    if form.is_valid():
        form.save()
        return redirect('facebook_account_list')
    return render(request, template_name, {'form':form})

def facebook_account_delete(request, pk, template_name='facebook-resources/facebook-accounts/facebook_account_confirm_delete.html'):
    if not request.user.is_authenticated():
        return redirect('home')
    facebook_account = get_object_or_404(FacebookAccount, pk=pk)
    if request.method=='POST':
        facebook_account.delete()
        return redirect('facebook_account_list')
    return render(request, template_name, {'object':facebook_account})

def facebook_fan_page_list(request, template_name='facebook-resources/facebook-fan-pages/facebook_fan_page_list.html'):
    if not request.user.is_authenticated():
        return redirect('home')
    facebook_fan_pages =  FacebookFanPage.objects.raw('SELECT * '
                                             'FROM fbautoreply_facebookfanpage '
                                             'JOIN fbautoreply_facebookaccount ON fbautoreply_facebookfanpage.facebook_account_id = fbautoreply_facebookaccount.id '
                                             'WHERE fbautoreply_facebookaccount.user_id = %s ', [str(request.user.id)])

    data = {}
    data['object_list'] = facebook_fan_pages
    return render(request, template_name, data)

def facebook_fan_page_new(request):
    if not request.user.is_authenticated():
        return redirect('home')
    data1 = {}
    data1['object_list'] = FacebookAccount.objects.all().filter(user=request.user)
    for facebook_account in data1['object_list']:
        data2 = json.load(urllib2.urlopen("https://graph.facebook.com/v2.7/me/accounts?access_token="+facebook_account.ouath_token))
        for j in data2['data']:
            data3 = {}
            data3['object_list'] = FacebookFanPage.objects.all().filter(fan_page_id=j['id'])
            if data3['object_list'].count() == 0:
                facebook_fan_page = FacebookFanPage()
                facebook_fan_page.facebook_account = facebook_account
                facebook_fan_page.fan_page_description = j['name']
                facebook_fan_page.fan_page_id = j['id']
                facebook_fan_page.fan_page_access_token = j['access_token']
                facebook_fan_page.save()
    return redirect('facebook_fan_page_list')

class PredefinedMessageForm(ModelForm):
    class Meta:
        model = PredefinedMessage
        fields = ['list_name', 'list_description']
        exclude = ('user',)

def predefined_message_list(request, template_name='predefined-message/predefined_message_list.html'):
    if not request.user.is_authenticated():
        return redirect('home')
    predefined_messages = PredefinedMessage.objects.all().filter(user=request.user)
    data = {}
    data['object_list'] = predefined_messages
    return render(request, template_name, data)

def predefined_message_create(request, template_name='predefined-message/predefined_message_form.html'):
    if not request.user.is_authenticated():
        return redirect('home')
    form = PredefinedMessageForm(request.POST or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.user = request.user
        form.save()
        return redirect('predefined_message_list')
    return render(request, template_name, {'form':form})

def predefined_message_update(request, pk, template_name='predefined-message/predefined_message_form.html'):
    if not request.user.is_authenticated():
        return redirect('home')
    predefined_message = get_object_or_404(PredefinedMessage, pk=pk)
    form = PredefinedMessageForm(request.POST or None, instance=predefined_message)
    if form.is_valid():
        form.save()
        return redirect('predefined_message_list')
    return render(request, template_name, {'form':form})

def predefined_message_delete(request, pk, template_name='predefined-message/predefined_message_confirm_delete.html'):
    if not request.user.is_authenticated():
        return redirect('home')
    predefined_message = get_object_or_404(PredefinedMessage, pk=pk)
    if request.method=='POST':
        predefined_message.delete()
        return redirect('predefined_message_list')
    return render(request, template_name, {'object':predefined_message})

class PredefinedMessageDetailForm(ModelForm):
    class Meta:
        model = PredefinedMessageDetail
        fields = ['predefined_message_detail', 'message']
        exclude = ('user',)

def predefined_message_detail_list(request, pk, template_name='predefined-message/predefined_message_detail_list.html'):
    if not request.user.is_authenticated():
        return redirect('home')

    predefined_message_details = FacebookFanPage.objects.raw('SELECT * '
                                             'FROM fbautoreply_predefinedmessagedetail '
                                             'JOIN fbautoreply_predefinedmessage ON fbautoreply_predefinedmessagedetail.predefined_message_detail_id = fbautoreply_predefinedmessage.id '
                                             'WHERE fbautoreply_predefinedmessage.user_id = %s ', [str(request.user.id)])

    data = {}
    data['object_list'] = predefined_message_details
    return render(request, template_name, data)

def predefined_message_detail_create(request, template_name='predefined-message/predefined_message_detail_form.html'):
    if not request.user.is_authenticated():
        return redirect('home')
    form = PredefinedMessageDetailForm(request.POST or None)
    form.fields["predefined_message_detail"].queryset = PredefinedMessage.objects.filter(user=request.user)
    if form.is_valid():
        form = form.save(commit=False)
        form.user = request.user
        form.save()
        return redirect('predefined_message_list')
    return render(request, template_name, {'form':form})

def predefined_message_detail_update(request, pk, template_name='predefined-message/predefined_message_detail_form.html'):
    if not request.user.is_authenticated():
        return redirect('home')
    predefined_message_detail = get_object_or_404(PredefinedMessageDetail, pk=pk)
    form = PredefinedMessageDetailForm(request.POST or None, instance=predefined_message_detail)
    form.fields["predefined_message_detail"].queryset = PredefinedMessage.objects.filter(user=request.user)
    if form.is_valid():
        form.save()
        return redirect('predefined_message_list')
    return render(request, template_name, {'form':form})

def predefined_message_detail_delete(request, pk, template_name='predefined-message/predefined_message_detail_confirm_delete.html'):
    if not request.user.is_authenticated():
        return redirect('home')
    predefined_message_detail = get_object_or_404(PredefinedMessageDetail, pk=pk)
    if request.method=='POST':
        predefined_message_detail.delete()
        return redirect('predefined_message_list')
    return render(request, template_name, {'object':predefined_message_detail})

class AutoresponderForm(ModelForm):
    class Meta:
        model = Campaign
        fields = ['campaign_name','autoresponder_type','facebook_account_to_use','set_auto_reply_for_fan_page','message_list_to_use','reply_only_for_this_keyword']
        exclude = ('user',)

def autoresponder_list(request, template_name='autoresponder/autoresponder_list.html'):
    if not request.user.is_authenticated():
        return redirect('home')
    campaigns = Campaign.objects.all().filter(user=request.user)
    data = {}
    data['object_list'] = campaigns
    return render(request, template_name, data)

def autoresponder_create(request, template_name='autoresponder/autoresponder_form.html'):
    if not request.user.is_authenticated():
        return redirect('home')
    form = AutoresponderForm(request.POST or None)
    form.fields["facebook_account_to_use"].queryset = FacebookAccount.objects.filter(user=request.user)
    form.fields["set_auto_reply_for_fan_page"].query = FacebookFanPage.objects.raw('SELECT * '
                                             'FROM fbautoreply_facebookfanpage '
                                             'JOIN fbautoreply_facebookaccount ON fbautoreply_facebookfanpage.facebook_account_id = fbautoreply_facebookaccount.id '
                                             'WHERE fbautoreply_facebookaccount.user_id = %s ', [str(request.user.id)])
    form.fields["message_list_to_use"].queryset = PredefinedMessage.objects.filter(user=request.user)
    if form.is_valid():
        form = form.save(commit=False)
        form.user = request.user
        form.save()
        return redirect('autoresponder_list')
    return render(request, template_name, {'form':form})

def autoresponder_update(request, pk, template_name='autoresponder/autoresponder_form.html'):
    if not request.user.is_authenticated():
        return redirect('home')
    campaign = get_object_or_404(Campaign, pk=pk)
    form = AutoresponderForm(request.POST or None, instance=campaign)
    form.fields["facebook_account_to_use"].queryset = FacebookAccount.objects.filter(user=request.user)
    form.fields["set_auto_reply_for_fan_page"].query = FacebookFanPage.objects.raw('SELECT * '
                                             'FROM fbautoreply_facebookfanpage '
                                             'JOIN fbautoreply_facebookaccount ON fbautoreply_facebookfanpage.facebook_account_id = fbautoreply_facebookaccount.id '
                                             'WHERE fbautoreply_facebookaccount.user_id = %s ', [str(request.user.id)])
    form.fields["message_list_to_use"].queryset = PredefinedMessage.objects.filter(user=request.user)
    if form.is_valid():
        form.save()
        return redirect('autoresponder_list')
    return render(request, template_name, {'form':form})

def autoresponder_delete(request, pk, template_name='autoresponder/autoresponder_confirm_delete.html'):
    if not request.user.is_authenticated():
        return redirect('home')
    campaign = get_object_or_404(Campaign, pk=pk)
    if request.method=='POST':
        campaign.delete()
        return redirect('autoresponder_list')
    return render(request, template_name, {'object':campaign})

class message_detail(APIView):
    """
    Retrieve, update or delete a message instance.
    """
    def get_object(self, pk):
        try:
            return Campaign.objects.get(pk=pk)
        except Campaign.DoesNotExist:
            raise Http404

    def get(self, request):

        string = []

        access_token = request.GET.get('access_token', '')
        set_auto_reply_for_fan_page = request.GET.get('set_auto_reply_for_fan_page', '')
        for f in Campaign.objects.raw('SELECT * '
                                             'FROM fbautoreply_campaign '
                                             'JOIN fbautoreply_facebookaccount ON fbautoreply_campaign.id = fbautoreply_facebookaccount.id '
                                             'JOIN fbautoreply_facebookfanpage ON fbautoreply_facebookaccount.id = fbautoreply_facebookfanpage.facebook_account_id '
                                             'JOIN fbautoreply_predefinedmessage ON fbautoreply_campaign.id = fbautoreply_predefinedmessage.id '
                                             'JOIN fbautoreply_predefinedmessagedetail ON fbautoreply_predefinedmessage.id = fbautoreply_predefinedmessagedetail.predefined_message_detail_id '
                                             'WHERE fbautoreply_facebookfanpage.fan_page_id = %s  AND '
                                             'fbautoreply_facebookaccount.ouath_token = %s ', [set_auto_reply_for_fan_page , access_token]):

            keyword = f.reply_only_for_this_keyword
            string.append(f.message)

        if keyword in request.GET.get('message_text', ''):
            response_message = ResponseMessage(message_text=random.choice(string))
        else:
            response_message = ResponseMessage(message_text="Not exist")

        serializer = MessageSerializer(response_message)
        print serializer.data
        return Response(serializer.data)
"""
        m = ArchiveMessage(sender_id = request.GET.get('sender_id', ''),
                    recipient_id = request.GET.get('recipient_id', ''),
                    message_text = request.GET.get('message_text', ''),
                    response_text = request.GET.get('reply_only_for_this_keyword', ''))
        m.save()
"""

"""

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = MessageSerializer(user, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""