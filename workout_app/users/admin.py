from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, PremiumAccount

class UserProfileInline(admin.StackedInline):
    """
    Inline configuration for the UserProfile model within the User admin page.
    """
    model = UserProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    """
    Custom User admin configuration to include UserProfileInline.
    """
    inlines = (UserProfileInline,)

# Unregister the default User admin and register with CustomUserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register PremiumAccount model in the admin panel
admin.site.register(PremiumAccount)
