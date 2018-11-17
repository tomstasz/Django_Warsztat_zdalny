from django.shortcuts import redirect
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from address_book.models import Person, Address, Phone, Email, Groups


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


@csrf_exempt
@html_decorator
def modify_person(request, id):
    person = Person.objects.get(id=id)
    if request.method == "GET":
        personal_form = "<form enctype='multipart/form-data' action='#' method='post'>{}</form>"
        personal_data = """<label>Imię:<br>
                         <input type='text' name='person_name' value={}>
                         </label><br><br>
                         <label>Nazwisko:<br>
                         <input type='text' name='person_surname' value={}>
                         </label><br><br>
                         <label>Opis:<br>
                         <textarea cols='50' rows='10' name='person_description'>{}</textarea>
                         </label><br><br>
                         <label>Zdjęcie:<br>
                         <input type='image' name='person_photo' value='załącz plik'>
                         </label><br><br>
                         <button name='personal'>Zmień dane</button>""".format(person.name,
                                                                               person.surname,
                                                                               person.description)

        address_form = """<form action='#' method='post'>
                         <fieldset>
                         <legend><b>Dane adresowe</b></legend>        
                         <label>Miasto:<br>
                         <input type='text' name='person_city'>
                         </label><br><br>
                         <label>Ulica:<br>
                         <input type='text' name='person_street'>
                         </label><br><br>
                         <label>Numer domu:<br>
                         <input type='number' name='person_house'>
                         </label><br><br>
                         <label>Numer mieszkania:<br>
                         <input type='number' name='person_flat'>
                         </label><br><br>
                         <input type='submit' name='address_button' value='Dodaj adres'>
                         </fieldset>
                         </form>""".format(person.id)
        phone_form = """<form action='#' method='post'>
                         <fieldset>
                         <legend><b>Telefony</b></legend>        
                         <label>Telefon:<br>
                         <input type='number' name='person_phone'>
                         </label><br><br>
                         <label>Rodzaj:<br>
                         <select name='phone_type'>
                         <option value='domowy'>domowy</option>
                         <option value='służbowy'>służbowy</option>
                         </select>
                         </label><br><br>
                         <input type='submit' name='phone_button' value='Dodaj telefon'>
                         </fieldset>
                         </form>""".format(person.id)
        email_form = """<form action='#' method='post'>
                         <fieldset>
                         <legend><b>Poczta</b></legend>        
                         <label>E-mail:<br>
                         <input type='email' name='person_email'>
                         </label><br><br>
                         <label>Rodzaj:<br>
                         <select name='email_type'>
                         <option value='domowy'>domowy</option>
                         <option value='służbowy'>służbowy</option>
                         </select>
                         </label><br><br>
                         <input type='submit' name='email_button' value='Dodaj e-mail'>
                         </fieldset>
                         </form>""".format(person.id)
        delete_phone = """<form action='#' method='post'>"""
        delete_phone += """<label>Usuń telefon:
                           <select name='delete_phone'>"""

        for number in person.phone_set.all():
            delete_phone += "<option value={}>{}</option>".format(number.id, number.number)

        delete_phone += "</select></label> <input type='submit' name='del_phone' value='skasuj'>"
        delete_phone += "</form>"

        delete_mail = """<form action='#' method='post'>"""
        delete_mail += """<label>Usuń e-mail:
                          <select name='delete_email'>"""

        for mail in person.email_set.all():
            delete_mail += "<option value={}>{}</option>".format(mail.id, mail.e_mail)

        delete_mail += "</select></label> <input type='submit' name='del_mail' value='skasuj'>"
        delete_mail += "</form>"

        return personal_form.format(personal_data) \
            + address_form \
            + phone_form + email_form \
            + delete_phone \
            + delete_mail \
            + "<br><a href='/show/{}/'>Wróć</a>".format(person.id)
    else:
        if request.POST.get('personal') is not None:
            name = request.POST.get('person_name')
            surname = request.POST.get('person_surname')
            description = request.POST.get('person_description')
            photo = request.POST.get('person_photo')
            person.name = name
            person.surname = surname
            person.description = description
            person.photo = photo
            person.save()
            res = "Zapisano dane {} {}".format(person.name, person.surname)
            res += "<br><br><a href='/show/{}/' style='color: red;'>Pokaż osobę</a>".format(person.id)
            return res
        elif request.POST.get('address_button') is not None:
            city = request.POST.get('person_city')
            street = request.POST.get('person_street')
            house = request.POST.get('person_house')
            flat = request.POST.get('person_flat')
            if city and street and house and flat:
                address = Address.objects.create(city=city, street=street, house_number=house, flat_number=flat)
                person.address = address
                person.save()
                res = """Zmiana adresu {} {} na: \n {} ul. {} {}/{}""".format(person.name,
                                                                              person.surname,
                                                                              address.city,
                                                                              address.street,
                                                                              address.house_number,
                                                                              address.flat_number)
                res += "<br><br><a href='/show/{}/' style='color: red;'>Pokaż osobę</a>".format(person.id)
            else:
                res = "Proszę podać pełne dane adresowe."
                res += "<br><br><a href='/modify/{}/'>wróć</a>".format(person.id)
            return res
        elif request.POST.get('phone_button') is not None:
            phone = request.POST.get('person_phone')
            type = request.POST.get('phone_type')
            if phone:
                new_phone = Phone.objects.create(number=phone, type=type, person=person)
                res = "Dodano {} telefon {} dla {} {}".format(new_phone.type,
                                                              new_phone.number,
                                                              person.name,
                                                              person.surname)
                res += "<br><br><a href='/show/{}/' style='color: red;'>Pokaż osobę</a>".format(person.id)
            else:
                res = "Proszę podać numer telefonu."
                res += "<br><br><a href='/modify/{}/'>wróć</a>".format(person.id)

            return res
        elif request.POST.get('email_button') is not None:
            mail = request.POST.get('person_email')
            type = request.POST.get('email_type')
            if mail:
                new_mail = Email.objects.create(e_mail=mail, type=type, person=person)
                res = "Dodano {} e-mail {} dla {} {}".format(new_mail.type,
                                                             new_mail.e_mail,
                                                             person.name,
                                                             person.surname)
                res += "<br><br><a href='/show/{}/' style='color: red;'>Pokaż osobę</a>".format(person.id)
            else:
                res = "Proszę podać adres email."
                res += "<br><br><a href='/modify/{}/'>wróć</a>".format(person.id)

            return res
        elif request.POST.get('del_phone') is not None:
            del_phone = request.POST.get('delete_phone')
            phone = Phone.objects.get(id=del_phone)
            phone.delete()

            res = "Usunięto numer {} dla {} {}".format(phone.number, person.name, person.surname)

            res += "<br><br><a href='/show/{}/' style='color: red;'>Pokaż osobę</a>".format(person.id)

            return res
        elif request.POST.get('del_mail') is not None:
            del_mail = request.POST.get('delete_email')
            mail = Email.objects.get(id=del_mail)
            mail.delete()

            res = "Usunięto adres {} dla {} {}".format(mail.e_mail, person.name, person.surname)

            res += "<br><br><a href='/show/{}/' style='color: red;'>Pokaż osobę</a>".format(person.id)

            return res


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
    res += """<a href='/new/' style='color: red;'>Dodaj osobę</a> 
              <a href='/groups/' style='color: red;'>Pokaż grupy</a>"""
    response.write(html.format(res))
    if request.method == "POST":
        delete_id = request.POST.get('delete')
        modify_id = request.POST.get('modify')
        if delete_id is not None:
            return redirect('/delete/{}/'.format(delete_id))
        elif modify_id is not None:
            return redirect('/modify/{}/'.format(modify_id))

    return response


