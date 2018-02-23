from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
# Create your views here.

def main(request):
	return redirect('questions')

def questions(request):
	return HttpResponse(render_to_string('questions.html'))

def login(request):
	return HttpResponse(render_to_string('login.html'))

def registration(request):
	return HttpResponse(render_to_string('registration.html'))

def new_ask(request):
	return HttpResponse(render_to_string('new_question.html'))

def settings(request):
	return HttpResponse(render_to_string('settings.html'))

def tag(request):
	return HttpResponse(render_to_string('tag.html'))

def question(request):
	return HttpResponse(render_to_string('question.html'))
