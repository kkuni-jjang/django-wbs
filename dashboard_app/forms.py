from django import forms
from .models import Task, MeetingNote

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title', 'assignee',
            'start_date', 'end_date',
            'status', 'priority', 'progress', 'is_done'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'progress': forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 100}),
            'is_done': forms.CheckboxInput()
        }

class MeetingNoteForm(forms.ModelForm):
    class Meta:
        model = MeetingNote
        fields = ['title', 'content', 'task']
