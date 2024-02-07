from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Model for types of exercises
class Exercise(models.Model):
    # Name of the exercise
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

# Model for Cardio exercises
class Cardio(models.Model):
    # User associated with the exercise
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    # Type of exercise (linked to Exercise model)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, default=1)

    # Date and time when the exercise was created
    created_at = models.DateTimeField(default=timezone.now)

    # Duration of the exercise
    duration = models.DurationField(null=True, default=0)

    # Distance covered during the exercise
    distance = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    # Additional comments for the exercise
    comment = models.TextField(default='')

    def __str__(self):
        # String representation of the Cardio exercise
        return f"{self.user.username}'s {self.exercise.name}"
