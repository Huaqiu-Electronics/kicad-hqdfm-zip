from kicad_freetrouting_plugin.language.lang_const import LANG_DOMAIN
from kicad_freetrouting_plugin.settings.supported_layer_count import AVAILABLE_LAYER_COUNTS
import builtins
import sys
import os
from kicad_freetrouting_plugin import PLUGIN_ROOT
from kicad_freetrouting_plugin.icon import GetImagePath
import wx
from kicad_freetrouting_plugin.settings.setting_manager import SETTING_MANAGER

# add translation macro to builtin similar to what gettext does
builtins.__dict__["_"] = wx.GetTranslation


def _displayHook(obj):
    if obj is not None:
        print(repr(obj))


class BaseApp(wx.EvtHandler):
    def __init__(self):
        super().__init__()
        sys.displayhook = _displayHook
        wx.Locale.AddCatalogLookupPathPrefix(
            os.path.join(PLUGIN_ROOT, "language", "locale")
        )
        existing_locale = wx.GetLocale()
        if existing_locale is not None:
            existing_locale.AddCatalog(LANG_DOMAIN)
        # self.progress_dialog = wx.ProgressDialog(_("Open Software"), _("In progress") )
        # self.progress_dialog.Update( 30 )


    def startup_dialog(self):

        from .freerouting import MyFrame
        self.dialog = MyFrame()
        self.dialog.SetIcon(wx.Icon(GetImagePath("ROUTE.ico")))
        self.dialog.Show()
        

    #     self.progress_dialog.Update( 100 )
    #     self.progress_dialog.Destroy()

    # def __del__(self):
    #     self.progress_dialog.Destroy()
        