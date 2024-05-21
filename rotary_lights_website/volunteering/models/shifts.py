from typing import TYPE_CHECKING

from django.db import models
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from modelcluster.models import ClusterableModel, ParentalKey

from rotary_lights_website.volunteering.models.activities import Activity

if TYPE_CHECKING:
    from rotary_lights_website.volunteering.models.organizations import Organization


class Shift(ClusterableModel):
    # Basic Properties
    activity = ParentalKey(Activity, on_delete=models.CASCADE, related_name="shifts")

    start_date = models.DateTimeField(_("Start Date"))
    end_date = models.DateTimeField(_("End Date"))

    organizations: Manager["Organization"]
    if TYPE_CHECKING:
        organizations: QuerySet["Organization"]

    class Meta(ClusterableModel.Meta):
        verbose_name = _("Shift")
        verbose_name_plural = _("Shifts")

    def __str__(self) -> str:
        start = timezone.localtime(self.start_date).strftime("%b %d, %Y %I:%M %p")
        end = timezone.localtime(self.end_date).strftime("%b %d, %Y %I:%M %p")
        return f"{self.activity.event.name} - {self.activity.name} ({start} - {end})"
