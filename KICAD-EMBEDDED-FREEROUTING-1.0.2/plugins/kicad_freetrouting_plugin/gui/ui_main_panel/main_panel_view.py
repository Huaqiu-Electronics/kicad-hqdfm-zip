import wx
import wx.xrc
import wx.dataview
import wx.dataview as dv

from .ui_main_panel import UiMainPanel
from .main_panel_model import MainPanelModel


class MainPanel(UiMainPanel):
    def __init__(
        self,
        parent,
        id=wx.ID_ANY,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=wx.TAB_TRAVERSAL,
        name=wx.EmptyString,
    ):
        super().__init__(parent, id=id, pos=pos, size=size, style=style, name=name)
        # self.part_list.EnableSelectionCopy(True)
        self.property = self.aDataView.AppendTextColumn(
            _("Property"),
            width=180,
            mode=dv.DATAVIEW_CELL_ACTIVATABLE,
            align=wx.ALIGN_LEFT,
        )
        self.value = self.aDataView.AppendTextColumn(
            _("Value"), width=-1, mode=dv.DATAVIEW_CELL_ACTIVATABLE, align=wx.ALIGN_LEFT
        )



    def update_data_view(self, part_details_data):
        self.main_panel_model = MainPanelModel( part_details_data )
        self.aDataView.AssociateModel(self.main_panel_model)
        wx.CallAfter(self.Layout)


    def update_view(self):
        self.Layout()
        