from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


# class DBRouter:
#     """
#     A router to control all database operations on models in the
#     user application.
#     """
#     def db_for_read(self, model, **hints):
#         """
#         Attempts to read icps models go to icps_db.
#         """
#         if model._meta.app_label == 'icps_data':
#             return 'icps_db'
#         elif model._meta.app_label == 'octagon_data':
#             return 'octagon_db'
#         return None
#
#     def db_for_write(self, model, **hints):
#         """
#         Attempts to write user models go to users_db.
#         """
#         if model._meta.app_label == 'icps_data':
#             return 'icps_db'
#         elif model._meta.app_label == 'octagon_data':
#             return 'octagon_db'
#         return None
#
#     def allow_relation(self, obj1, obj2, **hints):
#         """
#         Allow relations if a model in the icps app is involved.
#         """
#         if obj1._meta.app_label == 'icps_data' or \
#            obj2._meta.app_label == 'octagon_data':
#            return True
#         return None
#
#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         """
#         Make sure the auth app only appears in the 'icps_db'
#         database.
#         """
#         if app_label == 'icps_data':
#             return db == 'icps_db'
#         return None


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


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    is_head = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Employee(models.Model):
    first_name = models.CharField(max_length=60, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    user_policy = models.CharField(max_length=80)
    employee_id = models.IntegerField(blank=True, null=True)
    department = models.CharField(max_length=80)
    comment = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    timein = models.CharField(max_length=80, blank=True, null=True)
    timeout = models.CharField(max_length=80, blank=True, null=True)
    regular = models.CharField(max_length=20, blank=True, null=True)
    av_timein = models.CharField(max_length=80, blank=True, null=True)
    av_timeout = models.CharField(max_length=80, blank=True, null=True)
    ot = models.CharField(max_length=20, blank=True, null=True)
    total = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Access(models.Model):
    created_at = models.DateTimeField()
    date = models.DateField(blank=True, null=True)
    first_name = models.CharField(max_length=60, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    user_policy = models.CharField(max_length=80, null=True)
    employee_id = models.IntegerField(blank=True, null=True)
    morpho_device = models.CharField(max_length=80)
    key = models.CharField(max_length=50)
    access = models.CharField(max_length=50)
    department = models.CharField(max_length=80, blank=True, null=True)
    comment = models.CharField(max_length=100, blank=True, null=True)
    timein = models.CharField(max_length=80, blank=True, null=True)
    timeout = models.CharField(max_length=80, blank=True, null=True)
    av_timein = models.CharField(max_length=80, blank=True, null=True)
    av_timeout = models.CharField(max_length=80, blank=True, null=True)
    regular = models.CharField(max_length=20, blank=True, null=True)
    ot = models.CharField(max_length=20, blank=True, null=True)
    total = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class ICPSEmployee(models.Model):
    name = models.CharField(max_length=80, unique=True, blank=True, null=True)
    user_policy = models.CharField(max_length=80)
    employee_id = models.IntegerField(blank=True, null=True)
    department = models.CharField(max_length=80)
    comment = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    timein = models.CharField(max_length=80, blank=True, null=True)
    timeout = models.CharField(max_length=80, blank=True, null=True)
    av_timein = models.CharField(max_length=80, blank=True, null=True)
    av_timeout = models.CharField(max_length=80, blank=True, null=True)
    regular = models.CharField(max_length=20, blank=True, null=True)
    ot = models.CharField(max_length=20, blank=True, null=True)
    total = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name


class ICPSAccess(models.Model):
    created_at = models.DateTimeField()
    date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=80, blank=True, null=True)
    user_policy = models.CharField(max_length=80, null=True, blank=True)
    employee_id = models.IntegerField(blank=True, null=True)
    morpho_device = models.CharField(max_length=80)
    key = models.CharField(max_length=50)
    access = models.CharField(max_length=50)
    department = models.CharField(max_length=80, blank=True, null=True)
    comment = models.CharField(max_length=100, blank=True, null=True)
    timein = models.CharField(max_length=80, blank=True, null=True)
    timeout = models.CharField(max_length=80, blank=True, null=True)
    regular = models.CharField(max_length=20, blank=True, null=True)
    ot = models.CharField(max_length=20, blank=True, null=True)
    total = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name


class ICPSAccessUniqueAttendance(models.Model):
    # created_at = models.DateTimeField()
    date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=80, blank=True, null=True)
    employee_id = models.IntegerField(blank=True, null=True)
    comment = models.CharField(max_length=100, blank=True, null=True)
    timein = models.TimeField(null=True, blank=True)
    timeout = models.TimeField(null=True, blank=True)
    av_timein = models.TimeField(null=True, blank=True)
    av_timeout = models.TimeField(null=True, blank=True)
    regular = models.TimeField(null=True, blank=True)
    ot = models.TimeField(null=True, blank=True)
    w_hours = models.TimeField(null=True, blank=True)
    avg_hours = models.TimeField(null=True, blank=True)
    def __str__(self):
        return self.name
