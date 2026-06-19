from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import CommonTimeStampModel
from users.models import User


class Organization(CommonTimeStampModel):
    """
    Organization metadata and configuration
    """

    users = models.ManyToManyField(User)

    class Meta:  # type: ignore
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")


class OrganizationRelatedModel(models.Model):
    """
    Helper for grouping the organization related classes
    """

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class OrganizationDetails(OrganizationRelatedModel, CommonTimeStampModel):
    """
    Information about an organization
    """

    data = models.JSONField(default=dict, blank=True, null=False)

    class Meta:  # type: ignore
        verbose_name = _("organization details")
        verbose_name_plural = _("organization details")


class OrganizationDetailsSnapshot(OrganizationDetails):
    """
    Preferably read-only, historical copy of an organization's details
    """

    class Meta:  # type: ignore
        verbose_name = _("organization details snapshot")
        verbose_name_plural = _("organization details snapshots")


class OrganizationDocument(OrganizationRelatedModel):
    """
    Uploaded organization files
    """

    uploaded_document = models.FileField(
        verbose_name=_("uploaded document"),
        upload_to="orgs/%Y/%m/",
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
    referencing_snapshots = models.ManyToManyField(
        OrganizationDetailsSnapshot, verbose_name="referencing snapshots", blank=True, null=True
    )

    class Meta:  # type: ignore
        verbose_name = _("organization document")
        verbose_name_plural = _("organization documents")

    @staticmethod
    def sweep_items() -> models.QuerySet:
        return OrganizationDocument.objects.filter(organization__isnull=True, referencing_snapshots__set=None).all()


