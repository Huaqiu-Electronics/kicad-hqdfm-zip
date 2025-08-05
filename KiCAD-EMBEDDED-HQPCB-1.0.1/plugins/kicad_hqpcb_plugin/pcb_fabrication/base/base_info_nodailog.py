
from kicad_hqpcb_plugin.settings.setting_manager import SETTING_MANAGER

from kicad_hqpcb_plugin.utils.form_panel_base import FormKind, FormPanelBase

from kicad_hqpcb_plugin.kicad.board_manager import BoardManager
from .base_info_model import BaseInfo
from kicad_hqpcb_plugin.settings.form_value_fitter import fitter_and_map_form_value

import pcbnew
import wx


class BaseInfoNodailog():
    def __init__(self, board_manager: BoardManager):
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
        data = BaseInfo(
            blayer=layerCount,
            blength=str(
                (boardHeight/ 10)
            ),
            bwidth=str( ( boardWidth/10 )  )
        )
        return vars(data)

    def init(self):
        self.loadBoardInfo()
