from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from learn_app.models import UserProfile
from .models import Ship, Weapons, Shields, Engines, Thrusters
from .serializers import ShipSerializer, WeaponsSerializer, ThrustersSerializer, EnginesSerializer, ShieldsSerializer

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
