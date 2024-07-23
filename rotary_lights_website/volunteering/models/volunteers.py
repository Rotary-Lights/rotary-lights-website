from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.models import ClusterableModel, ParentalKey
from phonenumber_field.modelfields import PhoneNumberField

from rotary_lights_website.users.models import User
from rotary_lights_website.volunteering.models.organizations import Organization


class Volunteer(ClusterableModel):
    # For use with MultipleChooserPanel.
    volunteer_pk = models.ForeignKey(
        "Volunteer",
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
    )

    # Basic Properties
    organization = ParentalKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="members",
        null=True,
        blank=True,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")

    # Contact Properties
    address = models.CharField(_("Mailing Address"), max_length=150)
    primary_phone_number = PhoneNumberField(_("Primary Phone Number"))
    secondary_phone_number = PhoneNumberField(_("Secondary Phone Number"), blank=True)

    class Meta(ClusterableModel.Meta):
        verbose_name = _("Volunteer")
        verbose_name_plural = _("Volunteers")

    def __str__(self) -> str:
        name = f"{self.user.first_name} {self.user.last_name}"
        return name.strip() or str(self.user.username)
