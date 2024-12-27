import uuid
from django.db import models
from apps.organizations.models import Organization
from apps.users.models import User

# Create your models here.


class Industry(models.Model):
    """
    Represents an industry category for organizing project templates.

    The `Industry` model is used to classify templates into specific categories 
    based on industry type. This categorization helps users easily find and 
    apply relevant templates for their projects. Each industry is uniquely identified
    by an `industry_id`, which is a UUID.

    Attributes:
        industry_id (UUIDField): A unique identifier for the industry.
        industry_name (CharField): The name of the industry e.g., 'Construction'.
    """

    industry_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Industry ID")
    industry_name = models.CharField(
        max_length=50, unique=True, verbose_name="Industry name")

    class Meta:
        verbose_name_plural = "Industries"

    def __str__(self) -> str:
        return self.industry_name


def get_default_industry():
    """
    Retrieves the default industry to be used when a template references a deleted industry.

    Returns:
        UUID: The unique identifier (industry_id) of the default industry, 
            which is the "Other" industry.
    """
    industry = Industry.objects.get_or_create(industry_name="Other")
    return industry.pk


class Template(models.Model):
    """
    Represents a reusable project template that is categorized by industry.

    The `Template` model stores project templates that users can apply to their own 
    projects. Each template is linked to a specific `Industry`, allowing for better 
    organization and searchability.

    Attributes:
        industry_id (ForeignKey): A reference to the `Industry` that the template 
                                   belongs to. If the industry is deleted, it is 
                                   set to the default industry using `get_default_industry`.
        template_id (UUIDField): A unique identifier for the template, automatically 
                                 generated using UUID.
        template_name (CharField): The name of the template.
    """
    industry = models.ForeignKey(Industry, on_delete=models.SET_DEFAULT,
                                 default=get_default_industry, related_name="templates", verbose_name="Industry ID")
    template_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, verbose_name="Template ID")
    template_name = models.CharField(
        max_length=50, verbose_name="Template name")

    def __str__(self) -> str:
        return self.template_name


class TemplatePhase(models.Model):
    """
    Represents a phase within a template. A phase could be a step or stage 
    within a template, such as 'Design', 'Testing', etc.

    Attributes:
        template (ForeignKey): A reference to the `Template` that the phase belongs to.
        phase_id (UUIDField): A unique identifier for the phase, automatically generated using UUID.
        phase_name (CharField): The name of the phase, such as 'Design', 'Development', etc.
    """
    template = models.ForeignKey(
        Template, on_delete=models.RESTRICT, related_name="phases", verbose_name="Template"
    )
    phase_id = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=True, verbose_name="Phase ID")
    phase_name = models.CharField(max_length=50, verbose_name="Phase name")

    def __str__(self) -> str:
        return self.phase_name


class Project(models.Model):
    """
    Represents a project within an organization.

    This model tracks essential project information such as its template,
    deadlines, and current status, and associates it with an organization.
    """
    IN_PROGRESS = "IN_PROGRESS"
    ON_HOLD = "ON_HOLD"
    DONE = "DONE"

    PROJECT_STATUS_CHOICES = [
        (IN_PROGRESS, "In progress"),
        (ON_HOLD, "ON_HOLD"),
        (DONE, "Done"),
    ]
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     related_name="projects", help_text="The organization that owns or manages this project.",
                                     verbose_name="Project organization")
    template = models.ForeignKey(
        Template, on_delete=models.RESTRICT,
        help_text="The template from which this project is based.",
        verbose_name="Project base template")
    project_id = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=True,
        help_text="A unique identifier for the project, generated automatically.",
        verbose_name="Project ID")
    project_name = models.CharField(
        max_length=120, help_text="The name of the project, unique within the organization.", verbose_name="Project name")
    project_name_slug = models.SlugField(
        max_length=255, help_text="A URL-safe slug version of the project name.", verbose_name="Project Name Slug")
    description = models.TextField(
        blank=True, verbose_name="Project description")
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="The date and time when the project was created.",
        verbose_name="Project creation date")
    deadline = models.DateField(
        help_text="The date and time by which the project should be completed.",
        verbose_name="Deadline date")
    status = models.CharField(
        max_length=15,
        choices=PROJECT_STATUS_CHOICES,
        default=IN_PROGRESS,
        help_text="The current status of the project.",
        verbose_name="Project status"
    )

    def __str__(self) -> str:
        return self.project_name


class ProjectMember(models.Model):
    """
    Represents users who are members of a `Project` 
    """

    member = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Project Member")
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="members", verbose_name="Project")


class CustomPhase(models.Model):
    """
    Represents a custom project phase.

    This model allows a project to define custom phases when the predefined phases 
    in a template do not fully meet the project's requirements.
    """

    phase_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Phase ID")
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                help_text="The project which created this phase", related_name="custom_phases", verbose_name="Project")
    phase_name = models.CharField(
        max_length=50, help_text="The name of the project phase.", verbose_name="Phase name")


class ProjectPhase(models.Model):
    """
    Represents a phase within a project. This model links the project to its various phases, which can either be inherited from a template
    or be custom-specific phases created for the project.
    """
    phase_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Phase id")
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                related_name="phases", help_text="Project which this phase belongs to", verbose_name="Project")
    # The `on_delete=models.RESTRICT` ensures that a template phase cannot be deleted if it is being used in a project.
    template_phase = models.ForeignKey(
        TemplatePhase, on_delete=models.RESTRICT, null=True, help_text="Project phase inheritied from a template", verbose_name="Template phase")
    custom_phase = models.ForeignKey(CustomPhase, on_delete=models.CASCADE, null=True,
                                     help_text="Custom phase specific to this project", verbose_name='Custom phase')

    def __str__(self) -> str:
        return f'{self.project.project_name}| {self.template_phase.phase_name or self.custom_phase.phase_name}'
