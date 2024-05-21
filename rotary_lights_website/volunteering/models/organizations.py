from typing import TYPE_CHECKING

from address.models import AddressField
from django.db import models
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from modelcluster.models import ClusterableModel, ParentalKey
from phonenumber_field.modelfields import PhoneNumberField

from rotary_lights_website.volunteering.models.shifts import Shift

if TYPE_CHECKING:
    from rotary_lights_website.volunteering.models.volunteers import Volunteer


class OrganizationShiftRelation(ClusterableModel):
    organization = ParentalKey(
        "Organization",
        on_delete=models.CASCADE,
        related_name="shifts",
    )
    shift = models.ForeignKey(
        Shift,
        on_delete=models.CASCADE,
        related_name="organizations",
    )

    class Meta(ClusterableModel.Meta):
        unique_together = ("organization", "shift")

    def __str__(self) -> str:
        return "Not working"


class OrganizationOwnersRelation(ClusterableModel):
    organization = ParentalKey(
        "Organization",
        on_delete=models.CASCADE,
        related_name="owners",
    )
    owner = ParentalKey(
        "Volunteer",
        on_delete=models.CASCADE,
        related_name="owned_organizations",
    )

    class Meta(ClusterableModel.Meta):
        unique_together = ("organization", "owner")


class Organization(ClusterableModel):
    # Basic Properties
    name = models.CharField(_("Name"), max_length=128)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    is_quarantined = models.BooleanField(_("Is Quarantined"), default=False)
    scheduled_deletion_date = models.DateTimeField(
        _("Scheduled Deletion Date"),
        null=True,
        blank=True,
    )

    owners: Manager["Volunteer"]
    if TYPE_CHECKING:
        owners: QuerySet["Volunteer"]

    members: Manager["Volunteer"]
    if TYPE_CHECKING:
        members: QuerySet["Volunteer"]

    # Contact Properties
    address = AddressField(verbose_name=_("Mailing Address"))
    primary_phone_number = PhoneNumberField(_("Primary Organization Phone Number"))
    secondary_phone_number = PhoneNumberField(
        _("Secondary Organization Phone Number"),
        blank=True,
    )

    # Volunteering Properties
    shifts: Manager["Shift"]
    if TYPE_CHECKING:
        shifts: QuerySet["Shift"]

    class Meta(ClusterableModel.Meta):
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")

    def __str__(self) -> str:
        return str(self.name)
