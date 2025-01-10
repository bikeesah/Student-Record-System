# students/forms.py

from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'age', 'marks']

    # Adding MinValueValidator and MaxValueValidator to marks field
    marks = forms.IntegerField(
        validators=[
            MinValueValidator(1),  # Marks should be at least 1
            MaxValueValidator(100)  # Marks should not exceed 100
        ],
        widget=forms.NumberInput(attrs={'min': 1, 'max': 100})
    )

