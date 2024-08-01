from django.utils.translation import gettext_lazy as _
from wagtail.admin.views.reports import ReportView

from rotary_lights_website.volunteering.models.organizations import Organization
from rotary_lights_website.volunteering.models.volunteers import Volunteer


class VolunteerAvailabilityReport(ReportView):
    title = _("Volunteer Availability")
    list_export = [
        "name",
        "primary_contact_email",
        "secondary_contact_email",
        "notes",
        "notable_skills",
        "count_members",
        "first_activity",
        "second_activity",
        "third_activity",
    ]
    export_headings = {"count_members": _("Number of Members")}
    export_filename = "Volunteer Availability"

    def get_queryset(self):
        return Organization.objects.all()


class VolunteerContactInformationReport(ReportView):
    title = _("Volunteer Contact Information")
    list_export = [
        "get_first_name",
        "get_last_name",
        "get_email",
        "address",
        "primary_phone_number",
        "secondary_phone_number",
    ]
    export_headings = {
        "get_email": _("Email Address"),
        "get_first_name": _("First Name"),
        "get_last_name": _("Last Name"),
    }
    export_filename = "Volunteer Contact Information"

    def get_queryset(self):
        return Volunteer.objects.all()
