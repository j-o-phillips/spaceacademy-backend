from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import QuestionCard, UserProfile, Category, Question


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


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
        fields = ['id', 'content', 'choice_one', 'choice_two', 'choice_three', 'choice_four', 'answer']