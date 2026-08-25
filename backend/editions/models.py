from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from formbuilder.models import FieldsetField
from users.models import User
from utils.models import CommonTimeStampModel
from utils.storage import select_public_storage
from utils.translation import TranslateableTextField


class Edition(CommonTimeStampModel):
    """
    Data about an edition
    """

    # Description settings
    title = TranslateableTextField(verbose_name="title", blank=True, null=False, default=dict)
    description = TranslateableTextField(verbose_name="description", blank=True, null=False, default=dict)

    # Jury settings
    jury_users = models.ManyToManyField(User, verbose_name="jury users")

    # Visibility settings
    is_published = models.BooleanField(verbose_name="is published", null=False, default=False)
    is_readonly = models.BooleanField(verbose_name="is readonly", null=False, default=False)

    # Budget settings
    total_budget = models.DecimalField(
        verbose_name=_("total edition budget"),
        help_text=_("The total budget for this edition"),
        max_digits=14,
        decimal_places=2,
        default=Decimal(0),
        null=False,
        blank=True,
    )  # type: ignore
    individual_budget = models.DecimalField(
        verbose_name=_("individual project budget"),
        help_text=_("The maximum budget per project"),
        max_digits=14,
        decimal_places=2,
        default=Decimal(0),
        null=False,
        blank=True,
    )  # type: ignore
    budget_currency = models.CharField(verbose_name="budget currency", max_length=3, blank=True, null=False)

    # Computed data from related models
    cached_begins_on = models.DateTimeField(editable=False, blank=True, null=True)
    cached_ends_on = models.DateTimeField(editable=False, blank=True, null=True)

    # Type hinting for related models
    editionstage_set: "models.manager.RelatedManager[EditionStage]"

    # Model managers
    objects = models.Manager()

    class Meta:  # type: ignore
        verbose_name = _("edition")
        verbose_name_plural = _("editions")

    def __str__(self) -> str:
        return _("Edition {id}: {title}").format(id=self.pk, title=self.title)

    def refresh_cache(self, commit=True):
        try:
            self.cached_begins_on = self.editionstage_set.earliest("begins_on").begins_on
        except EditionStage.DoesNotExist:
            self.cached_begins_on = None

        try:
            self.cached_ends_on = self.editionstage_set.latest("ends_on").ends_on
        except EditionStage.DoesNotExist:
            self.cached_ends_on = None

        if commit:
            self.save()


class EditionRelatedModel(models.Model):
    """
    Helper for grouping the edition related classes
    """

    edition = models.ForeignKey(Edition, verbose_name="edition", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True

    @classmethod
    def sweep_items(cls) -> models.QuerySet:
        """
        Gather all edition related items for deleted editions
        """

        return cls.objects.filter(edition__isnull=True).all()


class EditionPublicDocument(EditionRelatedModel, CommonTimeStampModel):
    """
    Uploaded edition files for public view
    """

    uploaded_document = models.FileField(
        verbose_name=_("uploaded document"),
        upload_to="editions_public/%Y/%W/",
        storage=select_public_storage,
        blank=True,
        null=True,
    )
    linked_document_url = models.CharField(
        verbose_name=_("linked document URL"),
        max_length=2048,
        blank=True,
        null=False,
        default="",
        help_text=_("If the user entered a link instead of a file upload"),
    )

    # Model managers
    objects = models.Manager()

    class Meta:  # type: ignore
        verbose_name = _("edition public document")
        verbose_name_plural = _("edition public documents")

    def __str__(self) -> str:
        return _("(Edition {edition_id}) Public Document {id}").format(
            edition_id=self.edition.pk if self.edition else 0, id=self.pk
        )


class FinancingDomain(EditionRelatedModel, CommonTimeStampModel):
    title = TranslateableTextField(verbose_name="title", blank=True, null=False, default=dict)

    # Model managers
    objects = models.Manager()

    class Meta:  # type: ignore
        ordering = ("title",)
        verbose_name = _("financing domain")
        verbose_name_plural = _("financing domains")

    def __str__(self) -> str:
        return _("(Edition {edition_id}) Financing Domain {id}: {title}").format(
            edition_id=self.edition.pk if self.edition else 0, id=self.pk, title=self.title
        )


class JuryForm(CommonTimeStampModel):
    title = TranslateableTextField(verbose_name="title", blank=True, null=False, default=dict)
    fieldset = FieldsetField(verbose_name="fieldset", blank=True, null=False, default=dict)
    min_score = models.PositiveSmallIntegerField(verbose_name="minimum score", blank=True, null=False, default=0)
    max_score = models.PositiveSmallIntegerField(verbose_name="maximum score", blank=True, null=False, default=10)

    # Model managers
    objects = models.Manager()

    class Meta:  # type: ignore
        verbose_name = _("jury form")
        verbose_name_plural = _("jury forms")

    def __str__(self) -> str:
        return _("Jury Form {id}: {title}").format(id=self.pk, title=self.title)


class ProjectForm(CommonTimeStampModel):
    title = TranslateableTextField(verbose_name="title", blank=True, null=False, default=dict)
    fieldset = FieldsetField(verbose_name="fieldset", blank=True, null=False, default=dict)

    # Model managers
    objects = models.Manager()

    class Meta:  # type: ignore
        verbose_name = _("project form")
        verbose_name_plural = _("project forms")

    def __str__(self) -> str:
        return _("Project Form {id}: {title}").format(id=self.pk, title=self.title)


class EditionStage(EditionRelatedModel, CommonTimeStampModel):
    """
    Data about an edition stage
    """

    class StageTypeChoices(models.TextChoices):
        FORM = "FORM", _("Form Completion")
        JURY = "JURY", _("Jury Scoring")
        OTHER = "OTHER", _("Other")

    title = TranslateableTextField(verbose_name="title", blank=True, null=False, default=dict)
    stage_type = models.CharField(
        verbose_name="stage type",
        max_length=5,
        blank=False,
        null=False,
        choices=StageTypeChoices,
        default=StageTypeChoices.FORM,
    )
    description = TranslateableTextField(verbose_name="description", blank=True, null=False, default=dict)
    begins_on = models.DateTimeField(verbose_name="begins on", blank=False, null=False)
    ends_on = models.DateTimeField(verbose_name="ends on", blank=False, null=False)
    project_form = models.ForeignKey(
        ProjectForm, verbose_name="project form", blank=True, null=True, on_delete=models.SET_NULL
    )
    jury_form = models.ForeignKey(JuryForm, verbose_name="jury form", blank=True, null=True, on_delete=models.SET_NULL)

    # Model managers
    objects = models.Manager()

    class Meta:  # type: ignore
        verbose_name = _("edition stage")
        verbose_name_plural = _("edition stages")

    def __str__(self) -> str:
        return _("(Edition {edition_id}) Stage {id}: {title}").format(
            edition_id=self.edition.pk if self.edition else 0, id=self.pk, title=self.title
        )


class EditionStageRelatedModel(models.Model):
    """
    Helper for grouping the edition stage related classes
    """

    edition_stage = models.ForeignKey(
        EditionStage, verbose_name="edition stage", blank=True, null=True, on_delete=models.SET_NULL
    )

    class Meta:
        abstract = True

    @classmethod
    def sweep_items(cls) -> models.QuerySet:
        """
        Gather all edition stage related items for deleted edition stages
        """

        return cls.objects.filter(edition_stage__isnull=True).all()


class Project(EditionRelatedModel, CommonTimeStampModel):
    """
    Project metadata and configuration
    """

    title = TranslateableTextField(verbose_name="title", blank=True, null=False, default=dict)

    # Model managers
    objects = models.Manager()

    class Meta:  # type: ignore
        verbose_name = _("project")
        verbose_name_plural = _("projects")

    def __str__(self) -> str:
        return _("(Edition {edition_id}) Project {id}: {title}").format(
            edition_id=self.edition.pk if self.edition else 0, id=self.pk, title=self.title
        )


class ProjectRelatedModel(models.Model):
    """
    Helper for grouping the project related classes
    """

    project = models.ForeignKey(Project, verbose_name="project", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True

    @classmethod
    def sweep_items(cls) -> models.QuerySet:
        """
        Gather all project related items for deleted projects
        """

        return cls.objects.filter(project__isnull=True).all()


class TopLevelCommentManager(models.Manager):
    """
    Look for comments which are not a reply to another comment
    """

    def get_queryset(self):
        return super().get_queryset().filter(parent_comment__isnull=True)


class ProjectComment(ProjectRelatedModel, CommonTimeStampModel):
    """
    User comment about a project
    """

    author = models.ForeignKey(User, verbose_name="user", null=True, blank=True, on_delete=models.SET_NULL)
    parent_comment = models.ForeignKey("ProjectComment", verbose_name="parent comment", on_delete=models.CASCADE)
    title = TranslateableTextField(verbose_name="title", blank=True, null=False, default=dict)
    message = TranslateableTextField(verbose_name="message", blank=True, null=False, default=dict)

    # Model managers
    objects = models.Manager()
    top_level = TopLevelCommentManager()

    class Meta:  # type: ignore
        verbose_name = _("project comment")
        verbose_name_plural = _("project comments")

    def __str__(self) -> str:
        return _("(Project {project_id}) Comment {id}: {title}").format(
            project_id=self.project.pk if self.project else 0, id=self.pk, title=self.title[:32]
        )


class ProjectJury(EditionStageRelatedModel, ProjectRelatedModel, CommonTimeStampModel):
    """
    Project jury assignment for an edition stage
    """

    jury_users = models.ManyToManyField(User, verbose_name="jury users")
    cached_total_score = models.PositiveSmallIntegerField(editable=False, null=False, default=0)
    cached_average_score = models.FloatField(editable=False, null=False, default=0)

    # Model managers
    objects = models.Manager()

    class Meta:  # type: ignore
        verbose_name = _("project jury")
        verbose_name_plural = _("project juries")

    @classmethod
    def sweep_items(cls) -> models.QuerySet:
        """
        Gather all items for deleted edition stages or deleted projects
        """

        return cls.objects.filter(edition__isnull=True).all() | cls.objects.filter(project__isnull=True).all()

    def __str__(self) -> str:
        return _("(Project {project_id} Stage {edition_stage_id}) Jury {id}").format(
            project_id=self.project.pk if self.project else 0,
            edition_stage_id=self.edition_stage.pk if self.edition_stage else 0,
            id=self.pk,
        )


class JuryScorecard(EditionStageRelatedModel, ProjectRelatedModel, CommonTimeStampModel):
    """
    One jury user's score card for a project
    """

    jury_user = models.ForeignKey(User, verbose_name="jury user", blank=True, null=True, on_delete=models.SET_NULL)
    data = models.JSONField(verbose_name="data", null=True, blank=True)
    total_score = models.PositiveSmallIntegerField(editable=False, null=False, default=0)

    # Model managers
    objects = models.Manager()

    class Meta:  # type: ignore
        verbose_name = _("jury scorecard")
        verbose_name_plural = _("jury scorecards")

    def __str__(self) -> str:
        return _("(Project {project_id} Stage {edition_stage_id}) Scorecard {id}").format(
            project_id=self.project.pk if self.project else 0,
            edition_stage_id=self.edition_stage.pk if self.edition_stage else 0,
            id=self.pk,
        )


class ProjectData(EditionStageRelatedModel, ProjectRelatedModel, CommonTimeStampModel):
    data = models.JSONField(verbose_name="data", null=True, blank=True)

    # Model managers
    objects = models.Manager()

    class Meta:  # type: ignore
        verbose_name = _("project data")
        verbose_name_plural = _("project data")

    def __str__(self) -> str:
        return _("(Project {project_id}) Data {id}").format(
            project_id=self.project.pk if self.project else 0, id=self.pk
        )


class ProjectDataRelatedModel(models.Model):
    """
    Helper for grouping the project data related classes
    """

    project_data = models.ForeignKey(
        ProjectData, verbose_name="project data", blank=True, null=True, on_delete=models.SET_NULL
    )

    class Meta:
        abstract = True

    @classmethod
    def sweep_items(cls) -> models.QuerySet:
        """
        Gather all project related items for deleted projects
        """

        return cls.objects.filter(project_data__isnull=True).all()


class ProjectDataDocument(ProjectDataRelatedModel, CommonTimeStampModel):
    """
    Uploaded project files
    """

    uploaded_document = models.FileField(
        verbose_name=_("uploaded document"),
        upload_to="projects/%Y/%W/",
        blank=True,
        null=True,
    )
    linked_document_url = models.CharField(
        verbose_name=_("linked document URL"),
        max_length=2048,
        blank=True,
        null=False,
        default="",
        help_text=_("If the user entered a link instead of a file upload"),
    )

    # Model managers
    objects = models.Manager()

    class Meta:  # type: ignore
        verbose_name = _("project data document")
        verbose_name_plural = _("project data documents")

    def __str__(self) -> str:
        return _("(Project Data {project_data_id}) Document {id}").format(
            project_id=self.project_data.pk if self.project_data else 0, id=self.pk
        )
