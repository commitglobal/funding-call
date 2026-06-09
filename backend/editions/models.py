from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from users.models import User
from utils.translation import TranslateableTextField


class Edition(models.Model):
    """
    Data about an edition
    """

    title = TranslateableTextField(verbose_name="Title")
    description = TranslateableTextField(verbose_name="Description")
    jury_users = models.ManyToManyField(User)

    class Meta:
        verbose_name = _("edition")
        verbose_name_plural = _("editions")


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


class FinancingDomain(EditionRelatedModel):
    title = TranslateableTextField(verbose_name="Title")

    class Meta:  # type: ignore
        ordering = ("name",)
        verbose_name = _("financing domain")
        verbose_name_plural = _("financing domains")

    def __str__(self):
        if self.edition:
            return f"{self.edition.title}: {self.title}"
        else:
            return f"{self.title}"


class EditionStage(EditionRelatedModel):
    """
    Data about an edition stage 
    """

    title = TranslateableTextField(verbose_name="Title")
    description = TranslateableTextField(verbose_name="Description")
    requires_jury = models.BooleanField(default=False)    
    requires_form = models.BooleanField(default=False)
    begins_on = models.DateTimeField()
    ends_on= models.DateTimeField()

    class Meta:  # type: ignore
        verbose_name = _("edition stage")
        verbose_name_plural = _("edition stages")


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



class Project(EditionRelatedModel):
    """
    Project metadata and configuration
    """

    class Meta:  # type: ignore
        verbose_name = _("project")
        verbose_name_plural = _("projects")


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


class ProjectDocument(ProjectRelatedModel):
    """
    Uploaded project files
    """

    class Meta:  # type: ignore
        verbose_name = _("project document")
        verbose_name_plural = _("project documents")


class ProjectComment(ProjectRelatedModel):
    """
    User comment about a project
    """
    
    title = TranslateableTextField(verbose_name="Title")
    message = TranslateableTextField(verbose_name="Message")
    parent_comment = models.ForeignKey("ProjectComment", on_delete=models.CASCADE)

    class Meta:  # type: ignore
        verbose_name = _("project comment")
        verbose_name_plural = _("project comments")



class ProjectJury(EditionStageRelatedModel, ProjectRelatedModel):
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


class JuryScorecard(ProjectRelatedModel):
    """
    One jury user's score card for a project
    """

    jury_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:  # type: ignore
        verbose_name = _("jury scorecard")
        verbose_name_plural = _("jury scorecards")
