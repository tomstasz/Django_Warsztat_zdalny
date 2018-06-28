# Generated by Django 2.0.3 on 2018-06-28 09:35

from django.db import migrations
from address_book.models import Address, Person, Phone, Email, Groups


def populate(apps, schema_editor):

    add_1 = Address.objects.create(city='Zalesie', street='Różana', house_number=10, flat_number=6)
    add_2 = Address.objects.create(city='Opole', street='Niezapominajek', house_number=8, flat_number=12)
    add_3 = Address.objects.create(city='Warszawa', street='Dembego', house_number=3, flat_number=57)

    roman = Person.objects.create(name='Roman',
                                  surname='Kowalski',
                                  description="dobry mechanik, złota rączka",
                                  address=add_1)

    halinka = Person.objects.create(name='Halinka',
                                    surname='Kowalska',
                                    description='siostra Romana',
                                    address=add_1)
    janusz = Person.objects.create(name='Jausz',
                                   surname='Gadomski',
                                   description='wujek z Opola',
                                   address=add_2)

    aska = Person.objects.create(name='Aśka',
                                 surname='Burzyńska',
                                 description='ta ruda',
                                 address=add_3)

    phone_1 = Phone.objects.create(number=6047432, type='domowy', person=roman)
    phone_2 = Phone.objects.create(number=937491, type='domowy', person=halinka)
    phone_3 = Phone.objects.create(number=7205833, type='domowy', person=janusz)
    phone_4 = Phone.objects.create(number=4496290, type='domowy', person=aska)

    email_1 = Email.objects.create(e_mail='roman_K@onet.pl', type='domowy', person=roman)
    email_2 = Email.objects.create(e_mail='halinka_K@onet.pl', type='domowy', person=halinka)
    email_3 = Email.objects.create(e_mail='bigjanus@gazeta.pl', type='domowy', person=janusz)
    email_4 = Email.objects.create(e_mail='asia_burzynska@interia.pl', type='domowy', person=aska)

    group_1 = Groups.objects.create(name='rodzina')
    group_1.person.add(roman)
    group_1.person.add(halinka)
    group_1.person.add(janusz)
    group_2 = Groups.objects.create(name='znajomi')
    group_2.person.add(aska)


class Migration(migrations.Migration):

    dependencies = [
        ('address_book', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate),
    ]
