from django.core.exceptions import ValidationError
from django.db import models
from django.utils.deconstruct import deconstructible
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


@deconstructible
class MaxFileSizeValidator:
    """
    Validator which checks that file size is less or equal to the specified size limit
    """

    def __init__(self, max_size=1024):
        self.max_size = max_size

    def __call__(self, value):
        if not value and not hasattr(value, "size"):
            return
        if value.size > self.max_size:
            raise ValidationError(_("The file is too large."))
