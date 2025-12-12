from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile Information'
    fields = ('registration_date', 'last_login_ip', 'is_email_verified')
    readonly_fields = ('registration_date',)


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined', 'get_registration_date')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'userprofile__registration_date')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    def get_registration_date(self, obj):
        if hasattr(obj, 'userprofile'):
            return obj.userprofile.registration_date
        return None
    get_registration_date.short_description = 'Registration Date'
    get_registration_date.admin_order_field = 'userprofile__registration_date'


# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Also register UserProfile separately for direct access
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'registration_date', 'last_login_ip', 'is_email_verified')
    list_filter = ('registration_date', 'is_email_verified')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('registration_date',)
    ordering = ('-registration_date',)