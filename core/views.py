from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from .models import CustomUser, Group, Client, Project, Leave, TimeEntry
from .forms import UserForm, ClientForm, ProjectForm, LeaveForm, TimeEntryForm

# Custom user and group views

@login_required
def dashboard(request):
    """Main dashboard for logged in users."""
    return render(request, 'dashboard.html')

class UserListView(ListView):
    model = CustomUser
    template_name = 'users/user_list.html'
    context_object_name = 'users'

class UserDetailView(DetailView):
    model = CustomUser
    template_name = 'users/user_detail.html'
    context_object_name = 'user'

class UserCreateView(CreateView):
    model = CustomUser
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')

class UserUpdateView(UpdateView):
    model = CustomUser
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')

class UserDeleteView(DeleteView):
    model = CustomUser
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

class GroupListView(ListView):
    model = Group
    template_name = 'groups/group_list.html'
    context_object_name = 'groups'

class GroupDetailView(DetailView):
    model = Group
    template_name = 'groups/group_detail.html'
    context_object_name = 'group'

class GroupCreateView(CreateView):
    model = Group
    template_name = 'groups/group_form.html'
    fields = ['name', 'users']
    success_url = reverse_lazy('group_list')

class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'groups/group_form.html'
    fields = ['name', 'users']
    success_url = reverse_lazy('group_list')

class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'groups/group_confirm_delete.html'
    success_url = reverse_lazy('group_list')

# Client views

class ClientListView(ListView):
    model = Client
    template_name = 'clients/client_list.html'
    context_object_name = 'clients'

class ClientDetailView(DetailView):
    model = Client
    template_name = 'clients/client_detail.html'
    context_object_name = 'client'

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('client_list')

class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('client_list')

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'clients/client_confirm_delete.html'
    success_url = reverse_lazy('client_list')

# Project views

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project_list')

class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project_list')

class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')

# Leave views

class LeaveListView(ListView):
    model = Leave
    template_name = 'leaves/leave_list.html'
    context_object_name = 'leaves'

class LeaveCreateView(CreateView):
    model = Leave
    form_class = LeaveForm
    template_name = 'leaves/leave_form.html'
    success_url = reverse_lazy('leave_list')

class LeaveUpdateView(UpdateView):
    model = Leave
    form_class = LeaveForm
    template_name = 'leaves/leave_form.html'
    success_url = reverse_lazy('leave_list')

class LeaveDeleteView(DeleteView):
    model = Leave
    template_name = 'leaves/leave_confirm_delete.html'
    success_url = reverse_lazy('leave_list')

# Time Entry views

class TimeEntryListView(ListView):
    model = TimeEntry
    template_name = 'time_entries/time_entry_list.html'
    context_object_name = 'time_entries'

class TimeEntryCreateView(CreateView):
    model = TimeEntry
    form_class = TimeEntryForm
    template_name = 'time_entries/time_entry_form.html'
    success_url = reverse_lazy('time_entry_list')

    def form_valid(self, form):
        """Override form_valid to check if the engineer is on leave before saving."""
        user = form.cleaned_data['user']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        # Check if the user is on leave during the time entry period
        if Leave.objects.filter(user=user, start_date__lte=start_date, end_date__gte=end_date).exists():
            form.add_error(None, "The engineer is on leave during this time period.")
            return self.form_invalid(form)
        return super().form_valid(form)

class TimeEntryUpdateView(UpdateView):
    model = TimeEntry
    form_class = TimeEntryForm
    template_name = 'time_entries/time_entry_form.html'
    success_url = reverse_lazy('time_entry_list')

    def form_valid(self, form):
        """Check if the engineer is on leave before updating."""
        user = form.cleaned_data['user']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        if Leave.objects.filter(user=user, start_date__lte=start_date, end_date__gte=end_date).exists():
            form.add_error(None, "The engineer is on leave during this time period.")
            return self.form_invalid(form)
        return super().form_valid(form)

class TimeEntryDeleteView(DeleteView):
    model = TimeEntry
    template_name = 'time_entries/time_entry_confirm_delete.html'
    success_url = reverse_lazy('time_entry_list')

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
