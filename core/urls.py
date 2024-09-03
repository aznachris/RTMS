from django.urls import path
from . import views

urlpatterns = [
    path('engineer_dashboard/', views.engineer_dashboard, name='engineer_dashboard'),
    path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # Add other paths as needed
]
