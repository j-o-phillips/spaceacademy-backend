from django.contrib import admin
from .models import Ship, Weapons, Shields, Engines, Thrusters

admin.site.register(Ship)
admin.site.register(Weapons)
admin.site.register(Shields)
admin.site.register(Engines)
admin.site.register(Thrusters)
