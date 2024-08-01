from birdsong.wagtail_hooks import (
    BirdsongAdminGroup,
    CampaignAdmin,
    ContactAdmin,
    modeladmin_re_register,
)
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.admin.menu import AdminOnlyMenuItem
from wagtail.snippets.models import register_snippet

from rotary_lights_website.volunteering.models.emails import VolunteeringCampaign
from rotary_lights_website.volunteering.views.reports import (
    VolunteerAvailabilityReport,
    VolunteerContactInformationReport,
)
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


class CampaignAdmin(CampaignAdmin):
    model = VolunteeringCampaign


@modeladmin_re_register
class BirdsongAdminGroup(BirdsongAdminGroup):
    items = (CampaignAdmin, ContactAdmin)


@hooks.register("register_admin_viewset")
def register_events_chooserviewset() -> EventChooserViewSet:
    return event_chooserviewset


@hooks.register("register_admin_viewset")
def register_volunteers_chooserviewset() -> VolunteerChooserViewSet:
    return volunteer_chooserviewset


@hooks.register("register_admin_viewset")
def register_shifts_chooserviewset() -> ShiftChooserViewSet:
    return shift_chooserviewset


@hooks.register("register_reports_menu_item")
def register_volunteer_contact_information_report() -> AdminOnlyMenuItem:
    return AdminOnlyMenuItem(
        _("Volunteer Contact Information"),
        reverse("volunteer_contact_information_report"),
        order=700,
    )


@hooks.register("register_admin_urls")
def register_volunteer_contact_information_report_url() -> list:
    return [
        path(
            "reports/volunteer-contact-information/",
            VolunteerContactInformationReport.as_view(),
            name="volunteer_contact_information_report",
        ),
    ]


@hooks.register("register_reports_menu_item")
def register_volunteer_availability_report() -> AdminOnlyMenuItem:
    return AdminOnlyMenuItem(
        _("Volunteer Availability"),
        reverse("volunteer_availability_report"),
        order=700,
    )


@hooks.register("register_admin_urls")
def register_volunteer_availability_report_url() -> list:
    return [
        path(
            "reports/volunteer-availability/",
            VolunteerAvailabilityReport.as_view(),
            name="volunteer_availability_report",
        ),
    ]


register_snippet(VolunteeringViewSetGroup)
