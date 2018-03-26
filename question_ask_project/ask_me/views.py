from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from ask_me.models import *


def main(request):
	return redirect('feed')


def feed(request):
	return render(request, 'feed.html',
                  {'questions': paginator(request, objects_list=Question.objects.get_new()),
				   'headers': header_content("new")
				   })


def hot(request):
	return render(request, 'feed.html',
				  {'questions': paginator(request, objects_list=Question.objects.get_hot()),
				   'headers': header_content("hot")
				   })


def tag(request, tag):
	return render(request, 'feed.html',
				  {'questions': paginator(request, objects_list=Tag.objects.get_by_tag(tag_name=tag)),
				   'headers': header_content("tag", tag_name=tag)
				   })


def question(request, question_id):
	question = Question.objects.get_by_id(int(question_id)).first()
	answers = paginator(request, Answer.objects.get_answers_hot(question.id))
	if question is not None:
		return render(request, 'question.html', {'question': question, 'answers': answers})
	else:
		raise Http404


#TODO
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



def paginator(request, objects_list):
	paginator = Paginator(objects_list, 20)  # Show 20 contacts per page

	page = request.GET.get('page')

	try:
		objects = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		objects = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		objects = paginator.page(paginator.num_pages)

	return objects


def header_content(type, tag_name=""):
    if (type == "new"):
        content_header = [
            {'title': 'New Questions', 'url': 'feed', 'is_active': True},
            {'title': 'Hot Questions', 'url': 'hot', 'is_active': False}
        ]
    if (type == "hot"):
        content_header = [
            {'title': 'New Questions', 'url': 'feed', 'is_active': False},
            {'title': 'Hot Questions', 'url': 'hot', 'is_active': True}
        ]
    if (type == "tag"):
        content_header = [
            {'title': 'Tag: ' + tag_name, 'url': 'feed', 'is_active': True},
        ]
    return content_header