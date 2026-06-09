from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from users.models import User
from utils.models import CommonTimeStampModel
from utils.translation import TranslateableTextField


class Edition(CommonTimeStampModel):
    """
    Data about an edition
    """

    title = TranslateableTextField(verbose_name="Title")
    description = TranslateableTextField(verbose_name="Description")
    jury_users = models.ManyToManyField(User)

    class Meta:  # type: ignore
        verbose_name = _("edition")
        verbose_name_plural = _("editions")

    def __str__(self) -> str:
        return _("Edition {id}: {title}").format(id=self.pk, title=self.title)


class EditionRelatedModel(models.Model):
    """
    Helper for grouping the edition related classes
    """

    edition = models.ForeignKey(Edition, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True

    @classmethod
    def sweep_items(cls) -> QuerySet:
        """
        Gather all edition related items for deleted editions
        """

        return cls.objects.filter(edition__isnull=True).all()


class FinancingDomain(EditionRelatedModel, CommonTimeStampModel):
    title = TranslateableTextField(verbose_name="Title")

    class Meta:  # type: ignore
        ordering = ("name",)
        verbose_name = _("financing domain")
        verbose_name_plural = _("financing domains")

    def __str__(self) -> str:
        return _("Financing Domain {id}: {title}").format(id=self.pk, title=self.title)


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
        return _("Edition Stage {id}: {title}").format(id=self.pk, title=self.title)


class EditionStageRelatedModel(models.Model):
    """
    Helper for grouping the edition stage related classes
    """

    edition_stage = models.ForeignKey(EditionStage, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True

    @classmethod
    def sweep_items(cls) -> QuerySet:
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
        return _("Project {id}: {title}").format(id=self.pk, title=self.title)
    

class ProjectRelatedModel(models.Model):
    """
    Helper for grouping the project related classes
    """

    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True

    @classmethod
    def sweep_items(cls) -> QuerySet:
        """
        Gather all project related items for deleted projects
        """

        return cls.objects.filter(project__isnull=True).all()


class ProjectDocument(ProjectRelatedModel, CommonTimeStampModel):
    """
    Uploaded project files
    """

    class Meta:  # type: ignore
        verbose_name = _("project document")
        verbose_name_plural = _("project documents")


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
        return _("Project Comment {id}: {title}").format(id=self.pk, title=self.title)


class ProjectJury(EditionStageRelatedModel, ProjectRelatedModel, CommonTimeStampModel):
    """
    Project jury assignment for an edition stage
    """
    
    jury_users = models.ManyToManyField(User)
    
    class Meta:  # type: ignore
        verbose_name = _("project jury")
        verbose_name_plural = _("project juries")

    @classmethod
    def sweep_items(cls) -> QuerySet:
        """
        Gather all items for deleted edition stages or deleted projects
        """

        return cls.objects.filter(edition__isnull=True).all() | cls.objects.filter(project__isnull=True).all()
    
    def __str__(self) -> str:
        return _("Project {project_id} Stage {edition_stage_id} Jury").format(
            project_id=self.project.pk if self.project else 0,
            edition_stage_id=self.edition_stage.pk if self.edition_stage else 0,
        )


class JuryScorecard(ProjectRelatedModel, CommonTimeStampModel):
    """
    One jury user's score card for a project
    """

    jury_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:  # type: ignore
        verbose_name = _("jury scorecard")
        verbose_name_plural = _("jury scorecards")

    def __str__(self) -> str:
        return _("Jury Scorecard {id}").format(id=self.pk)