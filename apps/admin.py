from django.contrib import admin

from apps.models import Category, EmployerUser, User, Company, Salary, Language, TechStack, JobLanguage, JobTechStack
from .models import JobOffer


# @admin.register(CandidateUser)
# class CandidateUserAdmin(admin.ModelAdmin):
#     list_display = ('email', 'current_position', 'years_of_exp', 'location', 'is_active')
#     list_filter = ('current_position', 'job_status', 'work_mode', 'is_active')
#     search_fields = ('email', 'location')
#     filter_horizontal = ('skills',)


@admin.register(Company)
class CompanyModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'origin')


@admin.register(Language)
class LanguagesAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(TechStack)
class TechStackAdmin(admin.ModelAdmin):
    search_fields = ["name"]


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


class JobOfferSalaryStackedInline(admin.StackedInline):
    model = Salary
    extra = 1
    max_num = 5


class JobOfferLanguageStackedInline(admin.TabularInline):
    model = JobLanguage
    extra = 2
    max_num = 5
    autocomplete_fields = ["language"]


class JobOfferTechStackStackedInline(admin.TabularInline):
    model = JobTechStack
    extra = 3
    autocomplete_fields = ["tech_stack"]


@admin.register(JobOffer)
class OfferModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'category', 'created_at')
    search_fields = ['name', 'company__name']
    inlines = [
        JobOfferSalaryStackedInline,
        JobOfferLanguageStackedInline,
        JobOfferTechStackStackedInline
    ]
