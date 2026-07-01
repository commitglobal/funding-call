from django.conf import settings
from django.core.files.storage import storages


def select_public_storage():
    return storages["public"]
