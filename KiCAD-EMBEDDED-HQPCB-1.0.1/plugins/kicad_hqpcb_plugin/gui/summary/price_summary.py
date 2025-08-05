from dataclasses import dataclass
import wx.dataview as dv
from .bom_price_model import BomPriceModel
from .pcb_price_model import PCBPriceModel
from .smt_price_model import SmtPriceModel
from .price_model_base import PriceModelCol
from .price_model_base import PriceModelBase, PriceItem
from enum import Enum
from kicad_hqpcb_plugin.settings.setting_manager import SETTING_MANAGER


class PriceCategory(Enum):
    PCB = "pcb"
    SMT = "smt"
    BOM = "bom"



PRICE_KIND = 3


@dataclass
class PriceSummary:
    pcb_quantity: int = 0
    days: int = 0
    cost: int = 0


class PriceSummary( ):
    def __init__(self  , models : 'dict[ int,PriceModelBase ]'):

        # self.price_category: "dict[int,PriceModelBase]" = {
        #     PriceCategory.PCB: PCBPriceModel(),
        #     PriceCategory.SMT: SmtPriceModel(),
        # }
        self.price_category = models

    def update_price(self, price: "dict"):
        # for i in PriceCategory.PCB, PriceCategory.SMT, PriceCategory.BOM:
        print(f"{PriceCategory.SMT.value}")
        # if  PriceCategory.SMT.value 
        for i in self.price_category:
            if i.value in price:
                self.price_category[i].update(price[i.value])
        # self.Cleared()


    def get_sum(self):
        s = 0
        for i in self.price_category:
            s = s + self.price_category[i].sum()
        return s
