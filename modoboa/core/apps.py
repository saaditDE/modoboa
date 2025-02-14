"""Core config for admin."""

from django.apps import AppConfig
from django.db.models import signals
from django.utils.translation import ugettext_lazy


def load_core_settings():
    """Load core settings.

    This function must be manually called (see :file:`urls.py`) in
    order to load base settings.
    """
    from modoboa.parameters import tools as param_tools
    from . import app_settings
    from .api.v2 import serializers

    param_tools.registry.add(
        "global", app_settings.GeneralParametersForm, ugettext_lazy("General"))
    param_tools.registry.add2(
        "global", "core", ugettext_lazy("General"),
        app_settings.GLOBAL_PARAMETERS_STRUCT,
        serializers.CoreGlobalParametersSerializer)


class CoreConfig(AppConfig):
    """App configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "modoboa.core"
    verbose_name = "Modoboa core"

    def ready(self):
        load_core_settings()

        # Import these to force registration of checks and signals
        from . import checks  # NOQA:F401
        from . import handlers

        signals.post_migrate.connect(handlers.create_local_config, sender=self)
