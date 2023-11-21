from django.contrib import admin
from .models import Ship, Weapons, Shields, Engines, Thrusters, Hangar, Post, Comment

admin.site.register(Ship)
admin.site.register(Weapons)
admin.site.register(Shields)
admin.site.register(Engines)
admin.site.register(Thrusters)
admin.site.register(Hangar)
admin.site.register(Post)
admin.site.register(Comment)
