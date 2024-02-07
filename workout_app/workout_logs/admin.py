from django.contrib import admin
from .models import *

# Register Exercise and Cardio models with the Django admin site
admin.site.register(Exercise)
admin.site.register(Cardio)
