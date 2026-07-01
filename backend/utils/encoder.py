from django.db.models import QuerySet
from django.db.models.fields.files import FieldFile
from inertia.utils import InertiaJsonEncoder


class CustomJsonEncoder(InertiaJsonEncoder):
    """
    Expand the Inertia's encoder in order to better handle some specific data types
    """

    pass
