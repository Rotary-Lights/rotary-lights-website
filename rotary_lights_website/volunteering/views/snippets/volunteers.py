import re
from typing import List

from django import forms
from django.conf import settings
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from phonenumber_field.widgets import RegionalPhoneNumberWidget
from polymorphic.managers import PolymorphicQuerySet
from wagtail.admin.forms.choosers import BaseFilterForm, LocaleFilterMixin
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    MultiFieldPanel,
)
from wagtail.admin.ui.tables import TitleColumn
from wagtail.admin.views.generic.chooser import (
    BaseChooseView,
    ChooseResultsViewMixin,
    ChooseViewMixin,
    CreationFormMixin,
)
from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.models import TranslatableMixin
from wagtail.snippets.views.snippets import (
    SnippetViewSet,
)

from rotary_lights_website.volunteering.models.organizations import (
    OrganizationOwnersRelation,
)
from rotary_lights_website.volunteering.models.volunteers import Volunteer

# Choosers
# ----------------------------------------------------------------------


class VolunteerSearchFilterMixin(forms.Form):
    """A form implementing a search to filter Volunteers."""

    q = forms.CharField(
        label=_("Search Volunteers"),
        widget=forms.TextInput(attrs={"placeholder": _("Search")}),
        required=False,
    )

    def filter(
        self,
        objects: PolymorphicQuerySet[Volunteer],
    ) -> PolymorphicQuerySet[Volunteer]:
        """Filter possible parents of a Volunteer.

        Filters applied:
            - Search queries provided by user.

        Args:
            objects (PolymorphicQuerySet[Volunteer]): The initial
            queryset to filter against.

        Returns:
            PolymorphicQuerySet[Volunteer]: The filtered queryset.
        """
        objects = super().filter(objects)

        # Run any searches provided by the user.
        filters = Q()
        search_query: str | None = self.cleaned_data.get("q")
        if search_query:
            filters |= Q(name__icontains=search_query)
            self.is_searching = True
            self.search_query = search_query

        return objects.filter(filters)


class AbstractVolunteerChooseView(BaseChooseView):
    ordering = ["user__first_name", "user__last_name"]

    @property
    def columns(self) -> List[TitleColumn]:
        return [
            TitleColumn(
                name="__str__",
                label=_("Name"),
                url_name=self.chosen_url_name,
                link_attrs={"data-chooser-modal-choice": True},
            ),
        ]

    def get_filter_form_class(self):
        bases = [VolunteerSearchFilterMixin, BaseFilterForm]

        i18n_enabled = getattr(settings, "WAGTAIL_I18N_ENABLED", False)
        if i18n_enabled and issubclass(self.model_class, TranslatableMixin):
            bases.insert(0, LocaleFilterMixin)

        return type(
            "FilterForm",
            tuple(bases),
            {},
        )


class VolunteerChooseView(
    ChooseViewMixin,
    CreationFormMixin,
    AbstractVolunteerChooseView,
):
    def get_object_list(self):
        queryset = super().get_object_list()
        referer = self.request.headers.get("referer", "")

        if "add" in referer and not self.request.user.is_staff:
            # Filter out the current self.request.user
            queryset = queryset.exclude(user=self.request.user)
        else:
            # Filter out owners (through OrganizationOwnersRelation)
            match = re.search(r"(\d+)\/?$", referer)
            if match:
                organization_id = int(match.group(1))
                owner_ids = OrganizationOwnersRelation.objects.filter(
                    organization_id=organization_id
                ).values_list("owner_id", flat=True)
                queryset = queryset.exclude(id__in=owner_ids)

        return queryset


class VolunteerChooseResultsView(
    ChooseResultsViewMixin,
    CreationFormMixin,
    AbstractVolunteerChooseView,
):
    pass


class VolunteerChooserViewSet(ChooserViewSet):
    model = Volunteer

    choose_view_class = VolunteerChooseView
    choose_results_view_class = VolunteerChooseResultsView

    icon = "user"
    choose_one_text = _("Choose a volunteer")
    choose_another_text = _("Choose another volunteer")
    edit_item_text = _("Edit this volunteer")


volunteer_chooserviewset = VolunteerChooserViewSet("volunteer_chooser")


# ViewSets
# ----------------------------------------------------------------------

PANELS = [
    MultiFieldPanel(children=[FieldPanel("user")], heading=_("Basic Properties")),
    MultiFieldPanel(
        children=[
            FieldPanel("address"),
            FieldRowPanel(
                children=[
                    FieldPanel(
                        "primary_phone_number",
                        widget=RegionalPhoneNumberWidget,
                    ),
                    FieldPanel(
                        "secondary_phone_number",
                        widget=RegionalPhoneNumberWidget,
                    ),
                ]
            ),
        ],
        heading=_("Contact Information"),
        classname="collapsed",
    ),
]


class VolunteerViewSet(SnippetViewSet):
    model = Volunteer
    exclude_form_fields = []

    icon = "user"
    menu_label = _("Volunteers")
    menu_name = "volunteers"

    panels = PANELS
