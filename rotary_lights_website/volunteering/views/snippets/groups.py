from django.utils.translation import gettext_lazy as _
from wagtail.snippets.views.snippets import SnippetViewSetGroup

from rotary_lights_website.volunteering.views.snippets.activities import ActivityViewSet
from rotary_lights_website.volunteering.views.snippets.events import EventViewSet
from rotary_lights_website.volunteering.views.snippets.organizations import (
    OrganizationViewSet,
)
from rotary_lights_website.volunteering.views.snippets.shifts import ShiftViewSet
from rotary_lights_website.volunteering.views.snippets.volunteers import (
    VolunteerViewSet,
)

# ViewSetGroups
# ----------------------------------------------------------------------


class VolunteeringViewSetGroup(SnippetViewSetGroup):
    items = [
        OrganizationViewSet,
        VolunteerViewSet,
        EventViewSet,
        ActivityViewSet,
        ShiftViewSet,
    ]

    icon = "group"
    menu_icon = "group"
    menu_label = _("Volunteering")
    menu_name = "volunteering"
