from django.db.models import JSONField


class FieldsetField(JSONField):
    # TODO: store an entire form definition `{'tabs': [{'title': '', 'fields': []}]}`
    pass
