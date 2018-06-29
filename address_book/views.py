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


@csrf_exempt
def create_person(request):
    response = HttpResponse()
    html = "<html><body>{}</body></html>"
    if request.method == 'GET':
        res = """<form action="#" method="POST">
                 <label>Imię:<br>
                 <input type='text' name='person_name'>
                 </label><br><br>
                 <label>Nazwisko:<br>
                 <input type='text' name='person_surname'>
                 </label><br><br>
                 <label>Opis:<br>
                 <input type='text' name='person_description'>
                 </label><br><br>
                 <label>Zdjęcie:<br>
                 <input type='image' name='person_photo' value='załącz plik'>
                 </label><br><br>
                 <input type='submit' name='create_button' value='Dodaj'>
                 </form>
                 """
        response.write(html.format(res))
    else:
        name = request.POST.get('person_name')
        surname = request.POST.get('person_surname')
        description = request.POST.get('person_description')
        photo = request.POST.get('person_photo')
        Person.objects.create(name=name, surname=surname, description=description, photo=photo)
        last = Person.objects.latest('id')
        return redirect('/show/{}/'.format(last.id))

    return response


@form_decorator
def modify_person(request, id):
    person = Person.objects.get(id=id)
    res = ""


@csrf_exempt
@html_decorator
def delete_person(request, id):
    person = Person.objects.get(id=id)
    if person:
        person.delete()
        return "Skasowano {} {}".format(person.name, person.surname)
    else:
        return "Nie ma takiej osoby"


@csrf_exempt
def show_all(request):
    persons = Person.objects.order_by('surname')
    response = HttpResponse()
    html = "<html><body>{}</body></html>"
    res = "<ol>"

    for person in persons:
        res += """<li><h3><a href='/show/{}/'>{} {}</a></h3></li>""".format(person.id, person.surname, person.name)
        res += """<form action='#' method='post'>
                  <button name='modify' value='{}'>Edytuj</button>
                  <button name='delete' value='{}'>Skasuj</button><br><br>
                  </form>""".format(person.id, person.id)
    res += "</ol>"
    res += "<a href='/new/' style='color: red;'>Dodaj osobę</a>"
    response.write(html.format(res))
    if request.method == "POST":
        delete_id = request.POST.get('delete')
        modify_id = request.POST.get('modify')
        if delete_id is not None:
            return redirect('/delete/{}/'.format(delete_id))
        elif modify_id is not None:
            pass

    return response


@html_decorator
def show_person(request, id):
    person = Person.objects.get(id=id)
    res = ""
    res += "<h1>{} {}</h1>".format(person.name, person.surname)
    res += "("
    if person.groups_set.all():
        for group in person.groups_set.all():
            res += "<i>{}</i>".format(group.name)
    else:
        res += "<i>nie należy do grup</i>"
    res += ")"
    res += "<p>{} {}</p><br>".format(person.photo, person.description)
    res += "<form><fieldset>"
    res += "<legend><b>Dane kontaktowe</b></legend>"
    res += "<p>Telefon:</p>"
    if person.phone_set.all():
        for number in person.phone_set.all():
            res += "<p><b>{}</b>: {}</p>".format(number.type, number.number)
    else:
        res += "<p>brak</p>"
    res += "<br>"
    res += "<p>Email:</p>"
    if person.phone_set.all():
        for mail in person.email_set.all():
            res += "<p><b>{}</b>: {}</p>".format(mail.type, mail.e_mail)
    else:
        res += "<p>brak</p>"
    res += "</fieldset></form>"

    res += "<form><fieldset>"
    res += "<legend><b>Dane adresowe</b></legend>"
    if person.address is not None:
        res += "<p>{}</p>".format(person.address.city)
        res += "<p>ul. {} {}/{}</p>".format(person.address.street,
                                            person.address.house_number,
                                            person.address.flat_number)
    else:
        res += "<p>brak</p>"
    res += "</fieldset></form>"
    res += "<a href='/modify/{}' style='color: red;'>Edytuj osobę</a>"

    return res
