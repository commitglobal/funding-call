from django.db.models import JSONField


class TranslateableTextField(JSONField):
    # TODO: store data like `[{'lang': '', 'text': ''}]`
    pass
