import pcbnew
from kicad_hqpcb_plugin.settings.setting_manager import SETTING_MANAGER
from kicad_hqpcb_plugin.order.order_region import OrderRegion, URL_KIND

from kicad_hqpcb_plugin.kicad.fabrication_data_generator_thread import DataGenThread
from enum import Enum

from kicad_hqpcb_plugin.api.base_request import ( BaseRequest, SmtBaseRequest, SmtRequest, SmtFiles )
from kicad_hqpcb_plugin.utils.form_panel_base import FormKind, FormPanelBase
from kicad_hqpcb_plugin.kicad.fabrication_data_generator import FabricationDataGenerator
from kicad_hqpcb_plugin.utils.request_helper import RequestHelper
from kicad_hqpcb_plugin.settings.default_express import DEFAULT_EXPRESS ,ALLOWED_KEYS , ADDED_DATA

from kicad_hqpcb_plugin.kicad.board_manager import BoardManager
from kicad_hqpcb_plugin.gui.summary.price_summary_model import PriceCategory

from kicad_hqpcb_plugin.gui.summary.order_summary_model import (
    AVAILABLE_TIME_UNIT,
    OrderSummary,
    BuildTime,
    TimeUnit,
)
from kicad_hqpcb_plugin.gui.summary.price_summary import PriceSummary
from kicad_hqpcb_plugin.gui.summary.pcb_price_model import PCBPriceModel
from kicad_hqpcb_plugin.kicad_nextpcb_new.mainwindow_nodialog import MainWindowNodialog


import urllib
import json
import wx
import requests
import webbrowser
from urllib.parse import urlencode
import pcbnew

from kicad_hqpcb_plugin.pcb_fabrication.base.base_info_nodailog import BaseInfoNodailog
from kicad_hqpcb_plugin.pcb_fabrication.process.process_info_nodailog import ProcessInfoNodailog

from kicad_hqpcb_plugin.smt_pcb_fabrication.process.process_info_nodialog import SmtProcessInfoNodialog
from kicad_hqpcb_plugin.smt_pcb_fabrication.smt_base.base_info_nodialog import SmtBaseInfoNodialog
from kicad_hqpcb_plugin.gui.summary.price_summary_model import PriceSummaryModel

from kicad_hqpcb_plugin.gui.summary.pcb_price_model import PCBPriceModel
from kicad_hqpcb_plugin.gui.summary.smt_price_model import SmtPriceModel
from kicad_hqpcb_plugin.gui.summary.bom_price_model import BomPriceModel
from kicad_hqpcb_plugin.gui.summary.summary import Summary
from kicad_hqpcb_plugin.kicad_nextpcb_new.mainwindow_nodialog import MainWindowNodialog


class PCBFormPart(Enum):
    BASE_INFO = 0
    PROCESS_INFO = 1
    SPECIAL_PROCESS = 2
    PERSONALIZED = 3


class PriceCategory(Enum):
    PCB = "pcb"
    SMT = "smt"
    BOM = "bom"


DATA = "data"
LIST = "list"
SUGGEST = "suggest"
DEL_TIME = "deltime"
NAME = "name"
PCS_COUNT = "pcs_count"
TOTAL = "total"
PCB = "pcb"
FEE = "fee"
BCOUNT = "bcount"

