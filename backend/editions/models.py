from django.db import models

from utils.translation import TranslateableTextField


class Edition(models.Model):
    title = TranslateableTextField(verbose_name="Title")


class EditionRelatedModel(models.Model):
    edition = models.ForeignKey(Edition, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class JuryMember(EditionRelatedModel):
    pass


class EditionStage(EditionRelatedModel):
    pass


class Project(EditionRelatedModel):
    pass


class ProjectRelatedModel(models.Model):
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class ProjectDocument(ProjectRelatedModel):
    pass


class ProjectComment(ProjectRelatedModel):
    pass


class JuryScoring(ProjectRelatedModel):
    jury_member = models.ForeignKey(JuryMember, blank=True, null=True, on_delete=models.SET_NULL)

    pass

