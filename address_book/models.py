from django.db import models


# Create your models here.


class Address(models.Model):
    city = models.CharField(max_length=64, default='brak')
    street = models.CharField(max_length=64, default='brak')
    house_number = models.IntegerField(default=None)
    flat_number = models.IntegerField(default=None)


class Person(models.Model):
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    description = models.TextField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    photo = models.ImageField(null=True, blank=True)


class Phone(models.Model):
    number = models.IntegerField(default=None)
    type = models.CharField(max_length=32, default='brak')
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class Email(models.Model):
    e_mail = models.EmailField(max_length=64, default=None)
    type = models.CharField(max_length=32, default='brak')
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class Groups(models.Model):
    name = models.CharField(max_length=128, default='brak')
    person = models.ManyToManyField(Person)

