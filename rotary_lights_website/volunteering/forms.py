from typing import TYPE_CHECKING
from typing import Any

from django.core.exceptions import ValidationError
from wagtail.admin.forms import WagtailAdminPageForm

from rotary_lights_website.volunteering.models import Shift

if TYPE_CHECKING:
    from datetime import datetime


class ShiftAdminForm(WagtailAdminPageForm):
    class Meta:
        model = Shift
        fields = "__all__"

    def save(self, commit=True) -> Shift:
        instance: Shift = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
            instance.check_for_overlaps()
        return instance

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
