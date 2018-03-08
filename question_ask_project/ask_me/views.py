from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def main(request):
	return redirect('feed')


def feed(request):
	questions = []
	for i in range(1, 60):
		questions.append({
			'id': i,
			'title': 'Вопрос №' + str(i),
			'content': 'Now we might be able to get away with putting our templates directly in polls/templates '
                       '(rather than creating another polls subdirectory), but it would actually be a bad idea. '
                       'Django will choose the first template it finds whose name matches, and if you had a template '
                       'with the same name in a different application, Django would be unable to distinguish between '
                       'them. We need to be able to point Django at the right one, and the easiest way to ensure this '
                       'is by namespacing them. That is, by putting those templates inside another directory named for '
                       'the application itself.'
		})

	return render_paginator(request, questions,[
        {'title': 'New Questions', 'url': 'feed', 'class': 'new'},
        {'title': 'Hot Questions', 'url': 'hot', 'class': 'hot'}
    ])



def hot(request):
	questions = []
	for i in range(1, 31):
		questions.append({
			'id': i,
			'title': 'Вопрос №' + str(i),
			'content': 'Examination of a sample of full texts of stories on disarmament with reference '
                       'to the United Nations filed in May and August 1998 shows that only 10 per cent of '
                       'stories covered substantive aspects of the work of the United Nations.'
		})

	return render_paginator(request, questions, [
        {'title': 'Hot Questions', 'url': 'hot', 'class': 'hot'},
        {'title': 'New Questions', 'url': 'feed', 'class': 'new'}
    ])



def tag(request):
	questions = []
	for i in range(1, 10):
		questions.append({
			'id': i,
			'title': 'Вопрос №' + str(i),
			'content': 'Examination of a sample of full texts of stories on disarmament with reference to the United Nations filed in May and August 1998 shows that only 10 per cent of stories covered substantive aspects of the work of the United Nations.'
		})

	tag_name = 'bender'

	return render_paginator(request, questions,[
        {'title': 'Tag: ' + tag_name,
         'url': 'tag', 'class': 'tag-header'}
    ])



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








def question(request, question_id):
	question = {
		'id': question_id,
		'title': 'Вопрос №' + str(question_id),
		'content': 'Examination of a sample of full texts of stories on disarmament with reference to the United Nations filed in May and August 1998 shows that only 10 per cent of stories covered substantive aspects of the work of the United Nations.'
	}

	return render(request, 'question.html', {'question': question})



def login(request):
	return HttpResponse(render_to_string('login.html'))

def registration(request):
	return HttpResponse(render_to_string('registration.html'))

def new_ask(request):
	return HttpResponse(render_to_string('new_question.html'))

def settings(request):
	return HttpResponse(render_to_string('settings.html'))