class MainInterface:
    def __init__(self, board_manager):
        self._board_manager = board_manager
        self._dataGenThread: DataGenThread = None
        self._fabrication_data_gen = None
        self._fabrication_data_gen_thread = None

        self._pcb_form_parts: "dict[PCBFormPart, FormPanelBase]" = {}
        self.base_info_nodailog =  BaseInfoNodailog( self._board_manager )
        self.process_info_nodailog = ProcessInfoNodailog( self._board_manager )
        self.sme_process_info_nodialog = SmtProcessInfoNodialog( self._board_manager )
        self.smt_base_info_nodialog = SmtBaseInfoNodialog( self._board_manager )


        self.chatId=pcbnew.GetCopilotChatId()
        self.chatId = '11111'

        self.pcb_price_model = { PriceCategory.PCB: PCBPriceModel() }
        self.smt_price_model = { PriceCategory.PCB: self.pcb_price_model[PriceCategory.PCB],
                PriceCategory.SMT: SmtPriceModel(),
                PriceCategory.BOM: BomPriceModel(),
                }

        if self.chatId == '11111':
            self.pcb_on_place_order()
        elif self.chatId == '22222':
            self.pcb_on_update_price()
        elif self.chatId == '33333':
            self.smt_on_update_price()
        elif self.chatId == '44444':
            self.smt_on_place_order()


    def print_board_info(self):
        # 假设 board_manager 是 pcbnew.Board 对象
        print("Board filename:", self.board_manager.GetFileName())
        print("Board layer count:", self.board_manager.GetLayerCount())

    def pcb_on_place_order(self):
        url = OrderRegion.get_url(SETTING_MANAGER.order_region, URL_KIND.PLACE_ORDER)

        if self._dataGenThread is not None:
                self._dataGenThread.join()
                self._dataGenThread = None
        data = self.get_place_order_form()
        file = self.fabrication_data_generator
        self._dataGenThread = DataGenThread(
            self, 
            self.fabrication_data_generator, 
            self.get_place_order_form(), 
            url
        )

    def pcb_on_update_price(self ):
        url = OrderRegion.get_url(SETTING_MANAGER.order_region, URL_KIND.QUERY_PRICE)
        if url is None:
            wx.MessageBox(_("No available url for querying price in current region"))
            return
        
        try:
            form = self.get_query_price_form()
            rep = urllib.request.Request(
                url, data=RequestHelper.convert_dict_to_request_data(form)
            )
            fp = urllib.request.urlopen(rep)
            data = fp.read()
            encoding = fp.info().get_content_charset("utf-8")
            content = data.decode(encoding)
            quote = json.loads(content)
        except Exception as e:
            self.report_part_search_error(_("An unexpected HTTP error occurred: {error}").format(error=e))
        
        if DATA in quote and LIST in quote[DATA]:
            return self.parse_price_list(quote[DATA][LIST])
        elif SUGGEST in quote:
            return self.parse_price(quote)
        else:
            err_msg = quote
            if "msg" in quote:
                err_msg = quote["msg"]
            elif "message" in quote:
                err_msg = quote["message"]
            wx.MessageBox(_("Incorrect form parameter: ") + err_msg)
        
    def smt_on_update_price( self ):
        url = OrderRegion.get_url(SETTING_MANAGER.order_region, URL_KIND.SMT_QUERY_PRICE)
        if url is None:
            wx.MessageBox(_("No available url for querying price in current region"))
            return
        try:
            form = self.smt_get_query_price_form()
            # smt chinese price

            form =form | SmtFiles().__dict__ 
            json_data = json.dumps(form).encode('utf-8')
            headers = {'Content-Type': 'application/json'}
            rep = urllib.request.Request(
                url,  data = json_data, headers=headers
            )
            fp = urllib.request.urlopen(rep)
            data = fp.read()  
            encoding = fp.info().get_content_charset("utf-8")
            content = data.decode(encoding)
            quotes = json.loads(content)
            if not quotes.get("suc", {}):
                wx.MessageBox(_("Return false"))
                return
            quote = quotes.get("body", {})
            smt_price = self.parse_smt_price(quote)

            return smt_price
        except Exception as e:
            wx.MessageBox(str(e))
            raise e  # TODO remove me


    def smt_on_place_order( self ):
        self.summary_view = Summary( self._board_manager )
        
        dlg = MainWindowNodialog(self, self._board_manager)
        dlg.generate_fabrication_data()
        url = OrderRegion.get_url(SETTING_MANAGER.order_region, URL_KIND.SMT_PLACE_ORDER)
        if url is None:
            wx.MessageBox(_("No available url for querying price in current region"))
            return
        try:
            form = self.smt_get_query_price_form()
            # requests会自动处理multipart/form-data
            headers = { 'smt' : '1234' }
            rsp = requests.post(
                url,
                files=self.smt_build_file(),
                data=form,
                headers=headers
            )
            fp = json.loads(rsp.content)
            if fp.get("code", {}) != 0:
                _msg = fp.get("msg", {})
                wx.MessageBox( f"{_msg}",wx.ICON_ERROR )
                return
            _url = fp.get("url", {})
            uat_url = str(_url)
            webbrowser.open(uat_url)

        except Exception as e:
            print(e)
            wx.MessageBox(str(e) )



    def parse_price_list(self, summary: json):
        suggests = []
        for item in summary:
            if SUGGEST in summary[item] and DEL_TIME in summary[item][SUGGEST]:
                for suggest in summary[item][SUGGEST][DEL_TIME]:
                    if NAME in suggest and TOTAL in suggest and PCS_COUNT in suggest:
                        full_time_cost = str(suggest[NAME]).split(" ")
                        if len(full_time_cost) > 1:
                            qty = int(suggest[PCS_COUNT])
                            price = float(suggest[TOTAL])
                            suggests.append(
                                OrderSummary(
                                    pcb_quantity=qty,
                                    price=price,
                                    build_time=BuildTime(
                                        int(full_time_cost[0]), full_time_cost[1]
                                    ),
                                )
                            )


    def parse_smt_price(self, summary: json):
        self.model_price_summary = PriceSummary( self.smt_price_model )
        self.model_price_summary.update_price({PriceCategory.SMT.value: summary})
        # normal_total_price = self.model_price_summary.get_sum()
        return self.model_price_summary.get_sum()
        # self.model_price_summary = PriceSummaryModel( self.smt_price_model )
    
    def parse_price(self, summary: json):
        
        self.model_price_summary = PriceSummary( self.pcb_price_model )
        self.model_price_summary.update_price({PriceCategory.PCB.value: summary})
        normal_total_price = self.model_price_summary.get_sum()

        suggests = []
        if SUGGEST in summary and DEL_TIME in summary[SUGGEST]:
            for suggest in summary[SUGGEST][DEL_TIME]:
                if NAME in suggest and FEE in suggest and BCOUNT in suggest:
                    qty = int(suggest[BCOUNT])
                    price = float(suggest[FEE]) + normal_total_price

                    suggests.append(
                        OrderSummary(
                            pcb_quantity=qty,
                            price=price,
                            build_time=self.parse_zh_data_time(suggest[NAME]),
                        )
                    )


    def parse_zh_data_time(self, dt: str):
        t = ""
        unit = None
        for i in dt:
            if i.isnumeric():
                t = t + i
            elif "天" == i:
                unit = TimeUnit.DAY.value
        if unit is None:
            unit = TimeUnit.HOUR.value
        return BuildTime(int(t), unit)

    @property
    def fabrication_data_generator(self):
        if self._fabrication_data_gen is None:
            self._fabrication_data_gen = FabricationDataGenerator(
                self._board_manager.board
            )
        return self._fabrication_data_gen

    def get_place_order_form(self):
        return {**self.build_form(FormKind.PLACE_ORDER), "type": "pcbfile"}


    def get_query_price_form(self):
            form = self.build_form(FormKind.QUERY_PRICE)
            form = form | DEFAULT_EXPRESS | { "sid": self.chatId }
            return form


    def build_form(self, kind: FormKind):
        base = BaseRequest().__dict__
        data = self.base_info_nodailog.get_from(kind)
        data1 = self.process_info_nodailog.get_from(kind)
        base = base | data | data1 
        # for i in self._pcb_form_parts.values():
        #     base = base | i.get_from(kind)
        return base

    def smt_get_query_price_form(self):
            form = self.smt_build_form(FormKind.QUERY_PRICE)
            form = form | { "sid": self.chatId }
            return form


    def smt_build_form(self, kind: FormKind):
        # base = BaseRequest().__dict__
        base = self.summary_view.get_file_name().__dict__
        data = self.sme_process_info_nodialog.get_from(kind)
        data1 = self.smt_base_info_nodialog.get_from(kind)
        base = base | data | data1
        return base
    

    def smt_build_file(self):
        
        smt_files = self.summary_view.get_files()
        return smt_files


    def report_part_search_error(self, reason):
        wx.MessageBox(
            _("Failed to request the API:\r\n{reason}.\r\n \r\nPlease try making the request again.\r\n").format(reason=reason),
            _("Error"),
            style=wx.ICON_ERROR,
        )
        return
