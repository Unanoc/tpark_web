from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from ask_me.models import *

def main(request):
	return redirect('feed')


def feed(request):
	return render_paginator(request, question_list=Question.objects.get_new(), content_header=[
		{'title': 'New Questions', 'url': 'feed', 'class': 'new'},
        {'title': 'Hot Questions', 'url': 'hot', 'class': 'hot'}
    ])


def hot(request):
	return render_paginator(request, question_list=Question.objects.get_hot(), content_header=[
        {'title': 'Hot Questions', 'url': 'hot', 'class': 'hot'},
        {'title': 'New Questions', 'url': 'feed', 'class': 'new'}
    ])


def tag(request, tag):
	return render_paginator(request, question_list=Tag.objects.get_by_tag(tag_name=tag), content_header=[
        {'title': 'Tag: ' + tag, 'url': 'feed', 'class': 'tag-header'},
    ])


def question(request, question_id):
	question = Question.objects.get_by_id(int(question_id)).first()
	if question is not None:
		return render(request, 'question.html', {'question': question})
	else:
		raise Http404









def login(request):
	return HttpResponse(render_to_string('login.html'))



def logout(request):
	return redirect('feed')

def registration(request):
	return HttpResponse(render_to_string('registration.html'))

def new_ask(request):
	return HttpResponse(render_to_string('new_question.html'))

def settings(request):
	return HttpResponse(render_to_string('settings.html'))








def render_paginator(request, question_list, content_header = ''):
	paginator = Paginator(question_list, 20)  # Show 25 contacts per page

	page = request.GET.get('page')

	try:
		questions = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		questions = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		questions = paginator.page(paginator.num_pages)

	return render(request, 'feed.html',
                  {'questions': questions,
				   'headers': content_header
				   })
