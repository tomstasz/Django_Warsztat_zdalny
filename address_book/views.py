from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator
from datetime import datetime, timedelta
from address_book.models import Person, Address, Phone, Email, Groups
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your views here.


def html_decorator(func):
    def inner_function(*args, **kwargs):
        html = """<html><body>{}</body></html>""".format(func(*args, **kwargs))
        return HttpResponse(html)
    return inner_function


def form_decorator(func):
    def inner_function(*args, **kwargs):
        html = """<html><body>
                  <form enctype='multipart/form-data' action='#' method='post'>{}</form>
                  </body></html>""".format(func(*args, **kwargs))
        return HttpResponse(html)
    return inner_function


def create_person(request):
    pass


def modify_person(request):
    pass


def delete_person(request):
    pass


def show_person(request):
    pass


def show_all(request):
    pass
