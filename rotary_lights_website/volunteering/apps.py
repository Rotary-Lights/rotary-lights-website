from contextlib import suppress

from django.apps import AppConfig


class VolunteeringConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rotary_lights_website.volunteering"

    def ready(self) -> None:
        with suppress(ImportError):
            import rotary_lights_website.users.signals  # noqa: F401

        return super().ready()
