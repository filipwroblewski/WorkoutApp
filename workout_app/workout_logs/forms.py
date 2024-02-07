from django import forms
from .models import Cardio

# Form for capturing Cardio exercise details
class CardioForm(forms.ModelForm):
    class Meta:
        # Associate the form with the Cardio model
        model = Cardio

        # Specify the fields to be included in the form
        fields = ['exercise', 'created_at', 'duration', 'distance', 'comment']