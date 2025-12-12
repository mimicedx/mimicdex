from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='images')
    designation = models.CharField(max_length=100)
    email_address =models.EmailField(max_length=100, unique=True)
    Phone_number = models.CharField(max_length=12, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.first_name


class EmployeeApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    desired_position = models.CharField(max_length=100)
    experience_years = models.IntegerField()
    education = models.CharField(max_length=200)
    skills = models.TextField()
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    photo = models.ImageField(upload_to='application_photos/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_applications')
    admin_notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-applied_at']
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.desired_position}"
    