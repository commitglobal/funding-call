from hashlib import blake2b

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import CommonTimeStampModel
from users.models import User


def build_organization_document_storage_path(document, filename) -> str:
    return "{0}/organization/{1}".format(document.get_base_directory_path(), filename[-100:])


class Organization(CommonTimeStampModel):
    """
    Organization metadata and configuration
    """

    users = models.ManyToManyField(User)

    class Meta:  # type: ignore
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")

    def get_base_directory(self, public=False) -> str:
        """
        Build the base directory name for file storage
        """

        organization_hash: str = blake2b(
            f"ORGANIZATION PK={self.pk} KH={settings.SECRET_KEY_HASH}".encode(), 
            digest_size=4, 
            usedforsecurity=False
        ).hexdigest().lower()

        return f"organization-{self.pk}-{organization_hash}" + ("-public" if public else "")


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


class OrganizationDocument(OrganizationDetails):
    """
    Uploaded organization files
    """

    uploaded_document = models.FileField(
        verbose_name=_("uploaded document"),
        upload_to=build_organization_document_storage_path,
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
        verbose_name = _("organization document")
        verbose_name_plural = _("organization documents")


