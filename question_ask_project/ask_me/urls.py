from django.conf.urls import url
from ask_me.views import *

# app_name = 'ask_me'
urlpatterns = [
    url(r'^$', main),

    url(r'^feed/$', feed, name='feed'),
    url(r'^hot/$', hot, name='hot'),
    url(r'^tag/(?P<tag>.*)/$', tag, name='tag'),
    url(r'^question/(?P<question_id>[0-9]+)/$', question, name='question'),
    url(r'^question/(?P<question_id>[0-9]+)/answer/$', new_answer, name='new_answer'),

    url(r'^signin/$', signin, name='signin'),
    url(r'^signout/$', signout, name='signout'),
    url(r'^signup/$', signup, name='signup'),

    url(r'^ask/$', new_question, name='new_question'),
    url(r'^settings/$', settings, name='settings'),

    url(r'^question/delete/$', delete_question, name='delete_question'),
    url(r'^answer/delete/$', delete_answer, name='delete_answer'),

    url(r'^search/$', search, name='search')
]