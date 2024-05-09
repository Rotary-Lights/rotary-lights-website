from typing import TYPE_CHECKING
from typing import Any

from django.core.exceptions import ValidationError
from wagtail.admin.panels import FieldPanel
from wagtail.admin.panels import FieldRowPanel
from wagtail.admin.panels import MultiFieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from rotary_lights_website.volunteering.models import Activity
from rotary_lights_website.volunteering.models import Shift
from rotary_lights_website.volunteering.models import VolunteerOrganization
from rotary_lights_website.volunteering.models import VolunteerOrganizationOwner
from rotary_lights_website.volunteering.models import VolunteerOrganizationUser

if TYPE_CHECKING:
    from datetime import datetime


class ShiftViewSet(SnippetViewSet):
    model = Shift

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("description"),
                FieldRowPanel(
                    [FieldPanel("activity"), FieldPanel("organizations", read_only=True)],
                ),
                FieldRowPanel([FieldPanel("start_time"), FieldPanel("end_time")]),
            ],
            heading="Basic Settings",
        ),
    ]

    def get_form_class(self, for_update=False):
        cls = super().get_form_class(for_update)

        class ShiftAdminForm(cls):
            def clean(self) -> dict[str, Any]:
                cleaned_data = super().clean()

                # Ensure the start time is before the end time.
                start_time: datetime = cleaned_data["start_time"]
                end_time: datetime = cleaned_data["end_time"]
                if start_time and end_time and start_time >= end_time:
                    raise ValidationError(
                        {
                            "start_time": "The shift start time must be before it's end time.",
                        },
                    )
                return cleaned_data

        return ShiftAdminForm


register_snippet(VolunteerOrganization)
register_snippet(VolunteerOrganizationOwner)
register_snippet(VolunteerOrganizationUser)
register_snippet(ShiftViewSet)
register_snippet(Activity)
