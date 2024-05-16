from wagtail.snippets.models import register_snippet

from rotary_lights_website.volunteering.views.snippets.groups import (
    VolunteeringViewSetGroup,
)

register_snippet(VolunteeringViewSetGroup)
