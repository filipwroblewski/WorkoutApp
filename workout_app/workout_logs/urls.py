from django.urls import path
from . import views

urlpatterns = [
    # URL for the home/index page
    path('', views.index, name='index'),

    # URL for the workout history page with filtering options
    path('history/', views.history, name='history'),

    # URL for adding a new workout
    path('add_workout/', views.add_workout, name='add_workout'),

    # URL for the user profile page
    path('profile/', views.profile, name='profile'),

    # URL for deleting a specific workout with dynamic workout_id
    path('delete_workout/<int:workout_id>/', views.delete_workout, name='delete_workout'),

    # URL for editing a specific workout with dynamic workout_id
    path('edit_workout/<int:workout_id>/', views.edit_workout, name='edit_workout'),

    # URL for the Frequently Asked Questions (FAQ) page
    path('faq/', views.faq, name='faq'),
]
