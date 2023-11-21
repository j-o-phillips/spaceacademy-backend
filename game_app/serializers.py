from rest_framework import serializers
from .models import Ship, Engines, Weapons, Shields, Thrusters, Hangar, Comment, Post

class ShipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ship
        fields = ['id', 'name', 'user_profile_id', 'weapons_id', 'engines_id', 'thrusters_id', 'shields_id']

class WeaponsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Weapons
        fields = ['id', 'name', 'damage', 'level']

class EnginesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Engines
        fields = ['id', 'name', 'speed', 'level']

class ThrustersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Thrusters
        fields = ['id', 'name', 'thrust', 'level']

class ShieldsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shields
        fields = ['id', 'name', 'power', 'level']

class HangarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hangar
        fields = ['id', 'name']

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'content', 'profile_id', 'hangar_id']

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'post_id']