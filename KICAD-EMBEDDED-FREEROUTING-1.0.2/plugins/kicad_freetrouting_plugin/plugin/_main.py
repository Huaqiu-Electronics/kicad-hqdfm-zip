
from kicad_freetrouting_plugin.settings.single_plugin import SINGLE_PLUGIN


def _main():
    if not SINGLE_PLUGIN.show_existing():
        from kicad_freetrouting_plugin.gui.app_base import BaseApp
        
        app = BaseApp()
        app.startup_dialog()

