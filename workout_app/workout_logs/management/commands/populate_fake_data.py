from django.core.management.base import BaseCommand
from workout_logs.models import Exercise, Cardio
from faker import Faker
from django.contrib.auth.models import User
from django.utils import timezone
import random
from datetime import timedelta

fake = Faker('pl_PL')

class Command(BaseCommand):
    help = 'Populate Exercise and Cardio model instances with fake data'

    def create_fake_exercises(self, num_exercises, predefined_exercise_names):
        """
        Generate Exercise instances with random or predefined names.

        Args:
        - num_exercises (int): Number of Exercise instances to generate.
        - predefined_exercise_names (list): List of predefined exercise names.

        Returns:
        - list: List of generated Exercise instances.
        """
        exercises = []

        # Shuffle the predefined exercise names to choose randomly
        shuffled_exercises = predefined_exercise_names.copy()
        random.shuffle(shuffled_exercises)

        for _ in range(num_exercises):
            # Use a predefined name if available, otherwise generate a random word
            exercise_name = shuffled_exercises.pop() if shuffled_exercises else fake.word().capitalize()
            exercise = Exercise.objects.create(
                name=exercise_name,
            )
            exercises.append(exercise)
        return exercises

    def create_fake_cardio_data(self, users, exercises, num_entries):
        """
        Generate fake Cardio data entries for users and exercises.

        Args:
        - users (QuerySet): QuerySet of User instances.
        - exercises (list): List of Exercise instances.
        - num_entries (int): Number of Cardio data entries per user.

        Returns:
        - None
        """
        for user in users:
            for _ in range(num_entries):
                exercise = fake.random_element(exercises)
                Cardio.objects.create(
                    user=user,
                    exercise=exercise,
                    created_at=fake.date_time_this_decade(tzinfo=timezone.utc),
                    duration=timedelta(minutes=fake.random_int(min=30, max=180)),
                    distance=fake.pydecimal(min_value=1, max_value=20, right_digits=2),
                    comment=fake.text(),
                )

    def handle(self, *args, **options):
        predefined_exercise_names = [
            'Bieganie',
            'Jazda na rowerze',
            'Pływanie',
            'Wioślarstwo',
            'Sprint',
            'Rowerek stacjonarny',
            'Orbitrek',
            'Wchodzenie po schodach',
            'Wycieczka górska',
            'Bieżnia',
            'Jazda na nartach',
            'Ergometr wioślarski',
            'Bieg z przeszkodami',
            'Jogging',
            'Jazda na BMX',
            'Żeglarstwo',
            'Serfowanie',
            'Chodziarstwo',
        ]

        # Generate Exercise instances with random names
        num_exercises = 8
        exercises = self.create_fake_exercises(num_exercises, predefined_exercise_names)

        # Generate fake Cardio data
        users = User.objects.all()
        num_entries_per_user = 42
        self.create_fake_cardio_data(users, exercises, num_entries_per_user)

        self.stdout.write(self.style.SUCCESS('Successfully populated data'))
