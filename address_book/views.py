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


@form_decorator
def modify_person(request, id):
    person = Person.objects.get(id=id)
    res = ""


def delete_person(request, id):
    pass


@html_decorator
def show_all(request):
    persons = Person.objects.order_by('surname')
    res = "<ol>"
    # for person in persons:
    #     res += "<li><h3><a href='/show/{}'>{} {}</a></h3></li>".format(person.id, person.surname, person.name)
    #     res += """<a href='/modify/{}' style='color: red'>Edytuj osobę</a>
    #               <a href='/delete/{}' style='color: red'>Usuń osobę</a><br><br>""".format(person.id, person.id)
    for person in persons:
        res += "<li><h3><a href='/show/{}/'>{} {}</a></h3></li>".format(person.id, person.surname, person.name)
        res += """<button type='submit' name='modify' value={}'>Edytuj</button>
                  <button type='submit' name='delete' value={}'>Usuń</button><br><br>""".format(person.id, person.id)
    res += "</ol>"

    return res


@html_decorator
def show_person(request, id):
    person = Person.objects.get(id=id)
    res = ""
    res += "<h1>{} {}</h1>".format(person.name, person.surname)
    res += "("
    for group in person.groups_set.all():
        res += "<i>{}</i>".format(group.name)
    res += ")"
    res += "<p>{} {}</p><br>".format(person.photo, person.description)
    res += "<form><fieldset>"
    res += "<legend><b>Dane kontaktowe</b></legend>"
    res += "<p>Telefon:</p>"
    for number in person.phone_set.all():
        res += "<p><b>{}</b>: {}</p>".format(number.type, number.number)
    res += "<br>"
    res += "<p>Email:</p>"
    for mail in person.email_set.all():
        res += "<p><b>{}</b>: {}</p>".format(mail.type, mail.e_mail)
    res += "</fieldset></form>"

    res += "<form><fieldset>"
    res += "<legend><b>Dane adresowe</b></legend>"
    res += "<p>{}</p>".format(person.address.city)
    res += "<p>ul. {} {}/{}</p>".format(person.address.street, person.address.house_number, person.address.flat_number)
    res += "</fieldset></form>"
    res += "<a href='/modify/{}' style='color: red'>Edytuj osobę</a>"

    return res
