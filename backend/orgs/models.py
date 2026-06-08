from django.db import models

from utils.models import CommonTimeStampModel
from users.models import User


class Organization(CommonTimeStampModel):
    """
    Organization metadata and configuration
    """

    users = models.ManyToManyField(User)


class OrganizationRelatedModel(models.Model):
    """
    Helper for grouping the organization related classes
    """

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class OrganizationData(OrganizationRelatedModel):
    """
    Information about an organization
    """

    pass


class OrganizationDataSnapshot(OrganizationData):
    """
    Preferably read-only, historical copy of an organization's data
    """

    pass


class OrganizationDocument(OrganizationData):
    """
    Uploaded organization files
    """

    pass

