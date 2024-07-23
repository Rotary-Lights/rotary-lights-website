from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from birdsong.models import Contact
from django import forms
from django.contrib.auth import forms as admin_forms
from django.core.exceptions import MultipleObjectsReturned
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField

from rotary_lights_website.users.models import User
from rotary_lights_website.volunteering.models.volunteers import Volunteer


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        error_messages = {
            "username": {"unique": _("This username has already been taken.")},
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """

    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    address = forms.CharField(max_length=256)
    primary_phone_number = PhoneNumberField(region="US")
    secondary_phone_number = PhoneNumberField(region="US")

    def full_clean(self):
        try:
            return super().full_clean()
        except MultipleObjectsReturned as exc:
            if "Address" in str(exc):
                return

    def save(self, request):
        user: User = super().save(request)
        Volunteer.objects.get_or_create(
            user=user,
            address={"raw": request.POST["address"]},
            primary_phone_number=request.POST["primary_phone_number"],
            secondary_phone_number=request.POST["secondary_phone_number"],
        )
        Contact.objects.get_or_create(email=user.email)
        return user


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """
