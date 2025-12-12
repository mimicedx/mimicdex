from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Employee, EmployeeApplication

@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})

@login_required
def employee_detail(request, pk):
    employee = Employee.objects.get(pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee': employee})

@login_required
def apply_for_job(request):
    # Check if user already has a pending application
    existing_app = EmployeeApplication.objects.filter(user=request.user, status='pending').first()
    if existing_app:
        messages.info(request, 'You already have a pending application. Please wait for admin review.')
        return redirect('application_status')
    
    if request.method == 'POST':
        application = EmployeeApplication(
            user=request.user,
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            phone_number=request.POST['phone_number'],
            desired_position=request.POST['desired_position'],
            experience_years=request.POST['experience_years'],
            education=request.POST['education'],
            skills=request.POST['skills'],
            cover_letter=request.POST['cover_letter'],
        )
        
        if 'resume' in request.FILES:
            application.resume = request.FILES['resume']
        if 'photo' in request.FILES:
            application.photo = request.FILES['photo']
            
        application.save()
        messages.success(request, 'Your application has been submitted successfully! You will be notified once it\'s reviewed.')
        return redirect('application_status')
    
    return render(request, 'employees/apply.html')

@login_required
def application_status(request):
    applications = EmployeeApplication.objects.filter(user=request.user)
    return render(request, 'employees/application_status.html', {'applications': applications})
