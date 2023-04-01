from .models import *
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from base.models import HealthWorker


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = HealthWorker
        fields = ('email', 'firstName', 'middleName', 'lastName', 'date_of_birth', 'health_center', 'is_healthworker', 'is_admin')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def clean(self):
        is_healthworker = self.cleaned_data.get('is_healthworker')
        is_admin = self.cleaned_data.get('is_admin')
        if not is_healthworker and not is_admin:
            raise ValidationError('Please select at least one(1) permission before proceeding')
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = HealthWorker
        fields = ('email', 'firstName', 'middleName', 'lastName', 'date_of_birth', 'health_center', 'is_healthworker', 'is_admin')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2
    
    def clean(self):
        is_healthworker = self.cleaned_data.get('is_healthworker')
        is_admin = self.cleaned_data.get('is_admin')
        if not is_healthworker and not is_admin:
            raise ValidationError('Please select at least one(1) permission before proceeding')
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'firstName', 'middleName', 'lastName', 'date_of_birth', 'health_center', 'is_healthworker', 'is_admin', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Register your models here.
admin.site.register(HealthCenter)
admin.site.register(Patient)
admin.site.register(MedicalRecord)
admin.site.register(MedicalSupply)
admin.site.register(Prescription)
admin.site.register(Bill)
admin.site.register(OutbreakReport)
admin.site.register(Appointment)
admin.site.register(HealthWorker, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)