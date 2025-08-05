import wx
from kicad_hqpcb_plugin.order.order_region import OrderRegion, SupportedRegion
from kicad_hqpcb_plugin.settings.setting_manager import SETTING_MANAGER
from kicad_hqpcb_plugin.settings.form_value_fitter import fitter_and_map_form_value

from .ui_smt_personalized import UiPersonalizedService, BOX_SP_REQUEST
from kicad_hqpcb_plugin.utils.constraint import BOOLEAN_CHOICE
from .personalized_info_model import PersonalizedInfo
from kicad_hqpcb_plugin.utils.form_panel_base import FormKind, FormPanelBase
from kicad_hqpcb_plugin.utils.roles import EditDisplayRole
from kicad_hqpcb_plugin.settings.single_plugin import SINGLE_PLUGIN
import pcbnew

class SmtPersonalizedInfoNodialog(UiPersonalizedService, FormPanelBase):
    def __init__(self, parent, _):
        super().__init__(parent)

    @fitter_and_map_form_value
    def get_from(self, kind: FormKind) -> "dict":
        info = PersonalizedInfo( )
        boardWidth = pcbnew.ToMM(
            self.board_manager.board.GetBoardEdgesBoundingBox().GetWidth()
        )
        boardHeight = pcbnew.ToMM(
            self.board_manager.board.GetBoardEdgesBoundingBox().GetHeight()
        )
        info.pcb_width = str(float(boardWidth) * 0.1)
        info.pcb_height = str(float(boardHeight) * 0.1)
        return vars(info)

    @property
    def sp_box(self):
        return self.FindWindowById(BOX_SP_REQUEST)

    def on_need_split_changed( self, evt=None ):
        self.single_pcb_panel.Show(self.need_split.GetSelection() == 1)  
        self.Layout()
        if SINGLE_PLUGIN.get_main_wind() is not None:
            SINGLE_PLUGIN.get_main_wind().smt_adjust_size()

    def on_region_changed(self):
        for i in [ self.is_layout_cleaning, self.is_layout_cleaning_label,
                  self.is_welding_wire, self.is_welding_wire_label, self.is_assemble, self.is_assemble_label,
                  self.is_increase_tinning , self.is_increase_tinning_label,] :
            i.Show( SETTING_MANAGER.order_region == SupportedRegion.CHINA_MAINLAND )
        
        self.need_split.SetSelection(0)
        self.need_split.Enable(SETTING_MANAGER.order_region == SupportedRegion.CHINA_MAINLAND)
        self.on_need_split_changed( None )
        self.Layout()


