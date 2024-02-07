from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import RegisterForm
from .models import UserProfile

def index(request):
    # Check if the user is authenticated, if not, redirect to login page
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    # Render the index page for authenticated users
    return render(request, "workout_logs/index.html")

def login_view(request):
    if request.method == "POST":
        # Access username and password from the HTML form
        username = request.POST["username"]
        password = request.POST["password"]

        # Authenticate the user with provided username and password
        user = authenticate(request, username=username, password=password)

        # If authentication is successful, log in and redirect to the index page
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        # If authentication fails, return the login page with an error message
        else:
            return render(request, "users/login.html", {
                "message": "Niepoprawne dane logowania"
            })
    # Render the login page for GET requests
    return render(request, "users/login.html")

def logout_view(request):
    # Log out the user and render the login page with a logout message
    logout(request)
    return render(request, "users/login.html", {
        "message": "Wylogowano"
    })

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        # Check if the registration form is valid
        if form.is_valid():
            # Save the user and create a user profile
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            
            # Redirect to the login page after successful registration
            return redirect('login')
    else:
        # Render the registration page for GET requests
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})
