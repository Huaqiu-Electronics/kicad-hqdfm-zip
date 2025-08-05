# Inspired by https://github.com/AislerHQ/PushForKiCad/blob/main/src/plugin.py

import pcbnew
import os

from kicad_freetrouting_plugin.plugin._main import _main
from kicad_freetrouting_plugin.icon import ICON_ROOT


class KiCadAmfActionPlugin(pcbnew.ActionPlugin):
    def __init__(self):
        self.name = "Freerouting"
        self.category = "PCB auto routing"
        self.description = "Freerouting for PCB auto routing"
        self.pcbnew_icon_support = hasattr(self, "show_toolbar_button")
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(ICON_ROOT, "icon.png")
        self.dark_icon_file_name = os.path.join(ICON_ROOT, "icon.png")

    def Run(self):
        _main()
