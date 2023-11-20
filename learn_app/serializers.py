from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import QuestionCard, UserProfile, Category, Question, Answer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name', 'experience', 'credits', 'prestige', 'user_id' ]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class CategoryCardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class QuestionCardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QuestionCard
        fields = ['id', 'category_id', 'title', 'reward_credits', 'reward_exp']

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'content', 'choice_one', 'choice_two', 'choice_three', 'choice_four', 'correct_answer']

class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'user_answer', 'question_id', 'user_id']