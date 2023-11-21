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


class Hangar(models.Model):
     profile = models.ManyToManyField(UserProfile)
     name = models.CharField( max_length=100)
     
     def __str__(self):
        return self.name
     
class Post(models.Model):
     profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
     hangar = models.ForeignKey(Hangar, on_delete=models.CASCADE)

     title = models.CharField(max_length=100)
     author =  models.CharField(max_length=100)
     content =  models.CharField(max_length=300)

     def __str__(self):
        return self.title

class Comment(models.Model):
     post = models.ForeignKey(Post, on_delete=models.CASCADE)

     author =  models.CharField(max_length=100)
     content =  models.CharField(max_length=300)
     
