from users.models import UserProfile

def premium_status(request):
    # Check if the request has a user and the user is authenticated
    if hasattr(request, 'user') and request.user.is_authenticated:
        # If the user is authenticated, retrieve the user and their profile
        user = request.user
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            user_profile = None

        # Check if the user has a profile and a premium account
        if user_profile and user_profile.premium_account:
            # Check if the premium account is currently active
            is_premium_active = user_profile.premium_account.is_active()
        else:
            # If no profile or no premium account, consider premium as not active
            is_premium_active = False
    else:
        # If the user is not authenticated, consider premium as not active
        is_premium_active = False

    # Return a dictionary with the premium status
    return {'is_premium_active': is_premium_active}
