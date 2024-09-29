from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Client, Project, Leave, TimeEntry

# CustomUser form
class UserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone_number', 'address', 'experience_level', 'hourly_rate', 'linkedin_profile']

# Client form
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone_number', 'address']

# Project form
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'budget', 'client', 'status']

# Leave form
class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['user', 'start_date', 'end_date']

# TimeEntry form
class TimeEntryForm(forms.ModelForm):
    class Meta:
        model = TimeEntry
        fields = ['user', 'project', 'start_date', 'end_date', 'hours_spent']
