from django.utils.translation import gettext_lazy as _
from wagtail.snippets.views.snippets import SnippetViewSet

from rotary_lights_website.volunteering.models import VolunteerMember

# Choosers
# ----------------------------------------------------------------------


# ViewSets
# ----------------------------------------------------------------------


class VolunteerMembersViewSet(SnippetViewSet):
    model = VolunteerMember
    menu_icon = "group"
    menu_label = _("Organization Members")
