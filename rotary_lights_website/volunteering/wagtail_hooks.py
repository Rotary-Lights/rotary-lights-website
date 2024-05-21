from wagtail import hooks
from wagtail.snippets.models import register_snippet

from rotary_lights_website.volunteering.views.snippets.events import (
    EventChooserViewSet,
    event_chooserviewset,
)
from rotary_lights_website.volunteering.views.snippets.groups import (
    VolunteeringViewSetGroup,
)
from rotary_lights_website.volunteering.views.snippets.shifts import (
    ShiftChooserViewSet,
    shift_chooserviewset,
)
from rotary_lights_website.volunteering.views.snippets.volunteers import (
    VolunteerChooserViewSet,
    volunteer_chooserviewset,
)


@hooks.register("register_admin_viewset")
def register_events_chooserviewset() -> EventChooserViewSet:
    return event_chooserviewset


@hooks.register("register_admin_viewset")
def register_volunteers_chooserviewset() -> VolunteerChooserViewSet:
    return volunteer_chooserviewset


@hooks.register("register_admin_viewset")
def register_shifts_chooserviewset() -> ShiftChooserViewSet:
    return shift_chooserviewset


register_snippet(VolunteeringViewSetGroup)
