from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.snippets.views.snippets import SnippetViewSet

from rotary_lights_website.volunteering.models.activities import Activity

# ViewSets
# ----------------------------------------------------------------------

PANELS = [
    MultiFieldPanel(
        children=[
            FieldRowPanel(children=[FieldPanel("name"), FieldPanel("event")]),
            FieldPanel("description"),
            InlinePanel("shifts", label=_("Shifts")),
        ],
        heading=_("Basic Properties"),
    )
]


class ActivityViewSet(SnippetViewSet):
    model = Activity
    exclude_form_fields = []

    icon = "tasks"
    menu_label = _("Activities")
    menu_name = "activities"

    panels = PANELS
