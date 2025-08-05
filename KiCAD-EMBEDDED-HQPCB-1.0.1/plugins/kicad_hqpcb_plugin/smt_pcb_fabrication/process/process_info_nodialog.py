from kicad_hqpcb_plugin.kicad.board_manager import BoardManager
from kicad_hqpcb_plugin.settings.form_value_fitter import fitter_and_map_form_value
from .process_info_model import ProcessInfoModel, ProcessInfo
from kicad_hqpcb_plugin.utils.form_panel_base import FormKind, FormPanelBase
from kicad_hqpcb_plugin.utils.roles import EditDisplayRole
from kicad_hqpcb_plugin.settings.setting_manager import SETTING_MANAGER
from kicad_hqpcb_plugin.settings.single_plugin import SINGLE_PLUGIN
from kicad_hqpcb_plugin.order.supported_region import SupportedRegion

from .ui_process_info import UiProcessInfo
import wx
from collections import defaultdict


class SmtProcessInfoNodialog():
    def __init__(self,  board_manager: BoardManager):
        super().__init__()
        self.board_manager = board_manager
        self.init()


    @fitter_and_map_form_value
    def get_from(self, kind: FormKind) -> "dict":
        info = ProcessInfo(

            patch_pad_number = self.patch_pad_number,
            is_plug = self.is_plug,
            # self.is_plug.GetStringSelection(),
            plug_number = self.plug_number,

        )
        return vars(info)

    def init(self):
        self.GetPatchPadCount()

    def GetPatchPadCount(self):
        self.is_plug = 0
        self.plug_number = 0
        
        pads = self.board_manager.board.GetPads()

        # 使用defaultdict来自动初始化计数为0
        attrib_counts = defaultdict(int, {'PTH': 0, 'SMD': 0})
        
        # PAD_ATTRIB中各属性的值
        PAD_ATTRIB_VALUES = {
            0: 'PTH',
            1: 'SMD',
            2: 'CONN',
            3: 'NPTH'
        }

        for pad in pads:
            attrib = pad.GetAttribute()
            # 直接使用PAD_ATTRIB中的键来增加计数
            if attrib in PAD_ATTRIB_VALUES:
                attrib_name = PAD_ATTRIB_VALUES[attrib]
                attrib_counts[attrib_name] += 1
        
        self.patch_pad_number = str( attrib_counts['SMD'] )
        if attrib_counts['PTH'] != 0:
            self.is_plug= 1 
            self.plug_number = str( attrib_counts['PTH'] )

