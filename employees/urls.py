from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('<int:pk>/', views.employee_detail, name='employee_detail'),
    path('apply/', views.apply_for_job, name='apply'),
    path('application-status/', views.application_status, name='application_status'),
]