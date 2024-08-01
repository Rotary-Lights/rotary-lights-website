from django.utils.translation import gettext_lazy as _
from wagtail.admin.views.reports import ReportView

from rotary_lights_website.volunteering.models.organizations import Organization
from rotary_lights_website.volunteering.models.volunteers import Volunteer


class VolunteerAvailabilityReport(ReportView):
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

    def get_queryset(self):
        return Organization.objects.all()


class VolunteerContactInformationReport(ReportView):
    title = _("Volunteer Contact Information")
    list_export = [
        "get_email",
        "address",
        "primary_phone_number",
        "secondary_phone_number",
    ]

    def get_queryset(self):
        return Volunteer.objects.all()
