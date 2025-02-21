from django.contrib import admin
from django import forms
from .models import User, Doctor, Specialty, Patient
from django.contrib.auth.models import Group


admin.site.unregister(Group)
admin.site.register(Specialty)


class DoctorInline(admin.StackedInline):
    model = Doctor

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PatientInline(admin.StackedInline):
    model = Patient

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserForm
    
    def get_inlines(self, request, obj):
        if not obj:
            return [DoctorInline]
        
        if obj.role == "D":
            return [DoctorInline]
        
        if obj.role == "P":
            return [PatientInline]
        
        return []
        
    
    def has_change_permission(self, request, obj = ...):
        return False
    
    def has_delete_permission(self, request, obj = ...):
        return False

    def save_model(self, request, obj, form, change):
        obj.role = "D"
        obj.set_password(obj.password)
        obj.save()
