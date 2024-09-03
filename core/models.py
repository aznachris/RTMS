from django.db import models
from django.contrib.auth.models import User

# Engineer Model
class Engineer(models.Model):
    AVAILABILITY_CHOICES = [
        ('Available', 'Available'),
        ('Busy', 'Busy'),
        ('On Leave', 'On Leave'),
        ('On Project', 'On Project')
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    job_title = models.CharField(max_length=100)
    skillset = models.TextField()  # List of skills as a comma-separated string
    experience_level = models.CharField(max_length=50)  # e.g., Junior, Mid, Senior
    certifications = models.TextField(blank=True, null=True)  # Optional
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='Available')
    department = models.CharField(max_length=100, blank=True, null=True)  # Optional
    linkedin_profile = models.URLField(blank=True, null=True)  # Optional
    current_project = models.ForeignKey('Project', on_delete=models.SET_NULL, blank=True, null=True, related_name='current_engineers')
    next_available_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

# Project Model
class Project(models.Model):
    STATUS_CHOICES = [
        ('Planned', 'Planned'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed')
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    budget = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Planned')
    project_manager = models.ForeignKey('auth.User', on_delete=models.SET_NULL, blank=True, null=True)
    client_name = models.CharField(max_length=100, blank=True, null=True)  # Optional

    def total_cost(self):
        total_hours = sum([assignment.hours_worked for assignment in self.assignments.all()])
        return total_hours * self.engineers.first().hourly_rate  # Assuming a single engineer

    def __str__(self):
        return self.name

# Assignment Model
class Assignment(models.Model):
    engineer = models.ForeignKey(Engineer, on_delete=models.CASCADE, related_name='assignments')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='assignments')
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    role_in_project = models.CharField(max_length=100, blank=True, null=True)  # e.g., Developer, QA, Lead

    def __str__(self):
        return f"{self.engineer.name} on {self.project.name}"

# Time Tracking Model (Optional)
class TimeEntry(models.Model):
    engineer = models.ForeignKey(Engineer, on_delete=models.CASCADE, related_name='time_entries')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='time_entries')
    date = models.DateField()
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    work_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.engineer.name} - {self.date} - {self.hours_worked} hours"

# User Profile Model
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('Engineer', 'Engineer')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    associated_engineer = models.OneToOneField(Engineer, on_delete=models.SET_NULL, blank=True, null=True, related_name='user_profile')

    def __str__(self):
        return self.user.username

# Client Model (Optional)
class Client(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Reports and Analytics Model (Optional)
class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ('Engineer Availability', 'Engineer Availability'),
        ('Project Cost', 'Project Cost'),
        ('Time Tracking', 'Time Tracking')
    ]

    name = models.CharField(max_length=100)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPE_CHOICES)
    filters_applied = models.JSONField()  # Storing filters as JSON
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    generated_on = models.DateTimeField(auto_now_add=True)
    report_data = models.JSONField()  # Actual report data

    def __str__(self):
        return self.name
