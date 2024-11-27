from django.db import transaction
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TemplateCreateForm
from .models import Template, TemplatePhase


class TemplateCreateView(LoginRequiredMixin, FormView):
    """
    Handles the creation of a new template in the database. This view processes
    the `TemplateCreateForm`, creates a `Template` instance along with associated 
    `TemplatePhase` instances if the form is valid.

    Attributes:
        form_class (Form): The form class used for creating a template.
        template_name (str): The template used for rendering the form.
        success_url (str): The URL to redirect to after a successful form submission.

    Methods:
        form_valid(form): Handles the form submission when the form is valid. Creates a new `Template` and 
                          `TemplatePhase` instances, then redirects to the success_url .
        get_success_url(): Returns the URL to redirect to after successfully creating a template, 
                           which defaults to the user's profile page.
    """
    form_class = TemplateCreateForm
    template_name = 'projects/template_create.html'
    success_url = reverse_lazy("home")

    @transaction.atomic
    def form_valid(self, form):
        industry = form.cleaned_data['industry_choice']
        template_name = form.cleaned_data['template_name']
        template_phases = form.cleaned_data['template_phases']

        template = Template.objects.create(
            industry=industry,
            template_name=template_name,
        )

        phases_list = [phase.strip()
                       for phase in template_phases.split(",") if phase.strip()]
        TemplatePhase.objects.bulk_create([
            TemplatePhase(template=template, phase_name=phase_name)
            for phase_name in phases_list
        ])

        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('profile_page', kwargs={'username': self.request.user.username})
