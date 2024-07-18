import re

from django.forms import Media
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    MultiFieldPanel,
    MultipleChooserPanel,
)
from wagtail.snippets.views.snippets import (
    CreateView,
    EditView,
    IndexView,
    SnippetViewSet,
)

from rotary_lights_website.volunteering.models.organizations import (
    Organization,
    OrganizationOwnersRelation,
)
from rotary_lights_website.volunteering.models.volunteers import Volunteer

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


class OrganizationCreateView(CreateView):
    model = Organization

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if not self.request.user.is_staff:
            ctx["media"] += Media(
                js=["js/hide_owners.js", "js/disable_is_quarantined.js"]
            )

        return ctx

    def post(self, request, *args, **kwargs):
        # Insert the owner as the current user if user is not staff.
        if not self.request.user.is_staff:
            post = self.request.POST.copy()
            self.request.POST = post

        return super().post(request, *args, **kwargs)

    def save_instance(self):
        instance: Organization = super().save_instance()

        if not self.request.user.is_staff:
            OrganizationOwnersRelation.objects.create(
                organization=instance,
                owner=Volunteer.objects.get(user=self.request.user),
            )
        else:
            for post_key, post_value in self.request.POST.items():
                if "owners" in post_key:
                    match = re.search(r"(\d+)-owner", post_key)
                    if match:
                        owner_id = int(post_value)
                        OrganizationOwnersRelation.objects.get_or_create(
                            organization=instance,
                            owner=Volunteer.objects.get(user__pk=owner_id),
                        )

        return instance


class OrganizationEditView(EditView):
    model = Organization

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if not self.request.user.is_staff:
            ctx["media"] += Media(
                js=["js/hide_owners.js", "js/disable_is_quarantined.js"]
            )

        return ctx

    def post(self, request, *args, **kwargs):
        # Insert the owner as the current user if user is not staff.
        if not self.request.user.is_staff:
            post = self.request.POST.copy()
            self.request.POST = post

        return super().post(request, *args, **kwargs)

    def save_instance(self):
        instance: Organization = super().save_instance()

        for post_key, post_value in self.request.POST.items():
            if "owners" in post_key:
                match = re.search(r"(\d+)-owner", post_key)
                if match:
                    owner_id = int(post_value)
                    OrganizationOwnersRelation.objects.get_or_create(
                        organization=instance,
                        owner=Volunteer.objects.get(user__pk=owner_id),
                    )

        return instance


class OrganizationsIndexView(IndexView):
    model = Organization

    def get_queryset(self):
        # Limit the organizations to those of the user.
        queryset = super().get_queryset()
        return queryset.filter(owners__owner__user=self.request.user)


class OrganizationViewSet(SnippetViewSet):
    model = Organization

    add_view_class = OrganizationCreateView
    edit_view_class = OrganizationEditView
    index_view_class = OrganizationsIndexView

    icon = "group"
    menu_label = _("Organizations")
    menu_name = "organizations"

    panels = PANELS
