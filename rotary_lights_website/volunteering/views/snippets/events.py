from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.snippets.views.snippets import SnippetViewSet

from rotary_lights_website.volunteering.models.events import Event

# Choosers
# ----------------------------------------------------------------------


class EventChooserViewSet(ChooserViewSet):
    model = Event
    exclude_form_fields = []

    icon = "calendar-check"
    choose_one_text = _("Choose one event")
    choose_another_text = _("Choose another event")
    edit_item_text = _("Edit this event")


event_chooserviewset = EventChooserViewSet("event_chooser")


# ViewSets
# ----------------------------------------------------------------------

PANELS = [
    MultiFieldPanel(
        children=[
            FieldRowPanel(children=[FieldPanel("name")]),
            FieldPanel("description"),
            InlinePanel("activities", label=_("Activities")),
        ],
        heading=_("Basic Properties"),
    ),
    MultiFieldPanel(
        children=[
            FieldRowPanel(children=[FieldPanel("start_date"), FieldPanel("end_date")]),
            FieldRowPanel(
                children=[
                    FieldPanel("volunteer_registration_open"),
                    FieldPanel("volunteer_registration_close"),
                ]
            ),
        ],
        heading=_("Dates & Times"),
        classname="collapsed",
    ),
]


class EventViewSet(SnippetViewSet):
    model = Event
    exclude_form_fields = []

    icon = "calendar-check"
    menu_label = _("Events")
    menu_name = "events"

    panels = PANELS
