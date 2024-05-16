from address.models import AddressField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from organizations.models import (
    AbstractOrganization,
    AbstractOrganizationOwner,
    AbstractOrganizationUser,
)

from rotary_lights_website.users.models import User


class VolunteerOrganization(AbstractOrganization):
    # Basic Properties
    created = models.DateTimeField(auto_now_add=True)
    address = AddressField(on_delete=models.CASCADE)

    class Meta(AbstractOrganization.Meta):
        verbose_name = _("Volunteer Organization")
        verbose_name_plural = _("Volunteer Organizations")


class VolunteerMember(AbstractOrganizationUser):
    # Relation Properties
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    organization = models.ForeignKey(
        VolunteerOrganization,
        on_delete=models.CASCADE,
        related_name="members",
    )

    # Basic Properties
    joined = models.DateTimeField(auto_now_add=True)

    class Meta(AbstractOrganizationUser.Meta):
        unique_together = ("user", "organization")
        verbose_name = _("Volunteer Member")
        verbose_name_plural = _("Volunteer Members")


class VolunteerOwner(AbstractOrganizationOwner):
    # Relation Properties
    organization = models.OneToOneField(
        VolunteerOrganization,
        on_delete=models.CASCADE,
        related_name="owner",
    )
    organization_user = models.OneToOneField(
        VolunteerMember,
        on_delete=models.CASCADE,
        related_name="+",
    )

    # Basic Properties
    joined = models.DateTimeField(auto_now_add=True)
    owner_since = models.DateTimeField(default=timezone.now)

    class Meta(AbstractOrganizationOwner.Meta):
        verbose_name = _("Volunteer Owner")
        verbose_name_plural = _("Volunteer Owners")
