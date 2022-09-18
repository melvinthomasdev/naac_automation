from django.contrib.auth.models import AbstractUser, BaseUserManager  # A new class is imported. ##
from django.db import models
from django.utils.translation import gettext_lazy as _

from baseapp.models import TimestampedUUIDModel, UUIDModel


YEAR_OF_STUDY_CHOICES = (
    ("1", "1st Year"),
    ("2", "2nd Year"),
    ("3", "3rd Year"),
    ("4", "4th Year"),
)


class Institution(UUIDModel):
    name = models.CharField(max_length=200)
    address_line_1 = models.CharField(max_length=70)
    address_line_2 = models.CharField(max_length=70)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=70)
    pincode = models.IntegerField()
    phone_number = models.CharField(max_length=13,
                                    help_text=_("Phone number that can be used to contact the institution"))
    website = models.URLField()
    is_verified = models.BooleanField(default=False,
                                      help_text=_("Institutions need to be verified before they can use the portal"))

    def __str__(self):
        return f"{self.name}-({self.id})"

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, TimestampedUUIDModel):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)

    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    designation = models.CharField(max_length=50, blank=True, null=True)
    department = models.CharField(max_length=70, blank=True, null=True)
    # institution = models.ForeignKey(to=Institution, on_delete=models.CASCADE, blank=True, null=True)
    institution = models.CharField(max_length=300, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.email}-({self.id})"


class Criterion(UUIDModel):
    number = models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Criteria"

    def __str__(self):
        return f"{self.number}-{self.name}-({self.id})"


class Indicator(UUIDModel):
    criterion = models.ForeignKey(to=Criterion, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.criterion.name}-{self.name}-({self.id})"


class Document(TimestampedUUIDModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    indicator = models.ForeignKey(to=Indicator, on_delete=models.CASCADE)
    content = models.TextField(blank=False, null=False)

    def __str__(self):
        return f"{self.user.email}-{self.indicator.name}"

