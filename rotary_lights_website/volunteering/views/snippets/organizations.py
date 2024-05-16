from wagtail.snippets.views.snippets import SnippetViewSet

from rotary_lights_website.volunteering.models import VolunteerOrganization

# Choosers
# ----------------------------------------------------------------------


# ViewSets
# ----------------------------------------------------------------------


class VolunteerOrganizationsViewSet(SnippetViewSet):
    model = VolunteerOrganization
    menu_icon = "group"
