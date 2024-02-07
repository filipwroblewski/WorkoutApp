from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import Exercise, Cardio
from .forms import CardioForm
from users.models import UserProfile
from users.forms import UserProfileForm

from datetime import datetime, timedelta
from decimal import Decimal

from PIL import Image

# View to display the latest 3 exercises for the logged-in user
@login_required
def index(request):
    user = request.user
    latest_exercises = Cardio.objects.order_by('-created_at').filter(user=user)[:3]
    return render(request, "workout_logs/index.html", {'latest_exercises': latest_exercises})

# View to display workout history with various filtering options
@login_required
def history(request):
    workouts = Cardio.objects.order_by('-created_at').filter(user=request.user)

    exercise_name = request.GET.get('exercise_name')
    if exercise_name:
        workouts = workouts.filter(exercise__name=exercise_name)

    exercise_info = request.GET.get('exercise_info')
    if exercise_info:
        workouts = workouts.filter(
            Q(exercise__name__icontains=exercise_info)
            | Q(comment__icontains=exercise_info)
        )

    distance_start = request.GET.get('distance_start')
    distance_end = request.GET.get('distance_end')
    if distance_start and distance_end:
        workouts = workouts.filter(distance__gte=distance_start, distance__lte=distance_end)

    date_start = request.GET.get('date_start')
    date_end = request.GET.get('date_end')
    if date_start and date_end:
        date_start = datetime.strptime(date_start, '%Y-%m-%d').date()
        date_end = datetime.strptime(date_end, '%Y-%m-%d').date()
        workouts = workouts.filter(created_at__date__range=[date_start, date_end])

    duration_start = request.GET.get('duration_start')
    duration_end = request.GET.get('duration_end')
    if duration_start and duration_end:
        duration_start = timedelta(minutes=int(duration_start))
        duration_end = timedelta(minutes=int(duration_end))
        workouts = workouts.filter(duration__gte=duration_start, duration__lte=duration_end)

    exercises = Exercise.objects.all()

    paginator = Paginator(workouts, 8)  # Show 8 workouts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'exercise_name': exercise_name,
        'exercise_info': exercise_info,
        'distance_start': distance_start,
        'distance_end': distance_end,
        'date_start': request.GET.get('date_start'),
        'date_end': request.GET.get('date_end'),
        'duration_start': duration_start,
        'duration_end': duration_end,
        'exercises': exercises,
    }
    return render(request, "workout_logs/history.html", context)

# View to add a new workout
@login_required
def add_workout(request):
    if request.method == 'POST':
        # Extract workout details from the form and create a new Cardio instance
        exercise_id = request.POST.get('exercise')
        exercise = Exercise.objects.get(id=exercise_id)
        duration_minutes = int(request.POST.get('duration'))
        duration = timedelta(minutes=duration_minutes)
        distance = Decimal(request.POST.get('distance'))
        comment = request.POST.get('comment')
        created_at_str = request.POST.get('created_at')
        created_at = datetime.strptime(created_at_str, '%Y-%m-%dT%H:%M')
        workout = Cardio.objects.create(
            user=request.user,
            exercise=exercise,
            duration=duration,
            distance=distance,
            comment=comment,
            created_at=created_at
        )
        messages.success(request, f'{exercise} {distance}km ({duration})')

    exercises = Exercise.objects.all()

    context = {
        'exercises': exercises,
    }
    return render(request, "workout_logs/add_workout.html", context)

# View to delete a workout
@login_required
def delete_workout(request, workout_id):
    workout = get_object_or_404(Cardio, id=workout_id)

    # Check if the logged-in user is the owner of the workout before deleting
    if request.user == workout.user:
        workout.delete()
        return redirect('index')
    else:
        return HttpResponse('Permission Denied', status=403)

# View to edit a workout
@login_required
def edit_workout(request, workout_id):
    workout = get_object_or_404(Cardio, id=workout_id, user=request.user)

    if request.method == 'POST':
        form = CardioForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()

            # Update the duration in minutes based on the form data
            duration_minutes = int(request.POST.get('duration'))
            workout.duration = timedelta(minutes=duration_minutes)
            workout.save()

            return redirect('history')  # Redirect to the history page after editing
    else:
        form = CardioForm(instance=workout)
        duration_minutes = int(workout.duration.total_seconds() // 60)

    exercises = Exercise.objects.all()

    context = {
        'form': form,
        'current_workout': workout,
        'exercises': exercises,
        'duration_minutes': duration_minutes,
    }
    return render(request, 'workout_logs/edit_workout.html', context)

# View to display and update user profile information
@login_required
def profile(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    context = {
        'form': form,
        'user_profile': user_profile,
    }
    return render(request, "workout_logs/profile.html", context)

# View to display FAQ page
def faq(request):
    return render(request, "workout_logs/faq.html")
