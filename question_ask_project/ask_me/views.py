from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from ask_me.models import *
from ask_me.forms import UserRegistrationForm, UserLoginForm, NewQuestionForm, UserSettingsForm, AnswerForm


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
	if Question.objects.filter(id=question_id).exists():
		question = Question.objects.get_by_id(int(question_id)).first()
		answers = paginator(request, Answer.objects.get_answers_hot(question.id))
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
	if request.POST:
		form = UserLoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
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


@login_required(login_url='/signin/')
def new_question(request):
	if request.method == 'POST':
		form = NewQuestionForm(request.POST)
		if form.is_valid():
			ques = Question.objects.create(author=request.user,
											   date=timezone.now(),
											   is_active=True,
											   title=form.cleaned_data['title'],
											   text=form.cleaned_data['text'])
			ques.save()

			for tagTitle in form.cleaned_data['tags'].split():
				tag = Tag.objects.get_or_create(name=tagTitle)[0]
				ques.tags.add(tag)
				ques.save()
			return question(request, ques.id)
	else:
		form = NewQuestionForm()
	return render(request, 'new_question.html', {'form': form})


@login_required(login_url='/signin/')
def new_answer(request, question_id):
	if Question.objects.filter(id=question_id).exists():
		if request.method == 'POST':
			form = AnswerForm(request.POST)
			if form.is_valid():
				answeredQuestion = Question.objects.get_by_id(question_id)[0]
				answer = Answer.objects.create(author=request.user,
												  date=timezone.now(),
												  text=form.cleaned_data['text'],
												  question_id=answeredQuestion.id)
				answer.save()
				return redirect(f'/question/{ question_id }/#{ answer.id }')
		else:
			form = AnswerForm()
		return render(request, 'answer.html', {'form': form})
	else:
		raise Http404

#TODO добавить изменение пароля
#TODO Likes

@login_required(login_url='/signin/')
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


@login_required(login_url='/signin/')
def delete_question(request):
	if request.method == 'POST':
		question_id = int(request.POST.get('question_id'))
		question = Question.objects.get(id=question_id)
		question.delete()
		return redirect('/')
	else:
		raise Http404\


@login_required(login_url='/signin/')
def delete_answer(request):
	if request.method == 'POST':
		answer_id = int(request.POST.get('answer_id'))
		answer = Answer.objects.get(id=answer_id)
		answer.delete()
		return redirect('/')
	else:
		raise Http404


def search(request):
	if request.method == 'GET' and 'tag' in request.GET:
		tag_search = request.GET.get('tag')
		try:
			return tag(request, tag_search)
		except AttributeError:
			return redirect('/')
	else:
		raise Http404


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