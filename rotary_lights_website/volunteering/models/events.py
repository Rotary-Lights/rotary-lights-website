from typing import TYPE_CHECKING

from django.db import models
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from modelcluster.models import ClusterableModel

if TYPE_CHECKING:
    from rotary_lights_website.volunteering.models.activities import Activity


class Event(ClusterableModel):
    # Basic Properties
    name = models.CharField(_("Name"), max_length=128)
    description = models.TextField(_("Description"))

    activities: Manager["Activity"]
    if TYPE_CHECKING:
        activities: QuerySet["Activity"]

    # Dates and Times
    start_date = models.DateField(_("Start Date"))
    end_date = models.DateField(_("End Date"))
    volunteer_registration_open = models.DateField(_("Volunteer Registration Open"))
    volunteer_registration_close = models.DateField(_("Volunteer Registration Close"))

    class Meta(ClusterableModel.Meta):
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __str__(self) -> str:
        return str(self.name)
