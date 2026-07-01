from django.db import models
from django.utils.translation import gettext_lazy as _


class CommonTimeStampModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        help_text=_("Timestamp of the creation of the object"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("updated at"),
        help_text=_("Timestamp of the last update of the object"),
        auto_now=True,
    )

    class Meta:
        abstract = True
