from kicad_hqpcb_plugin.kicad.board_manager import BoardManager
from kicad_hqpcb_plugin.order.supported_region import SupportedRegion
from kicad_hqpcb_plugin.settings.setting_manager import SETTING_MANAGER
from kicad_hqpcb_plugin.settings.single_plugin import SINGLE_PLUGIN
from kicad_hqpcb_plugin.utils.form_panel_base import FormKind, FormPanelBase
from kicad_hqpcb_plugin.utils.observer_class import Subject
from .base_info_model import BaseInfoModel
from kicad_hqpcb_plugin.gui.event.pcb_fabrication_evt_list import (
    LayerCountChange, boardCount,EVT_BOARD_COUNT )
from .ui_smt_base_info import (
    UiSmtBaseInfo,
    BOX_SIZE_SETTING,
    # BOX_PANEL_SETTING,
    # BOX_BREAK_AWAY,
)
from kicad_hqpcb_plugin.utils.validators import (
    NumericTextCtrlValidator,
    FloatTextCtrlValidator,
)
from kicad_hqpcb_plugin.utils.roles import EditDisplayRole
from kicad_hqpcb_plugin.settings.form_value_fitter import fitter_and_map_form_value
from kicad_hqpcb_plugin.settings.supported_layer_count import AVAILABLE_LAYER_COUNTS

import pcbnew
import wx
from wx.lib.pubsub import pub


class SmtBaseInfoView(UiSmtBaseInfo, FormPanelBase, Subject,):
    def __init__(self, parent, board_manager: BoardManager):
        super().__init__(parent)
        Subject.__init__(self)
        self.board_manager = board_manager

    @property
    def box_piece_or_panel_size(self):
        return self.FindWindowById(BOX_SIZE_SETTING)


    def get_pcb_length(self):
        """Default is mm
        Returns:
            _type_: float
        """
        return float(self.edit_size_x.GetValue())
        

    def get_pcb_width(self):
        """Default is mm
        Returns:
            _type_: float
        """
        return float(self.edit_size_y.GetValue())

    @fitter_and_map_form_value
    def get_from(self, kind: FormKind) -> "dict":
        boardWidth = pcbnew.ToMM(
            self.board_manager.board.GetBoardEdgesBoundingBox().GetWidth()
        )
        boardHeight = pcbnew.ToMM(
            self.board_manager.board.GetBoardEdgesBoundingBox().GetHeight()
        )

        data = BaseInfoModel(
            pcb_width = str(float(boardWidth) * 0.1)
            pcb_height = str(float(boardHeight) * 0.1)
 
            pcb_ban_height=str(
                FormPanelBase.convert_geometry(
                    kind, SETTING_MANAGER.order_region, self.get_pcb_length()
                )
            ),
            pcb_ban_width=str(
                FormPanelBase.convert_geometry(
                    kind, SETTING_MANAGER.order_region, self.get_pcb_width()
                )
            ),
        )
        return vars(data)

    def getBaseInfo(self):
        return self.base_info


    def loadBoardInfo(self):

        self.edit_size_x.SetValue(str(boardWidth))
        self.edit_size_y.SetValue(str(boardHeight))
