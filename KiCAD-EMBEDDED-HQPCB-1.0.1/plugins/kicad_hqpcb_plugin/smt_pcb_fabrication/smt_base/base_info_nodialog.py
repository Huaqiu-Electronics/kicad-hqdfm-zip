from kicad_hqpcb_plugin.kicad.board_manager import BoardManager
from kicad_hqpcb_plugin.utils.form_panel_base import FormKind, FormPanelBase

from .base_info_model import BaseInfoModel,BaseInfo
from kicad_hqpcb_plugin.gui.event.pcb_fabrication_evt_list import (
    LayerCountChange, boardCount,EVT_BOARD_COUNT )

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


class SmtBaseInfoNodialog( ):
    def __init__(self,  board_manager: BoardManager):
        super().__init__()
        self.board_manager = board_manager


    @fitter_and_map_form_value
    def get_from(self, kind: FormKind) -> "dict":
        boardWidth = pcbnew.ToMM(
            self.board_manager.board.GetBoardEdgesBoundingBox().GetWidth()
        )
        boardHeight = pcbnew.ToMM(
            self.board_manager.board.GetBoardEdgesBoundingBox().GetHeight()
        )

            
        layerCount = self.board_manager.board.GetCopperLayerCount()
        if layerCount>2:
            layerCount = 2

        data = BaseInfo(
            single_or_double_technique = layerCount,
            pcb_width = str(round(float(boardWidth) * 0.1, 2)),
            pcb_height = str(round(float(boardHeight) * 0.1, 2)),
            pcb_ban_height = str(round(float(boardHeight) * 0.1, 2)),
            pcb_ban_width = str(round(float(boardWidth) * 0.1, 3)),
        )

        return vars(data)

    def getBaseInfo(self):
        return self.base_info

