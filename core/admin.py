from django.contrib import admin
from .models import Engineer, Project, Assignment, TimeEntry, UserProfile, Client, Report

# General Admin - Full Access
class AdminModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        # Only admins can see everything
        return super().get_queryset(request)

# Custom admin for Engineers
class EngineerAdmin(AdminModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'job_title', 'availability_status', 'hourly_rate')
    search_fields = ('name', 'email')
    list_filter = ('availability_status', 'department')

class ProjectAdmin(AdminModelAdmin):
    list_display = ('name', 'description', 'start_date', 'end_date', 'budget', 'status')
    search_fields = ('name', 'description')
    list_filter = ('status', 'start_date', 'end_date')

class AssignmentAdmin(AdminModelAdmin):
    list_display = ('engineer', 'project', 'start_date', 'end_date', 'hours_worked', 'role_in_project')
    search_fields = ('engineer__name', 'project__name')
    list_filter = ('start_date', 'end_date')

class TimeEntryAdmin(AdminModelAdmin):
    list_display = ('engineer', 'project', 'date', 'hours_worked', 'work_description')
    search_fields = ('engineer__name', 'project__name', 'work_description')
    list_filter = ('date',)

class UserProfileAdmin(AdminModelAdmin):
    list_display = ('user', 'role', 'associated_engineer')
    search_fields = ('user__username', 'associated_engineer__name')
    list_filter = ('role',)

class ClientAdmin(AdminModelAdmin):
    list_display = ('name', 'contact_person', 'email', 'phone_number')
    search_fields = ('name', 'contact_person', 'email')

class ReportAdmin(AdminModelAdmin):
    list_display = ('name', 'report_type', 'generated_by', 'generated_on')
    search_fields = ('name', 'report_type')
    list_filter = ('report_type', 'generated_on')

# Register models
admin.site.register(Engineer, EngineerAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(TimeEntry, TimeEntryAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Report, ReportAdmin)
