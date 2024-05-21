from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel
from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.snippets.views.snippets import SnippetViewSet

from rotary_lights_website.volunteering.models.shifts import Shift

# Choosers
# ----------------------------------------------------------------------


class ShiftChooserViewSet(ChooserViewSet):
    model = Shift
    exclude_form_fields = []

    icon = "calendar-check"
    choose_one_text = _("Choose one shift")
    choose_another_text = _("Choose another shift")
    edit_item_text = _("Edit this shift")


shift_chooserviewset = ShiftChooserViewSet("shift_chooser")


# ViewSets
# ----------------------------------------------------------------------

PANELS = [
    MultiFieldPanel(
        children=[
            FieldPanel("activity"),
            FieldRowPanel(children=[FieldPanel("start_date"), FieldPanel("end_date")]),
        ],
        heading=_("Basic Properties"),
    ),
]


class ShiftViewSet(SnippetViewSet):
    model = Shift
    exclude_form_fields = []

    icon = "calendar-check"
    menu_label = _("Shifts")
    menu_name = "shifts"

    panels = PANELS
