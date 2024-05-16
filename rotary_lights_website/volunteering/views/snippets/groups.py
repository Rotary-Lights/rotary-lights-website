from django.utils.translation import gettext_lazy as _
from wagtail.snippets.views.snippets import SnippetViewSetGroup

from rotary_lights_website.volunteering.views.snippets.members import (
    VolunteerMembersViewSet,
)
from rotary_lights_website.volunteering.views.snippets.organizations import (
    VolunteerOrganizationsViewSet,
)
from rotary_lights_website.volunteering.views.snippets.owners import (
    VolunteerOwnersViewSet,
)


class VolunteeringViewSetGroup(SnippetViewSetGroup):
    items = [
        VolunteerOrganizationsViewSet,
        VolunteerOwnersViewSet,
        VolunteerMembersViewSet,
    ]
    menu_icon = "group"
    menu_name = _("Volunteering")
