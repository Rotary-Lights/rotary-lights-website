from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    MultiFieldPanel,
    MultipleChooserPanel,
)
from wagtail.snippets.views.snippets import SnippetViewSet

from rotary_lights_website.volunteering.models.organizations import Organization

# ViewSets
# ----------------------------------------------------------------------

PANELS = [
    MultiFieldPanel(
        children=[
            FieldRowPanel(
                children=[
                    FieldPanel("name"),
                    FieldPanel("created", read_only=True),
                ]
            ),
            FieldRowPanel(
                children=[
                    FieldPanel("is_quarantined"),
                    FieldPanel("scheduled_deletion_date", read_only=True),
                ]
            ),
            FieldPanel("address"),
        ],
        heading=_("Basic Properties"),
    ),
    MultiFieldPanel(
        children=[
            FieldRowPanel(
                children=[
                    FieldPanel("primary_contact_name"),
                    FieldPanel("primary_contact_email"),
                    FieldPanel("primary_contact_phone_number"),
                ]
            ),
        ],
        heading=_("Primary Contact Information"),
    ),
    MultiFieldPanel(
        children=[
            FieldRowPanel(
                children=[
                    FieldPanel("secondary_contact_name"),
                    FieldPanel("secondary_contact_email"),
                    FieldPanel("secondary_contact_phone_number"),
                ]
            ),
        ],
        heading=_("Secondary Contact Information"),
        classname="collapsed",
    ),
    MultiFieldPanel(
        children=[MultipleChooserPanel("owners", chooser_field_name="owner")],
        heading=_("Owners"),
        classname="collapsed",
    ),
    MultiFieldPanel(
        children=[MultipleChooserPanel("members", chooser_field_name="volunteer_pk")],
        heading=_("Members"),
        classname="collapsed",
    ),
    MultiFieldPanel(
        children=[
            MultipleChooserPanel(
                "shifts",
                chooser_field_name="shift",
                label=_("Participating Shifts"),
            )
        ],
        heading=_("Volunteering Properties"),
        classname="collapsed",
    ),
]


class OrganizationViewSet(SnippetViewSet):
    model = Organization
    exclude_form_fields = []

    icon = "group"
    menu_label = _("Organizations")
    menu_name = "organizations"

    panels = PANELS
