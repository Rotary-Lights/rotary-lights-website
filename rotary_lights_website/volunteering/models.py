from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.models import ClusterableModel
from organizations.models import Organization
from organizations.models import OrganizationOwner
from organizations.models import OrganizationUser


class VolunteerOrganization(Organization):
    class Meta:
        verbose_name = _("Volunteer Organization")
        verbose_name_plural = _("Volunteer Organizations")


class VolunteerOrganizationUser(OrganizationUser):
    class Meta:
        verbose_name = _("Volunteer Organization User")
        verbose_name_plural = _("Volunteer Organization Users")


class VolunteerOrganizationOwner(OrganizationOwner):
    class Meta:
        verbose_name = _("Volunteer Organization Owner")
        verbose_name_plural = _("Volunteer Organization Owners")


class Activity(ClusterableModel):
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True)

    class Meta:
        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")

    def __str__(self):
        return self.name


class Shift(ClusterableModel):
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name="shifts",
        null=True,
    )
    organizations = models.ManyToManyField(VolunteerOrganization, related_name="shifts", blank=True)
    start_time = models.DateTimeField(_("Start Date & Time"))
    end_time = models.DateTimeField(_("End Date & Time"))
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True)

    class Meta:
        verbose_name = _("Shift")
        verbose_name_plural = _("Shifts")
        ordering = ["start_time", "end_time", "name"]

    def __str__(self) -> str:
        return f"{self.name} from {self.start_time} to {self.end_time}"
