from typing import TYPE_CHECKING

from django.db import models
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from modelcluster.models import ClusterableModel, ParentalKey

from rotary_lights_website.volunteering.models.activities import Activity

if TYPE_CHECKING:
    from rotary_lights_website.volunteering.models.organizations import Organization


class Shift(ClusterableModel):
    # Basic Properties
    activity = ParentalKey(Activity, on_delete=models.CASCADE, related_name="shifts")

    name = models.CharField(_("Name"), max_length=255)
    start_date = models.DateTimeField(_("Start Date"), null=True, blank=True)
    end_date = models.DateTimeField(_("End Date"), null=True, blank=True)

    organizations: Manager["Organization"]
    if TYPE_CHECKING:
        organizations: QuerySet["Organization"]

    class Meta(ClusterableModel.Meta):
        verbose_name = _("Shift")
        verbose_name_plural = _("Shifts")

    def __str__(self) -> str:
        return f"{self.activity.event.name} - {self.activity.name}"
