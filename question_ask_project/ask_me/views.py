from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.contrib.auth import authenticate, login, logout

from ask_me.models import *
from ask_me.forms import UserRegistrationForm, UserLoginForm, NewQuestionForm, UserSettingsForm


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


def signup(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST, request.FILES)
		if form.is_valid():
			user = form.save()
			user.set_password(form.cleaned_data['password'])
			user.save()
			login(request, user)
			return redirect('/')
	else:
		form = UserRegistrationForm()
		logout(request)
	return render(request, 'signup.html', {'form': form})


def signin(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect(request.GET.get('next') if request.GET.get('next') != '' else '/')
	else:
		form = UserLoginForm()
		logout(request)
	return render(request, 'signin.html', {'form': form})


def signout(request):
	if not request.user.is_authenticated:
		raise Http404
	logout(request)
	return redirect(request.GET['from'])


def new_question(request):
	if not request.user.is_authenticated:
		form = UserLoginForm()
		return render(request, 'signin.html', {'form': form})

	if request.method == 'POST':
		form = NewQuestionForm(request.POST)
		if form.is_valid():
			question = form.save()
			question.author = request.POST['author_id']
			question.save()

			for tagTitle in request.POST['tags'].split():
				tag = Tag.objects.get_or_create(name=tagTitle)[0]
				question.tags.add(tag)
				question.save()
			return question(request, question.id)
	else:
		form = NewQuestionForm()
	return render(request, 'new_question.html', {'form': form})


def settings(request):
	if request.method == 'POST':
		form = UserSettingsForm(request.POST, request.FILES)
		if form.is_valid():
			for changedField in form.changed_data:
				setattr(request.user, changedField, request.POST[changedField])
			request.user.save()
			return redirect('/')
	else:
		form = UserSettingsForm()

		for i in form.base_fields:
			form.base_fields[i].widget.attrs['placeholder'] = getattr(request.user, i)
	return render(request, 'settings.html', {'form': form})


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