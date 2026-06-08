from django.db import models

from users.models import User
from utils.translation import TranslateableTextField


class Edition(models.Model):
    """
    Data about an edition
    """

    title = TranslateableTextField(verbose_name="Title")
    jury_users = models.ManyToManyField(User)


class EditionRelatedModel(models.Model):
    """
    Helper for grouping the edition related classes
    """

    edition = models.ForeignKey(Edition, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True


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

    pass


class Project(EditionRelatedModel):
    """
    Project metadata and configuration
    """

    pass


class ProjectRelatedModel(models.Model):
    """
    Helper for grouping the project related classes
    """

    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class ProjectDocument(ProjectRelatedModel):
    """
    Uploaded project files
    """

    pass


class ProjectComment(ProjectRelatedModel):
    """
    User comment about a project
    """
    
    pass


class JuryScorecard(ProjectRelatedModel):
    """
    One jury user's score card for a project
    """

    jury_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    pass

