from django.contrib import admin
from django.utils import timezone
from .models import Employee, EmployeeApplication

# Register your models here.
admin.site.register(Employee)

@admin.register(EmployeeApplication)
class EmployeeApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'desired_position', 'status', 'applied_at', 'experience_years')
    list_filter = ('status', 'applied_at', 'desired_position')
    search_fields = ('first_name', 'last_name', 'email', 'desired_position')
    readonly_fields = ('applied_at', 'user')
    
    fieldsets = (
        ('Applicant Information', {
            'fields': ('user', 'first_name', 'last_name', 'email', 'phone_number')
        }),
        ('Application Details', {
            'fields': ('desired_position', 'experience_years', 'education', 'skills', 'cover_letter')
        }),
        ('Files', {
            'fields': ('resume', 'photo')
        }),
        ('Review', {
            'fields': ('status', 'admin_notes', 'reviewed_by', 'reviewed_at')
        }),
        ('Timestamps', {
            'fields': ('applied_at',)
        })
    )
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Full Name'
    
    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data:
            obj.reviewed_by = request.user
            obj.reviewed_at = timezone.now()
        super().save_model(request, obj, form, change)
    
    actions = ['approve_applications', 'reject_applications']
    
    def approve_applications(self, request, queryset):
        updated = queryset.update(
            status='approved',
            reviewed_by=request.user,
            reviewed_at=timezone.now()
        )
        self.message_user(request, f'{updated} applications approved.')
    approve_applications.short_description = 'Approve selected applications'
    
    def reject_applications(self, request, queryset):
        updated = queryset.update(
            status='rejected',
            reviewed_by=request.user,
            reviewed_at=timezone.now()
        )
        self.message_user(request, f'{updated} applications rejected.')
    reject_applications.short_description = 'Reject selected applications'