from django.db import models


# Create your models here.


class Address(models.Model):
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    house_number = models.IntegerField()
    flat_number = models.IntegerField()


class Person(models.Model):
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    description = models.TextField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    photo = models.ImageField(null=True, blank=True)


class Phone(models.Model):
    number = models.IntegerField()
    type = models.CharField(max_length=32)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class Email(models.Model):
    e_mail = models.EmailField(max_length=64)
    type = models.CharField(max_length=32)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class Groups(models.Model):
    name = models.CharField(max_length=128)
    person = models.ManyToManyField(Person)

