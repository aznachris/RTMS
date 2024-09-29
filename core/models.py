from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, Group, Permission

# Custom User Model
class CustomUser(AbstractUser):
    EXPERIENCE_LEVEL_CHOICES = [
        ('Junior', 'Junior'),
        ('Mid', 'Mid'),
        ('Senior', 'Senior'),
    ]

    # Add related_name to resolve clashes
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_permissions', blank=True)
    
    # Additional fields here
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    experience_level = models.CharField(max_length=10, choices=EXPERIENCE_LEVEL_CHOICES)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    name = models.CharField(max_length=255, blank=True, null=True)
    linkedin_profile = models.URLField(blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Username and email are required for auth
    
    def __str__(self):
        return self.name or self.username  # Return username if name is blank

# Groups (Custom user roles, which can be linked to permissions or handled differently)
class Group(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(CustomUser, related_name="user_groups")  # Avoiding conflict with CustomUser's groups

    def __str__(self):
        return self.name

# Clients Model
class Client(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Projects Model
class Project(models.Model):
    STATUS_CHOICES = [
        ('Planned', 'Planned'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    budget = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Planned')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, related_name='projects')

    def __str__(self):
        return self.name

# Leaves Model
class Leave(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='leaves')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.user.name} - {self.start_date} to {self.end_date}"

    # Ensure no overlapping leaves for the same user
    def clean(self):
        if Leave.objects.filter(user=self.user, start_date__lte=self.end_date, end_date__gte=self.start_date).exists():
            raise ValidationError("There is already a leave within this period.")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'start_date', 'end_date'], name='unique_leave_period')
        ]

class TimeEntry(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='time_entries', null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='time_entries')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    hours_spent = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.user.name} worked {self.hours_spent} hours on {self.project.name}"

    # Ensure the user is not on leave during time entry creation
    def clean(self):
        overlapping_leaves = Leave.objects.filter(
            user=self.user,
            start_date__lte=self.start_date,
            end_date__gte=self.end_date or self.start_date
        )
        if overlapping_leaves.exists():
            raise ValidationError("User is on leave during this period and cannot create time entries.")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'start_date', 'project'], name='unique_time_entry')
        ]