from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Group, Client, Project, Leave, TimeEntry

# Custom UserAdmin for CustomUser model
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('name', 'email', 'phone_number', 'experience_level', 'hourly_rate', 'linkedin_profile')
    search_fields = ('name', 'email', 'phone_number')
    list_filter = ('experience_level',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('name', 'email', 'phone_number', 'address', 'linkedin_profile')}),
        ('Professional Info', {'fields': ('experience_level', 'hourly_rate')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password1', 'password2', 'phone_number', 'address', 'experience_level', 'hourly_rate', 'linkedin_profile')}
        ),
    )
    ordering = ('email',)

# Custom Admin for Group model
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('users',)  # Allows for a better user-group relationship management

# Custom Admin for Client model
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'email', 'phone_number')
    search_fields = ('name', 'contact_person', 'email', 'phone_number')
    list_filter = ('name',)

# Custom Admin for Project model
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'start_date', 'end_date', 'status', 'budget')
    search_fields = ('name', 'client__name')
    list_filter = ('status', 'start_date', 'end_date')
    ordering = ('start_date',)

# Custom Admin for Leave model
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'end_date')
    search_fields = ('user__name', 'start_date')
    list_filter = ('start_date', 'end_date')

# Custom Admin for TimeEntry model
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'start_date', 'end_date', 'hours_spent')
    search_fields = ('user__name', 'project__name', 'start_date')
    list_filter = ('start_date', 'end_date')

# Register models with custom admins
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Leave, LeaveAdmin)
admin.site.register(TimeEntry, TimeEntryAdmin)
