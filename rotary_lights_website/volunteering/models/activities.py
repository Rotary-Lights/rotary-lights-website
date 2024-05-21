from typing import TYPE_CHECKING

from django.db import models
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from modelcluster.models import ClusterableModel, ParentalKey

from rotary_lights_website.volunteering.models.events import Event

if TYPE_CHECKING:
    from rotary_lights_website.volunteering.models.shifts import Shift


class Activity(ClusterableModel):
    # Basic Properties
    name = models.CharField(_("Name"), max_length=128)
    description = models.TextField(_("Description"))
    event = ParentalKey(Event, on_delete=models.CASCADE, related_name="activities")

    shifts: Manager["Shift"]
    if TYPE_CHECKING:
        shifts: QuerySet["Shift"]

    class Meta(ClusterableModel.Meta):
        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")

    def __str__(self) -> str:
        return f"{self.event.name} - {self.name}"
