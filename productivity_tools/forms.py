# forms.py
from django import forms
from .models import Task, WeeklyReport


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input w-full p-4 border border-gray-300 rounded-lg text-lg focus:outline-none focus:ring-2 focus:ring-black-500',
                'placeholder': 'Entrez le titre de la tâche ici...',
            }),
        }

class weekly_report_form(forms.ModelForm):
    class Meta:
        model = WeeklyReport
        fields = ['title', 'date', 'content']