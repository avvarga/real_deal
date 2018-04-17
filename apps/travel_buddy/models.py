from __future__ import unicode_literals

from django.db import models
from datetime import date
import bcrypt, datetime
# Create your models here.
class UserManager (models.Manager):
    def valid_registration (self,postData):
        errors = []
        name = postData['name']
        username = postData['username']
        password = postData['password']
        pwd_confirm = postData['pwd_confirm']

        if len(name) ==0  :
            errors.append ("Your name is required")
        elif len(name) < 3:
            errors.append ("Your name should be at least 3 characters long")
        if len(username) == 0:
            errors.append ("Your username is required")
        elif len(username) < 3:
            errors.append ("Your username should be at least 3 characters long")
        if len(password) == 0:
            errors.append ("Your password is required")
        elif len(password) < 8:
            errors.append ("Your Password must be at least 8 characters long")
        if User.objects.filter(username = username):
            errors.append ('This username is already in use. Please log in instead.')
        if password != pwd_confirm:
            errors.append ('The password and password confirmation must match')
        return errors

    def valid_login (self,postData):
        errors =[]
        username = postData['username']
        password = postData['password']
        if len(username) == 0:
            errors.append ("Invalid username/password combination")
        elif len(username) < 3:
            errors.append ("Invalid username/password combination")
        elif len(password) == 0:
            errors.append ("Invalid username/password combination")
        try:
            user = User.objects.get(username = username)
            if bcrypt.checkpw ( password.encode(), user.password.encode() ):
                return errors
            errors.append ("Invalid username/password combination")
        except User.DoesNotExist:
            errors.append ("Invalid username/password combination")
        return errors

class TripManager (models.Manager):
    def valid_trip (self,postData):
        errors = []
        destination = postData['destination']
        description = postData['description']
        travel_from = postData['travel_from']
        travel_to = postData['travel_to']
        today = date.today().isoformat()
        if len(destination) == 0:
            errors.append ("Please enter a destination")
        if len(description) == 0:
            errors.append ("Please enter a valid description")
        if len(travel_from) == 0:
            errors.append ("Please enter a valid start date")
        if len(travel_to) == 0:
            errors.append ("Please enter a valid end date")
        elif travel_from <= today:
            errors.append ("The trip must be scheduled in the future")
        elif travel_to < travel_from:
            errors.append ("The Travel End Date cannot be before {}".format(travel_from))
        return errors

class User (models.Model):
    name = models.CharField (max_length = 255)
    username = models.CharField (max_length = 255)
    password = models.CharField (max_length = 255)
    objects = UserManager()    

    created_at = models.DateTimeField (auto_now_add = True)
    updated_at = models.DateTimeField (auto_now = True)

    def __str__(self):
        return self.name


class Trip (models.Model):
    destination = models.CharField (max_length = 255)
    description = models.TextField ()
    travel_from = models.DateField (null=True, blank=True)
    travel_to = models.DateField (null=True, blank=True)
    user = models.ForeignKey (User, related_name = 'trips')
    other = models.ManyToManyField (User, related_name = 'other_trips')     
    objects = TripManager()

    created_at = models.DateTimeField (auto_now_add = True)
    updated_at = models.DateTimeField (auto_now = True)

    def __str__(self):
        return self.name


