from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from .models import User

class CustomUserAdmin(UserAdmin):
    # List View
    list_display = (
        'email', 
        'username', 
        'get_verification_status',  # Changed from verification_status
        'is_active', 
        'date_joined',
    )
    
    list_filter = ('is_email_verified', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('-date_joined',)
    
    #Edit view
    fieldsets = (
        ('Login Credentials', {
            'fields': ('email', 'username', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name'),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Verification', {
            'fields': ('is_email_verified',),
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('date_joined', 'last_login')
    
    # Custom display methods
    
    def get_verification_status(self, obj):
        """Display colored verification status"""
        if obj.is_email_verified:
            return " Verified"
        return " Unverified"
    get_verification_status.short_description = 'Status'
    get_verification_status.admin_order_field = 'is_email_verified'
    
    # Bulk actions
    
    actions = ['make_verified', 'make_unverified', 'activate_users', 'deactivate_users']
    
    def make_verified(self, request, queryset):
        count = queryset.update(is_email_verified=True)
        self.message_user(request, f"✅ {count} users marked as verified.")
    make_verified.short_description = "Mark selected users as verified"
    
    def make_unverified(self, request, queryset):
        count = queryset.update(is_email_verified=False)
        self.message_user(request, f"⚠️ {count} users marked as unverified.")
    make_unverified.short_description = "Mark selected users as unverified"
    
    def activate_users(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"✅ {count} users activated.")
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"⚠️ {count} users deactivated.")
    deactivate_users.short_description = "Deactivate selected users"

# REGISTER THE MODEL
admin.site.register(User, CustomUserAdmin)