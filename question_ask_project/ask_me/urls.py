from django.conf.urls import url
from ask_me.views import *

# app_name = 'ask_me'
urlpatterns = [
    url(r'^$', main),
    url(r'^feed/$', feed, name='feed'),
    url(r'^hot/$', hot, name='hot'),
    url(r'^tag/bender/$', tag, name='tag'),

    url(r'^question/(?P<question_id>[0-9]+)/$', question, name='question'),
    url(r'^login/$', login, name='login'),
    url(r'^registration/$', registration, name='registration'),
    url(r'^ask/$', new_ask, name='new_ask'),
    url(r'^settings/$', settings, name='settings')
]

