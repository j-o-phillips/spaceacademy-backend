from django.contrib import admin
from .models import QuestionCard, UserProfile, Planet, Category, Question

# Register your models here.
admin.site.register(QuestionCard)
admin.site.register(UserProfile)
admin.site.register(Planet)
admin.site.register(Category)
admin.site.register(Question)
