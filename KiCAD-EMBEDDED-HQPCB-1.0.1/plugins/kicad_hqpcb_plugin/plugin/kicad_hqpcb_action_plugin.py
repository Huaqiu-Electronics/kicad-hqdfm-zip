# Inspired by https://github.com/AislerHQ/PushForKiCad/blob/main/src/plugin.py

import pcbnew
import os

from kicad_hqpcb_plugin.plugin._main import _main
from kicad_hqpcb_plugin.icon import ICON_ROOT


class KiCadHqpcbActionPlugin(pcbnew.ActionPlugin):
    def __init__(self):
        self.name = "PCB"
        self.category = "Manufacturing"
        self.description = "Quote and place order."
        self.pcbnew_icon_support = hasattr(self, "show_toolbar_button")
        self.show_toolbar_button = False
        self.icon_file_name = os.path.join(ICON_ROOT, "None")
        self.dark_icon_file_name = os.path.join(ICON_ROOT, "None")
        # self.icon_file_name = os.path.join(ICON_ROOT, "icon.png")
        # self.dark_icon_file_name = os.path.join(ICON_ROOT, "icon.png")


    def Run(self):
        _main()
