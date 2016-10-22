"""FacebookAutoReply URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from fbautoreply import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.model_activation.urls')),
    url(r'^$', views.home, name='home'),
    url(r'^facebookaccount$', views.facebook_account_list, name='facebook_account_list'),
    url(r'^facebookaccount/new$', views.facebook_account_create, name='facebook_account_new'),
    url(r'^facebookaccount/edit/(?P<pk>\d+)$', views.facebook_account_update, name='facebook_account_edit'),
    url(r'^facebookaccount/delete/(?P<pk>\d+)$', views.facebook_account_delete, name='facebook_account_delete'),
    url(r'^facebookfanpage$', views.facebook_fan_page_list, name='facebook_fan_page_list'),
    url(r'^facebookfanpage/new$', views.facebook_fan_page_new, name='facebook_fan_page_new'),
    url(r'^predefinedmessage$', views.predefined_message_list, name='predefined_message_list'),
    url(r'^predefinedmessage/new$', views.predefined_message_create, name='predefined_message_new'),
    url(r'^predefinedmessage/edit/(?P<pk>\d+)$', views.predefined_message_update, name='predefined_message_edit'),
    url(r'^predefinedmessage/delete/(?P<pk>\d+)$', views.predefined_message_delete, name='predefined_message_delete'),
    url(r'^predefinedmessagedetail/(?P<pk>\d+)$', views.predefined_message_detail_list, name='predefined_message_detail_list'),
    url(r'^predefinedmessagedetail/new$', views.predefined_message_detail_create, name='predefined_message_detail_new'),
    url(r'^predefinedmessagedetail/edit/(?P<pk>\d+)$', views.predefined_message_detail_update, name='predefined_message_detail_edit'),
    url(r'^predefinedmessagedetail/delete/(?P<pk>\d+)$', views.predefined_message_detail_delete, name='predefined_message_detail_delete'),
    url(r'^autoresponder$', views.autoresponder_list, name='autoresponder_list'),
    url(r'^autoresponder/new$', views.autoresponder_create, name='autoresponder_new'),
    url(r'^autoresponder/edit/(?P<pk>\d+)$', views.autoresponder_update, name='autoresponder_edit'),
    url(r'^autoresponder/delete/(?P<pk>\d+)$', views.autoresponder_delete, name='autoresponder_delete'),
    url(r'^api/messages$', views.message_detail.as_view()),
]