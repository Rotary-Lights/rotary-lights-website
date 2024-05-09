from django.apps import AppConfig


class VolunteeringConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rotary_lights_website.volunteering"

    def ready(self) -> None:
        from rotary_lights_website.volunteering import forms  # noqa: F401

        return super().ready()
