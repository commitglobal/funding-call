from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _

from utils.models import MaxFileSizeValidator
from utils.storage import select_public_storage


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    The default Django user model, but change it to use the email address
    instead of the username
    """

    # We ignore the "username" field because we will use the email for the authentication
    username = models.CharField(
        verbose_name=_("username"),
        max_length=150,
        unique=True,
        help_text=_("We do not use this field"),
        validators=[],
        null=True,
        editable=False,
    )

    email = models.EmailField(verbose_name=_("email address"), blank=False, null=False, unique=True)

    # Type hinting for related models
    profile: "models.manager.RelatedManager[Profile]"

    # Model managers
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        constraints = [
            models.UniqueConstraint(Lower("email"), name="email_unique"),
        ]

    def __str__(self) -> str:
        return _("User {id}: {email}").format(id=self.pk, title=self.email)

    def to_dict(self):
        # TODO
        return {}


class Profile(models.Model):
    """
    Additional user information, not related to the authentication process
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        related_name="profile",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    picture = models.FileField(
        verbose_name=_("picture"),
        upload_to="profiles_public/%Y/%m/",
        storage=select_public_storage,
        blank=True,
        null=True,
        validators=(
            FileExtensionValidator(allowed_extensions=("jpg", "jpeg", "png")),
            MaxFileSizeValidator(settings.MAX_DOCUMENT_SIZE),
        ),
    )

    accepted_newsletter = models.DateTimeField(verbose_name=_("Accepted to receive newsletters"), null=True, blank=True)

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")
        ordering = ["user__email"]

    def __str__(self) -> str:
        return _("(User {user_id}) Profile {id}").format(user_id=self.user.pk, id=self.pk)
