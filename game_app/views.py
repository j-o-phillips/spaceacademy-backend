from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from learn_app.models import UserProfile
from .models import Ship, Weapons, Shields, Engines, Thrusters, Hangar, Post, Comment
from .serializers import ShipSerializer, WeaponsSerializer, ThrustersSerializer, EnginesSerializer, HangarSerializer, ShieldsSerializer, PostSerializer, CommentSerializer
from rest_framework import viewsets, permissions, generics
from learn_app.serializers import UserProfileSerializer

class ShipView(APIView):
    def get(self, request, format=None):
        user = self.request.user
        user = User.objects.get(id=user.id)
        user_profile = UserProfile.objects.get(user=user)
        
        ship = Ship.objects.get(user_profile=user_profile)

        weapons = Weapons.objects.get(id=ship.weapons_id)
        weapons = WeaponsSerializer(weapons)

        shields = Shields.objects.get(id=ship.shields_id)
        shields = ShieldsSerializer(shields)

        engines = Engines.objects.get(id=ship.engines_id)
        engines = EnginesSerializer(engines)

        thrusters = Thrusters.objects.get(id=ship.thrusters_id)
        thrusters = ThrustersSerializer(thrusters)
        
        ship = ShipSerializer(ship, context={'request': request})

        return JsonResponse({'ship': ship.data, 'weapons': weapons.data, 'shields': shields.data, 'engines': engines.data, 'thrusters': thrusters.data}  )


class HangarView(APIView):
    def get(self, request, format=None):
        hangars = Hangar.objects.all()
        hangars = HangarSerializer(hangars, many=True)

        return JsonResponse({'data': hangars.data})
    
    #create hangar
    def post(self, request, format=None):
        user = self.request.user
        user = User.objects.get(id=user.id)
        user_profile = UserProfile.objects.get(user=user)
        data = self.request.data
        hangar_name = data['hangar_name']

        hangar = Hangar.objects.create(name=hangar_name)
        hangar.save()

        hangar.profile.add(user_profile)

        return JsonResponse({'message': 'hangar created'})

class HangarDetailView(APIView):
    def get(self, request, hangar_id, format=None):
        hangar = Hangar.objects.get(id=hangar_id)
        members = hangar.profile.all()
        print(members)

        members = UserProfileSerializer(members, many=True)

        return JsonResponse({'data': members.data})
    #join hangar
    def post(self, request, hangar_id, format=None):
        hangar = Hangar.objects.get(id=hangar_id)
        user = self.request.user
        user = User.objects.get(id=user.id)
        user_profile = UserProfile.objects.get(user=user)

        #check if already a member
        try:
            #already a member
            member = hangar.profile.get(id=user_profile.id)
            return JsonResponse({ 'message': 'already a user'})
        except:
            #not a member
            hangar.profile.add(user_profile)
            return JsonResponse({ 'message': 'user joined'})
        
    #leave hangar
    def put(self, request, hangar_id, format=None):
        hangar = Hangar.objects.get(id=hangar_id)
        user = self.request.user
        user = User.objects.get(id=user.id)
        user_profile = UserProfile.objects.get(user=user)
        
        #check if a member
        try:
            # a member
            member = hangar.profile.get(id=user_profile.id)
            hangar.profile.remove(member)
            return JsonResponse({ 'message': 'user left'})
        except:
            #not a member
            return JsonResponse({ 'message': 'not a member'})
                                
class PostView(APIView):
    def get(self, request, hangar_id, format=None):
        try:
            posts = Post.objects.filter(hangar_id=hangar_id)
            posts = PostSerializer(posts, many=True)

            return JsonResponse({ 'data': posts.data})
        
        except:
            return JsonResponse({ 'data': 'django error'})
        
    def post(self, request, hangar_id, format=None):
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)
        data = self.request.data
        title = data['title']
        content = data['content']

        user = self.request.user
        user = User.objects.get(id=user.id)
        
        Post.objects.create(title=title, author=user.username, content=content, profile_id=user_profile.id, hangar_id=hangar_id )

        return JsonResponse({ 'message': 'post created'})

