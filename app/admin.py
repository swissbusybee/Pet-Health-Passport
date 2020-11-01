import json
from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.http import JsonResponse
from django.urls import path
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import FamilyGroup, Profile, Vaccine, Immunization

class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile

class VaccineResource(resources.ModelResource):
    class Meta:
        model = Vaccine

class ImmunizationResource(resources.ModelResource):
    class Meta:
        model = Immunization

class FamilyGroupResource(resources.ModelResource):
    class Meta:
        model = FamilyGroup

class ImmunizationInline(admin.TabularInline):
    model = Immunization
    fields = ("vaccine", "expired_by", "date_administered", "administered_by",)
    fk_name = "profile" 

@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ProfileResource
    list_display = ("id", "familygroup", "pet_name", "pet_microchip_id", "date_of_birth", "doctor_name_contact", "family_member_type", "created_at", "owner",)
    list_filter = ("pet_name", "pet_microchip_id", "date_of_birth", "doctor_name_contact", "family_member_type")
    search_fields = ("pet_name", "pet_microchip_id", "date_of_birth", "doctor_name_contact", "family_member_type")
    inlines = [ImmunizationInline]
    exclude = ['owner', 'familygroup']

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)

class ProfileInline(admin.TabularInline):
    model = Profile
    fields = ("pet_name", "pet_microchip_id", "date_of_birth", "doctor_name_contact", "family_member_type",)
    fk_name = "familygroup"

@admin.register(FamilyGroup)
class FamilyGroupAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = FamilyGroupResource
    list_display = ("id", "family_group_name", "owner",)
    search_fields = ("family_group_name",)
    inlines = [ProfileInline]
    exclude = ['owner',]

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)

@admin.register(Immunization)
class ImmunizationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ImmunizationResource
    list_display = ("id", "profile", "get_vaccine_name", "expired_by", "date_administered", "administered_by", "created_at", "owner",)
    list_filter = ("vaccine", "expired_by", "date_administered", "administered_by")
    search_fields = ("vaccine", "expired_by", "date_administered", "administered_by")
    exclude = ['owner', 'profile']

    def get_vaccine_name(self, obj):
        return obj.vaccine.vaccine_name
    get_vaccine_name.short_description = 'Vaccine Name'
    get_vaccine_name.admin_order_field = 'vaccine'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)  

@admin.register(Vaccine)
class VaccineAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = VaccineResource
    list_display = ("id", "vaccine_name", "required_doses","created_at")
    list_filter = ("vaccine_name", "required_doses")
    search_fields = ("vaccine_name", "required_doses")
