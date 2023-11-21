from django.db import models
from django.contrib.auth.models import User
from learn_app.models import UserProfile

class Weapons(models.Model):
     name = models.CharField( max_length=100)
     damage = models.IntegerField()
     level = models.IntegerField()


class Engines(models.Model):
     name = models.CharField( max_length=100)
     speed = models.IntegerField()
     level = models.IntegerField()

class Thrusters(models.Model):
     name = models.CharField( max_length=100)
     thrust = models.IntegerField()
     level = models.IntegerField()


class Shields(models.Model):
     name = models.CharField( max_length=100)
     power = models.IntegerField()
     level = models.IntegerField()
     

class Ship(models.Model):
     user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

     name = models.CharField( max_length=100)
     weapons = models.ForeignKey(Weapons, on_delete=models.CASCADE)
     engines = models.ForeignKey(Engines, on_delete=models.CASCADE)
     thrusters = models.ForeignKey(Thrusters, on_delete=models.CASCADE)
     shields = models.ForeignKey(Shields, on_delete=models.CASCADE)
     

