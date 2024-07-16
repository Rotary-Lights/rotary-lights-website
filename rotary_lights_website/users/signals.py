from typing import Type

from allauth.account.signals import email_confirmed
from django.contrib.auth.models import Group
from django.dispatch import receiver

from rotary_lights_website.users.models import User


@receiver(email_confirmed, dispatch_uid="set_default_user_roles")
def set_default_user_roles(sender: Type[User], **kwargs) -> None:
    email_address = kwargs["email_address"]
    user = User.objects.get(email=email_address)
    user_group = Group.objects.get(name="Users")
    if not user.is_staff:
        user.groups.add(user_group)
    user.save()
