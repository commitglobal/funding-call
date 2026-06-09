
from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User
from utils.models import CommonTimeStampModel
from utils.storage import select_public_storage
from utils.translation import TranslateableTextField


def build_edition_public_document_storage_path(document, filename) -> str:
    return "{0}/edition_public/{1}".format(document.get_base_directory_path(), filename[-100:])


def build_project_document_storage_path(document, filename) -> str:
    return "{0}/project/{1}".format(document.get_base_directory_path(), filename[-100:])


class Edition(CommonTimeStampModel):
    """
    Data about an edition
    """

    # Description settings
    title = TranslateableTextField(verbose_name="Title")
    description = TranslateableTextField(verbose_name="Description")

    # Jury settings
    jury_users = models.ManyToManyField(User)

    # Visibility settings
    is_published = models.BooleanField(null=False, default=False)
    is_readonly = models.BooleanField(null=False, default=False)

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
    budget_currency = models.CharField(max_length=3, blank=True, null=False)

    # Computed data from related models
    cached_begins_on = models.DateTimeField(editable=False, blank=True, null=True)
    cached_ends_on= models.DateTimeField(editable=False, blank=True, null=True)

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

    edition = models.ForeignKey(Edition, blank=True, null=True, on_delete=models.SET_NULL)

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
        upload_to=build_edition_public_document_storage_path,
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

    class Meta:  # type: ignore
        verbose_name = _("edition public document")
        verbose_name_plural = _("edition public documents")

    def __str__(self) -> str:
        return _("(Edition {edition_id}) Public Document {id}").format(
            edition_id=self.edition.pk if self.edition else 0, id=self.pk)


class FinancingDomain(EditionRelatedModel, CommonTimeStampModel):
    title = TranslateableTextField(verbose_name="Title")

    class Meta:  # type: ignore
        ordering = ("name",)
        verbose_name = _("financing domain")
        verbose_name_plural = _("financing domains")

    def __str__(self) -> str:
        return _("(Edition {edition_id}) Financing Domain {id}: {title}").format(
            edition_id=self.edition.pk if self.edition else 0, id=self.pk, title=self.title)


class EditionStage(EditionRelatedModel, CommonTimeStampModel):
    """
    Data about an edition stage 
    """

    title = TranslateableTextField(verbose_name="Title")
    description = TranslateableTextField(verbose_name="Description")
    begins_on = models.DateTimeField()
    ends_on= models.DateTimeField()
    requires_form = models.BooleanField(default=False)
    requires_jury = models.BooleanField(default=False)    

    class Meta:  # type: ignore
        verbose_name = _("edition stage")
        verbose_name_plural = _("edition stages")

    def __str__(self) -> str:
        return _("(Edition {edition_id}) Stage {id}: {title}").format(
            edition_id=self.edition.pk if self.edition else 0, id=self.pk, title=self.title)


class EditionStageRelatedModel(models.Model):
    """
    Helper for grouping the edition stage related classes
    """

    edition_stage = models.ForeignKey(EditionStage, blank=True, null=True, on_delete=models.SET_NULL)

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

    title = TranslateableTextField(verbose_name="Title")

    class Meta:  # type: ignore
        verbose_name = _("project")
        verbose_name_plural = _("projects")
    
    def __str__(self) -> str:
        return _("(Edition {edition_id}) Project {id}: {title}").format(
            edition_id=self.edition.pk if self.edition else 0, id=self.pk, title=self.title)
    

class ProjectRelatedModel(models.Model):
    """
    Helper for grouping the project related classes
    """

    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True

    @classmethod
    def sweep_items(cls) -> models.QuerySet:
        """
        Gather all project related items for deleted projects
        """

        return cls.objects.filter(project__isnull=True).all()


class ProjectDocument(ProjectRelatedModel, CommonTimeStampModel):
    """
    Uploaded project files
    """

    uploaded_document = models.FileField(
        verbose_name=_("uploaded document"),
        upload_to=build_project_document_storage_path,
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

    class Meta:  # type: ignore
        verbose_name = _("project document")
        verbose_name_plural = _("project documents")

    def __str__(self) -> str:
        return _("(Project {project_id}) Document {id}").format(
            project_id=self.project.pk if self.project else 0, id=self.pk)


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
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL)
    parent_comment = models.ForeignKey("ProjectComment", on_delete=models.CASCADE)
    title = TranslateableTextField(verbose_name="Title")
    message = TranslateableTextField(verbose_name="Message")

    objects = models.Manager()
    top_level = TopLevelCommentManager()

    class Meta:  # type: ignore
        verbose_name = _("project comment")
        verbose_name_plural = _("project comments")
    
    def __str__(self) -> str:
        return _("(Project {project_id}) Comment {id}: {title}").format(
            project_id=self.project.pk if self.project else 0, id=self.pk, title=self.title[:32])


class ProjectJury(EditionStageRelatedModel, ProjectRelatedModel, CommonTimeStampModel):
    """
    Project jury assignment for an edition stage
    """
    
    jury_users = models.ManyToManyField(User)
    
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
            id=self.pk
        )


class JuryScorecard(EditionStageRelatedModel, ProjectRelatedModel, CommonTimeStampModel):
    """
    One jury user's score card for a project
    """

    jury_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:  # type: ignore
        verbose_name = _("jury scorecard")
        verbose_name_plural = _("jury scorecards")

    def __str__(self) -> str:
        return _("(Project {project_id} Stage {edition_stage_id}) Scorecard {id}").format(
            project_id=self.project.pk if self.project else 0,
            edition_stage_id=self.edition_stage.pk if self.edition_stage else 0,
            id=self.pk
        )
