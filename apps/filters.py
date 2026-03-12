class JobOfferFilter:
    def __init__(self, request, queryset):
        self.request = request
        self.qs = queryset

    def filter(self):
        qs = self.qs

        category = self.request.GET.get("category")
        working_mode = self.request.GET.getlist("working_mode")
        contract_type = self.request.GET.getlist("contract_type")
        working_type = self.request.GET.getlist("working_type")
        experience = self.request.GET.getlist("experience")
        salary_only = self.request.GET.get("salary_only")

        if category:
            qs = qs.filter(category__slug=category)

        if working_mode:
            qs = qs.filter(working_mode__in=working_mode)

        if contract_type:
            qs = qs.filter(contract_type__in=contract_type)

        if working_type:
            qs = qs.filter(working_type__in=working_type)

        if experience:
            qs = qs.filter(required_experience__in=experience)

        if salary_only:
            qs = qs.filter(undisclosed_salary=False, salaries__isnull=False).distinct()

        return qs
