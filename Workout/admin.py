from django.contrib import admin
from .models import Exercise, Performance, UserProfile

# Register your models
admin.site.register(Exercise)
admin.site.register(Performance)
admin.site.register(UserProfile)