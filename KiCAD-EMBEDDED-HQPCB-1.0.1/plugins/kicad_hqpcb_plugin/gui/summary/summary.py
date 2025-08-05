from kicad_hqpcb_plugin.order.supported_region import SupportedRegion
from kicad_hqpcb_plugin.utils.roles import EditDisplayRole
from .ui_summary_panel import UiSummaryPanel
from kicad_hqpcb_plugin.icon import GetImagePath
import wx
from .order_summary_model import OrderSummaryModel
from .price_summary_model import PriceSummaryModel


import wx.dataview as dv
from kicad_hqpcb_plugin.settings.setting_manager import SETTING_MANAGER
from kicad_hqpcb_plugin.gui.event.pcb_fabrication_evt_list import (
    UpdatePrice,
    PlaceOrder,
    OrderRegionChanged,
    SmtOrderRegionChanged,
    GetUniqueValueFpCount,
)

from kicad_hqpcb_plugin.kicad.helpers import get_valid_footprints
from kicad_hqpcb_plugin.kicad.board_manager import BoardManager

import os
from kicad_hqpcb_plugin.api.base_request import (  SmtRequest )

from pathlib import Path
import tempfile
from enum import Enum
from .price_model_base import PriceModelBase
from .pcb_price_model import PCBPriceModel
from .smt_price_model import SmtPriceModel
from .bom_price_model import BomPriceModel
from ...utils.mediator_class import Mediator
from wx.lib.pubsub import pub
from kicad_hqpcb_plugin.utils.observer_class import Observer

OrderRegionSettings = (
    EditDisplayRole(SupportedRegion.CHINA_MAINLAND, _("Mainland China")),
    EditDisplayRole(SupportedRegion.EUROPE_USA, _("Worldwide (English)")),
    EditDisplayRole(SupportedRegion.JAPAN, _("Worldwide (Japanese)")),
)

class PriceCategory(Enum):
    PCB = "pcb"
    SMT = "smt"
    BOM = "bom"


class Summary():
    def __init__(self, board_manager: BoardManager):
        super().__init__()
        self._board_manager = board_manager
        self.project_path = os.path.split(self._board_manager.board.GetFileName())[0]
        nextpcb_path = os.path.join(self.project_path, "nextpcb")
        try:
            Path(nextpcb_path).mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError) as e:
            self.project_path = os.path.join(tempfile.gettempdir() )
        
        self.db_file_path = os.path.join(self.project_path, "database","hqproject.db")
        self.get_files_dir = os.path.join(self.project_path, "nextpcb", "production_files")
        # self.store = Store(self, self.project_path, self._board_manager.board )

        # self.pcb_price_model = { PriceCategory.PCB: PCBPriceModel() }
        # self.smt_price_model = { PriceCategory.PCB: self.pcb_price_model[PriceCategory.PCB],
        #         PriceCategory.SMT: SmtPriceModel(),
        #         PriceCategory.BOM: BomPriceModel(),
        #         }
        
        # self.pcb_number = 5
        # self.singles_pcb_prices : float = 0
        # self.mediator = Mediator()
        # self.mediator.register( self.smt_price_model[ PriceCategory.BOM ] )

        # self.model_price_summary = PriceSummaryModel( self.pcb_price_model )
        


    def update_total_price(self):
        total_prices = self.pcb_number * self.singles_pcb_prices
        self.mediator.notify( total_prices  )
        self.list_price_detail.Refresh()


    def _get_file_list(self):
        file_list = []
        if os.path.exists(self.get_files_dir) and os.path.isdir(self.get_files_dir):
            # Iterate over files in the directory
            for filename in os.listdir(self.get_files_dir):
                file_path = os.path.join(self.get_files_dir, filename)
                if os.path.isfile(file_path):
                    # Add only files to the file_list
                    file_list.append(file_path)
        return file_list

    def judge_files_exist(self):
        file_list = self._get_file_list()
        self.patch_file = next((file for file in file_list if "CPL" in file and "zip" in file), "")
        self.pcb_file = next((file for file in file_list if "GERBER" in file and "zip" in file), "")
        self.bom_file = next((file for file in file_list if "BOM" in file and "csv" in file), "")
        return os.path.exists(self.patch_file) and os.path.exists(self.pcb_file) and os.path.exists(self.bom_file)

    def get_files(self):
        file_list = self._get_file_list()
        self.patch_file = next((file for file in file_list if "CPL" in file and "zip" in file), "")
        self.pcb_file = next((file for file in file_list if "GERBER" in file and "zip" in file), "")
        self.bom_file = next((file for file in file_list if "BOM" in file and "csv" in file), "")
        smt_files = {
            "patch_file": open(self.patch_file, 'rb'),
            "bom_file": open(self.bom_file, 'rb'),
            "pcb_file": open(self.pcb_file, 'rb'),
        }
        return smt_files

    def get_file_name(self):
        file_list = self._get_file_list()
        patch_file = next((file for file in file_list if "CPL" in file and "zip" in file), "")
        pcb_file = next((file for file in file_list if "GERBER" in file and "zip" in file), "")
        bom_file = next((file for file in file_list if "BOM" in file and "csv" in file), "")
        return SmtRequest(
            patch_file_name=os.path.basename(patch_file),
            bom_file_name=os.path.basename(bom_file),
            pcb_file_name=os.path.basename(pcb_file),
        )

    def update_price_detail(self, price: "dict"):
        self.model_price_summary.update_price(price)

    def get_total_price(self):
        return self.model_price_summary.get_sum()

    def update_order_summary(self, price_summary: "list"):
        self.model_order_summary.update_order_info(price_summary)

