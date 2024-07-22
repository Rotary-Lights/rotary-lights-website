from birdsong.blocks import DefaultBlocks
from birdsong.models import Campaign
from django.db import models
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel


class VolunteeringCampaign(Campaign):
    body = StreamField(DefaultBlocks())

    panels = [*Campaign.panels, FieldPanel('body')]