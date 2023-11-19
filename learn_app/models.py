from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField( max_length=255, default='')
    last_name = models.CharField( max_length=255, default='')
    experience = models.IntegerField()
    credits = models.IntegerField()
    prestige = models.IntegerField()

    def __str__(self):
        return self.first_name
    
class Planet(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class QuestionCard(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    title = models.CharField( max_length=200)
    reward_credits = models.IntegerField()
    reward_exp = models.IntegerField()

    def __str__(self):
        return self.title

class Question(models.Model):
    question_card = models.ForeignKey(QuestionCard, on_delete=models.CASCADE)

    content = models.CharField(max_length=300)
    choice_one = models.CharField(max_length=300)
    choice_two = models.CharField(max_length=300)
    choice_three = models.CharField(max_length=300)
    choice_four = models.CharField(max_length=300)
    answer = models.CharField(max_length=300)

    