@html_decorator
def show_person(request, id):
    person = Person.objects.get(id=id)
    res = ""
    res += "<h1>{} {}</h1>".format(person.name, person.surname)
    if person.groups_set.all():
        res += "<b>Należy do grup:</b>"
        res += "<ul>"
        for group in person.groups_set.all():
            res += "<li><i>{}</i></li>".format(group.name)
        res += "</ul>"
    else:
        res += "<i>nie należy do grup</i>"
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
    res += """<a href='/modify/{}/' style='color: red;'>Edytuj osobę</a>
              <a href='/' style='color: red;'>Pokaż wszystkie kontakty</a>
              <a href='/add_to_group/{}/' style='color: red;'>Dodaj do grupy</a>""".format(person.id, person.id)

    return res


@html_decorator
def show_groups(request):
    groups = Groups.objects.all()
    search_link = " <a href='/search-groups/' style='color: red;'>Szukaj członków grup</a>"
    res = "<ul>"
    for group in groups:
        res += "<li><a href='/show_members/{}/'><h3>{}</h3></a></li><br>".format(group.id, group.name)
    res += "</ul>"
    res += "<a href='/create_group/' style='color: red;'>Stwórz nową grupę</a>" + search_link

    return res


@html_decorator
def show_group_members(request, id):
    group = Groups.objects.get(id=id)
    res = ""
    if request.method == "GET":
        res += """<h3>Grupa '{}'</h3>""".format(group.name)
        res += """<small><a href='/delete_group/{}/'>Usuń grupę</a></small>""".format(group.id)
        res += "<ul>"
        for member in group.person.all():
            res += "<li><a href='/show/{}/'>{} {}</a></li><br>""".format(member.id, member.surname, member.name)
        res += "</ul>"

    return res


