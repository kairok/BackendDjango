from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Firma(models.Model):
    name = models.CharField(max_length=100)
    user = models.ManyToManyField(User)

    def __str__(self):
        return 'Firma'.format(self.name)


class Request(models.Model):
    tema = models.CharField(max_length=100)
    problem  = models.ForeignKey('Problem', on_delete=models.DO_NOTHING)
    datetask = models.DateTimeField(auto_now_add=True)
    master = models.ForeignKey('Master', on_delete=models.CASCADE)
    prioritet = models.ForeignKey('Prioritet', on_delete=models.DO_NOTHING)
    description = models.TextField()
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    status = models.ForeignKey('Status', on_delete=models.DO_NOTHING)
    daterun = models.DateField(blank=True, null=True)
    firma = models.ForeignKey('Firma', on_delete=models.CASCADE)

    def __str__(self):
        return 'Request'.format(self.tema)


class Client(models.Model):
    company = models.CharField(max_length=200)
    contactfio = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    flat = models.CharField(max_length=50, blank=True)
    cabinet = models.CharField(max_length=10, blank=True)
    date_in = models.DateField(blank=True, null=True)
    description = models.TextField(default='')
    active = models.BooleanField(default=True)
    firma = models.ForeignKey('Firma', on_delete=models.CASCADE)

    def __str__(self):
        return 'Client'.format(self.company)



class Problem(models.Model):
    type = models.CharField(max_length=100)
    firma = models.ForeignKey('Firma', on_delete=models.CASCADE)

    def __str__(self):
        return 'Problem'.format(self.type)


class Master(models.Model):
    fio = models.CharField(max_length=100)
    profesion = models.CharField(max_length=50)
    spec = models.ForeignKey('Spec', on_delete=models.DO_NOTHING)
    phone = models.CharField(max_length=20, blank=True)
    vacation = models.BooleanField(default=False)
    time_start = models.CharField(max_length=10, blank=True)
    time_end =models.CharField(max_length=10, blank=True)
    description = models.TextField(default='')
    adress = models.CharField(max_length=200, default='')
    active = models.BooleanField(default=True)
    firma = models.ForeignKey('Firma', on_delete=models.CASCADE)

    def __str__(self):
        return 'Master'.format(self.fio)


class Prioritet(models.Model):
    type = models.CharField(max_length=20)


    def __str__(self):
        return 'Prioritet'.format(self.type)


class Spec(models.Model):
    type = models.CharField(max_length=20)
    firma = models.ForeignKey('Firma', on_delete=models.CASCADE)

    def __str__(self):
        return 'Spec'.format(self.type)

class Status(models.Model):
    type = models.CharField(max_length=20)


    def __str__(self):
        return 'Spec'.format(self.type)
