import uuid

from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager as AbstractBaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _

from tech_three.utils.validators import PHONE_REGEX, NAME_REGEX


class Mode(models.TextChoices):
    ACTIVE = "A", "Active"
    DEACTIVATED = "D", "Deactivated"
    TRASHED = "T", "Trashed"


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(
        'account.User', verbose_name=_('Created by'), on_delete=models.SET_NULL, editable=False,
        related_name="created_%(app_label)s_%(class)s_set", null=True, help_text=_('Data created by')
    )
    modified_by = models.ForeignKey(
        'account.User', verbose_name=_('Modified by'), on_delete=models.SET_NULL, editable=False,
        related_name="modified_%(app_label)s_%(class)s_set", null=True, help_text=_('Data modified by')
    )
    created_on = models.DateTimeField(verbose_name=_('Created on'), auto_now_add=True, help_text=_('Data created on'))
    modified_on = models.DateTimeField(verbose_name=_('Modified by'), auto_now=True, help_text=_('Data modified on'))
    mode = models.CharField(verbose_name=_('Mode'), max_length=1, default=Mode.ACTIVE, choices=Mode.choices)

    class Meta:
        abstract = True


class Role(BaseModel):
    name = models.CharField(verbose_name=_('Name'), max_length=50, unique=True, help_text=_('User role name'))
    description = models.TextField(verbose_name=_('Description'), blank=True, help_text=_('User role description'))

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'role'
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        ordering = ('name',)


class UserManager(AbstractBaseUserManager):
    def create_superuser(self, phone, password=None):
        """
        Creates and saves a superuser with the given phone and password.
        """
        if not phone:
            raise ValueError(_('Users must have a phone number'))

        if not password:
            raise ValueError(_('Users must input password'))

        user = self.model(phone=phone)
        user.set_password(password)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.role = Role.objects.get(name="Owner")
        user.save(using=self._db)
        return user


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(verbose_name=_('Phone'), help_text=_('Phone Number'), unique=True,
                             validators=[PHONE_REGEX], max_length=15)  # validators should be a list
    first_name = models.CharField(verbose_name=_('First Name'), max_length=255, help_text=_('First name'),
                                  validators=[NAME_REGEX])
    last_name = models.CharField(verbose_name=_('Last Name'), max_length=255, blank=True, help_text=_('Last name'),
                                 validators=[NAME_REGEX])
    is_staff = models.BooleanField(verbose_name=_('Is staff user?'), default=False)
    role = models.ForeignKey(Role, verbose_name=_('Role'), related_name='users', null=True, on_delete=models.SET_NULL,
                             help_text=_('Role'))
    address_line1 = models.CharField(verbose_name=_('Address Line 1'), max_length=255, blank=True,
                                     help_text=_('Address line 1'))
    address_line2 = models.CharField(verbose_name=_('Address Line 2'), max_length=255, blank=True,
                                     help_text=_('Address line 2'))
    city = models.CharField(verbose_name=_('City'), max_length=100, blank=True, help_text=_('City'))
    state = models.ForeignKey('account.State', verbose_name=_('State/Province/County'), related_name='users',
                              null=True, on_delete=models.DO_NOTHING, help_text=_('State'))
    country = models.ForeignKey('account.Country', verbose_name=_('Country'), related_name='users', null=True,
                                on_delete=models.DO_NOTHING, help_text=_('Country'))
    postal_code = models.CharField(verbose_name=_('Postal Code'), max_length=20, blank=True, help_text=_('postal code'))

    USERNAME_FIELD = 'phone'
    objects = UserManager()

    def __str__(self):
        return f'{str(self.phone)} - {self.role}'

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

    class Meta:
        db_table = 'user'
        verbose_name = _('Users')
        verbose_name_plural = _('Users')


class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name=_('Name'), max_length=100, unique=True, help_text=_('Country name'))
    iso = models.CharField(max_length=2, unique=True,
                           help_text=_('2 letter country code (Example: IN for India)'))
    iso3 = models.CharField(max_length=3, unique=True,
                            help_text=_('3 letter country code (Example: IND for India)'))
    calling_code = models.CharField(verbose_name=_('Calling code'), max_length=10,
                                    help_text=_('Telephone calling code (Example: +91 for India)'))

    def save(self, **kwargs):
        if not self.id:
            self.name = self.name.title()
        super(Country, self).save()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'country'
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        ordering = ('name',)


class State(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='states', help_text=_('Country'))
    name = models.CharField(verbose_name=_('Name'), max_length=100, help_text=_('State name'))
    abbreviation = models.CharField(verbose_name=_('Abbreviation'), max_length=30, blank=True,
                                    help_text=_('State abbreviation'))

    def save(self, **kwargs):
        if not self.id:
            self.name = self.name.title()
        super(State, self).save()

    def __str__(self):
        return self.name.title()

    class Meta:
        db_table = 'state'
        unique_together = ('country', 'name')
        verbose_name = _('State')
        verbose_name_plural = _('States')
        ordering = ('name',)