@csrf_exempt
@form_decorator
def add_to_group(request, id):
    person = Person.objects.get(id=id)
    groups = Groups.objects.all()
    res = ""
    if request.method == 'GET':
        for group in groups:
            res += """<label>{}
                     <input type='checkbox' name='member' value={}>
                     </label><br><br>""".format(group.name, group.id)

        res += "<input type='submit' value='dodaj'>"
        return res
    else:
        for group in groups:
            for selected in request.POST.getlist('member'):
                if group.id == int(selected):
                    group.person.add(person)
                    res += "{} {} dodany do grupy '{}'<br>".format(person.name, person.surname, group.name)
        res += "<br><a href='/show/{}/'>Wróć</a>".format(person.id)

    return res


def delete_cookie(request, name):
    response = HttpResponse()
    if name in request.COOKIES:
        response.delete_cookie(name)
        response.write("Ciasteczko '{}' skasowane<br>".format(name))
    else:
        response.write("brak ciasteczka")
    return response


@csrf_exempt
@form_decorator
def create_group(request):
    res = ""
    if request.method == 'GET':
        res += """<label>Nazwa grupy:
                 <input type='text' name='group_name'>
                 </label>
                 <input type='submit' value='załóż grupę'>"""

    else:
        name = request.POST.get('group_name')
        Groups.objects.create(name=name)
        res += "Założono grupę '{}'<br><br>".format(name)
        res += "<a href='/groups/' style='color: red;'>Pokaż grupy</a>"

    return res


@html_decorator
def delete_group(request, id):
    res = ""
    if request.method == "GET":
        group = Groups.objects.get(id=id)
        group.delete()
        res += "Grupa '{}' skasowana<br><br>".format(group.name)
    res += "<a href='/groups/' style='color: red;'>Pokaż grupy</a>"
    return res


@csrf_exempt
@form_decorator
def search_groups(request):
    res = ""
    if request.method == 'GET':
        res += """<label>Imię:
                  <input type='text' name='s_name'>
                  </label>"""
        res += """<label>Nazwisko:
                  <input type='text' name='s_surname'>
                  </label>"""
        res += "<input type='submit' value='szukaj'>"
        res += "<br>"
        res += "<a href='/'>wróć</a>"
    else:
        name = request.POST.get('s_name')
        surname = request.POST.get('s_surname')

        if name is not None and surname is None:
            try:
                persons = Person.objects.filter(name__contains=name.title())
            except Http404:
                return "nie ma takiej osoby"
        elif name is None and surname is not None:
            try:
                persons = Person.objects.filter(surname__contains=surname.title())
            except Http404:
                return "nie ma takiej osoby"
        elif (name and surname) is not None:
            try:
                persons = Person.objects.filter(name__contains=name.title(), surname__contains=surname.title())
            except Http404:
                return "nie ma takiej osoby"
        else:
            raise Http404

        for person in persons:
            if person.groups_set.all():
                res += "{} {} należy do:".format(person.name, person.surname)
                res += "<ul>"
                for group in person.groups_set.all():
                    res += "<li>{}</li>".format(group.name)
                res += '</ul><br><br>'
            else:
                res += "Osoba nie należy do zadnej grupy"

    return res


