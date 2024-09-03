# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Engineer, Project, Assignment, TimeEntry

@login_required
def engineer_dashboard(request):
    if request.user.profile.role == 'Engineer':
        engineer = request.user.profile.associated_engineer
        assignments = Assignment.objects.filter(engineer=engineer)
        time_entries = TimeEntry.objects.filter(engineer=engineer)
        context = {
            'assignments': assignments,
            'time_entries': time_entries,
        }
        return render(request, 'engineer_dashboard.html', context)
    else:
        return redirect('home')

@login_required
def manager_dashboard(request):
    if request.user.profile.role == 'Manager':
        projects = Project.objects.all()
        engineers = Engineer.objects.all()
        context = {
            'projects': projects,
            'engineers': engineers,
        }
        return render(request, 'manager_dashboard.html', context)
    else:
        return redirect('home')

@login_required
def admin_dashboard(request):
    if request.user.profile.role == 'Admin':
        projects = Project.objects.all()
        engineers = Engineer.objects.all()
        assignments = Assignment.objects.all()
        time_entries = TimeEntry.objects.all()
        context = {
            'projects': projects,
            'engineers': engineers,
            'assignments': assignments,
            'time_entries': time_entries,
        }
        return render(request, 'admin_dashboard.html', context)
    else:
        return redirect('home')
