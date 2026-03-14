from django_filters import FilterSet, CharFilter, MultipleChoiceFilter, BooleanFilter

from apps.models import JobOffer
from apps.models.job_offers import WorkingMode, ContractType, WorkingType, Experience


class JobOfferFilter(FilterSet):
    category = CharFilter(field_name="category__slug")
    working_mode = MultipleChoiceFilter(field_name="working_mode", choices=WorkingMode.choices)
    contract_type = MultipleChoiceFilter(field_name="contract_type", choices=ContractType.choices)
    working_type = MultipleChoiceFilter(field_name="working_type", choices=WorkingType.choices)
    experience = MultipleChoiceFilter(field_name="required_experience", choices=Experience.choices)
    salary_only = BooleanFilter(method="filter_salary")

    class Meta:
        model = JobOffer
        fields = []

    def filter_salary(self, queryset, name, value):
        if value:
            return queryset.filter(undisclosed_salary=False, salaries__isnull=False).distinct()
        return queryset
