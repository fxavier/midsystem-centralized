from django.contrib import admin
from users.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from import_export.admin import ImportExportMixin
from core.models import (DatabaseConfig, MissedAppointment,
                         PatientEligibleVLCollection, ViralLoadTestResult,
                         Visit, ActiveInDrugMissedAppointment)
# Register your models here.


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


class VisitAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = [
        'province', 'district', 'health_facility', 'patient_identifier',
        'age', 'last_appointment_date', 'appointment_date', 'created_at',
        'sent'
    ]


class MissedAppointmentAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = [
        'id', 'province', 'district', 'health_facility', 'patient_identifier',
        'age', 'gender', 'last_appointment_date', 'sent'
    ]


class PatientEligibleVLCollectionAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = [
        'province', 'district', 'health_facility', 'patient_identifier',
        'age', 'last_vl_date', 'last_vl_value', 'last_vl_quality',
        'created_at', 'sent'
    ]


class ViralLoadTestResultAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = [
        'province', 'district', 'health_facility', 'patient_identifier',
        'age', 'last_vl_date', 'last_vl_value', 'last_vl_quality',
        'created_at', 'sent'
    ]


class GlobalPropertyAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['property_name', 'property_value']


class DatabaseConfigAdmin(ImportExportMixin, admin.ModelAdmin):

    list_display = [
        'province', 'openmrs_username', 'openmrs_password', 'openmrs_url',
        'openmrs_rest_endpoint', 'reminder_uuid', 'missed_appointment_uuid',
        'viral_load_eligibility_uuid', 'viral_load_test_result_uuid',
        'viamo_api_url', 'viamo_api_public_key'
    ]

class ActiveInDrugMissedAppointmentAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = [
        'province', 'district', 'health_facility', 'patient_identifier', 'patient_name',
        'age', 'pregnant', 'appointment_date'
        ]
    


admin.site.register(User, UserAdmin)
admin.site.register(Visit, VisitAdmin)
admin.site.register(MissedAppointment, MissedAppointmentAdmin)
admin.site.register(PatientEligibleVLCollection,
                    PatientEligibleVLCollectionAdmin)
admin.site.register(ViralLoadTestResult, ViralLoadTestResultAdmin)
admin.site.register(DatabaseConfig, DatabaseConfigAdmin)
admin.site.register(ActiveInDrugMissedAppointment, ActiveInDrugMissedAppointmentAdmin)

admin.site.site_header = 'MidSystem Centralized'
