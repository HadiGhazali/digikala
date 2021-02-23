from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager as BaseUserManager
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.db import models


# Create your models here.
class UserManger(BaseUserManager):
    def _create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        username = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(_('Phone number'), max_length=40, unique=True)
    first_name = models.CharField(_('First name'), max_length=150, null=True, blank=True)
    last_name = models.CharField(_('Last name'), max_length=150, null=True, blank=True)
    image = models.ImageField(_("image"), upload_to='account/user/images', null=True, blank=True)
    create_at = models.DateTimeField(_('Create at'), auto_now_add=True)
    update_at = models.DateTimeField(_('Update at'), auto_now=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    EMAIL_FIELD = 'username'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('phone_number', )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = UserManger()

    def clean(self):
        super().clean()
        self.username = self.__class__.objects.normalize_email(self.username)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.username], **kwargs)


class Email(models.Model):
    to = models.ForeignKey(User, verbose_name=_('to'), on_delete=models.SET_NULL, null=True)
    subject = models.CharField(_('Subject'), max_length=150)
    body = models.TextField(_('Body'))
    create_at = models.DateTimeField(_('Create at'), auto_now_add=True)
    update_at = models.DateTimeField(_('Update at'), auto_now=True)

    class Meta:
        verbose_name = _('Email')
        verbose_name_plural = _('Emails')


class Address(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE, related_name='user_address',
                             related_query_name='user_address')
    city = models.CharField(_('City'), max_length=150)
    street = models.CharField(_('street'), max_length=150)
    zip_code = models.CharField(_('Zip code'), max_length=150)
    allay = models.CharField(_('Allay'), max_length=150)
    create_at = models.DateTimeField(_('Create at'), auto_now_add=True)
    update_at = models.DateTimeField(_('Update at'), auto_now=True)

    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('addresses')

    @property
    def show_address(self):
        return '{} {}'.format(self.city, self.street)


class Shop(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE)
    name = models.CharField(_('name'), max_length=150)
    description = models.TextField(_('Description'), max_length=150)
    image = models.ImageField(_('image'), upload_to='account/shop/images')
    create_at = models.DateTimeField(_('Create at'), auto_now_add=True)
    update_at = models.DateTimeField(_('Update at'), auto_now=True)
    satisfaction = models.PositiveIntegerField(_('satisfaction'), null=True, blank=True, default=3)

    class Meta:
        verbose_name = _('shop')
        verbose_name_plural = _('shops')

    def __str__(self):
        return self.name
