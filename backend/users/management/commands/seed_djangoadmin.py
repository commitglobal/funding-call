import logging

from django.conf import settings

from ._private.seed_user import CommonCreateUserCommand

logger = logging.getLogger(__name__)


class Command(CommonCreateUserCommand):
    help = "Command to create a Django superadmin"

    def handle(self, *args, **kwargs):
        self._create_user(
            admin_email=settings.DJANGO_ADMIN_EMAIL,
            password=settings.DJANGO_ADMIN_PASSWORD,
            is_superuser=True,
            is_staff=True,
            first_name=kwargs.get("first_name", "Django"),
            last_name=kwargs.get("last_name", "Admin"),
        )
        logger.info("Django superadmin created successfully")

        return 0
