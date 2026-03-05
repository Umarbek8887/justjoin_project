from django.contrib import admin

from apps.models import Category, EmployerUser, User


# @admin.register(CandidateUser)
# class CandidateUserAdmin(admin.ModelAdmin):
#     list_display = ('email', 'current_position', 'years_of_exp', 'location', 'is_active')
#     list_filter = ('current_position', 'job_status', 'work_mode', 'is_active')
#     search_fields = ('email', 'location')
#     filter_horizontal = ('skills',)


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'svg')
    search_fields = ['name']


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'first_name', 'last_name')
    search_fields = ['email']


@admin.register(EmployerUser)
class EmployerUserModelAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'country')
    search_fields = ['phone_number']
