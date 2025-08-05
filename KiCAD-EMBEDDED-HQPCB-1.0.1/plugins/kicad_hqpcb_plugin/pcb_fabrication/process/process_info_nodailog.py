from kicad_hqpcb_plugin.kicad.board_manager import BoardManager
from kicad_hqpcb_plugin.settings.form_value_fitter import fitter_and_map_form_value
from .process_info_model import ProcessInfo
from kicad_hqpcb_plugin.utils.form_panel_base import FormKind, FormPanelBase


from .ui_process_info import UiProcessInfo
import wx
import pcbnew
from pcbnew import PCB_TRACK, PCB_TRACE_T, PCB_ARC_T, PCB_VIA_T


OZ = "oz"

MIL = "mil"

MM = "mm"

DEFAULT_MIN_TRACK_WIDTH = 6



GOLD_THICKNESS_CHOICE_UNIT = "µm"



class ProcessInfoNodailog( ):
    def __init__(self, board_manager: BoardManager):
        super().__init__()
        self.board_manager = board_manager

        self.minTrace =None
        self.minHoleSize =None
        self.loadBoardInfo()

    @fitter_and_map_form_value
    def get_from(self, kind: FormKind) -> "dict":
        thickness = pcbnew.ToMM(self.get_board_thickness_in_kicad_setting),
        info = ProcessInfo(
            

            bheight = str( thickness[0]  ),
            lineweight=str(
                self.minTrace 
            ),
            vias=str( self.minHoleSize )

        )
        return vars(info)

    def init(self):
        self.loadBoardInfo()

    @property
    def layer_count(self):
        return self.board_manager.board.GetCopperLayerCount()
    
    @property
    def get_board_thickness_in_kicad_setting(self):
        return self.board_manager.board.GetDesignSettings().GetBoardThickness()

    def loadBoardInfo(self):
        self.setup_trace_and_via()



    def set_min_trace(self, minTraceWidth, minTraceClearance):
        if minTraceWidth == 0 and minTraceClearance == 0:
            self.minTrace = 6
        elif minTraceWidth == 0:
            self.minTrace = minTraceClearance
        elif minTraceClearance == 0:
            self.minTrace = minTraceWidth
        else:
            self.minTrace = min(minTraceWidth, minTraceClearance)

        if self.minTrace == 0:
            self.minTrace = 6
        
        elif self.minTrace > 8:
            self.minTrace = 10
            
        elif self.minTrace > 6:
            self.minTrace = 8
            
        elif self.minTrace > 5:
            self.minTrace = 6
            
        elif self.minTrace > 4:
            self.minTrace = 5
            
        elif self.minTrace > 3.5:
            self.minTrace = 4
            
        else:
            self.minTrace = 3.5
            

    def set_min_hole(self, minHoleSize):
        if minHoleSize == 0:
            self.minHoleSize  = 0.3

        elif minHoleSize >= 0.3:
            self.minHoleSize  = 0.3

        elif minHoleSize >= 0.25:
            self.minHoleSize  = 0.25

        elif minHoleSize >= 0.2:
            self.minHoleSize  = 0.2

        else:
            self.minHoleSize  = 0.15


    def setup_trace_and_via(self):
        designSettings = self.board_manager.board.GetDesignSettings()
        minTraceWidth = (
            designSettings.m_TrackMinWidth
            if designSettings.m_TrackMinWidth != 0
            else None
        )
        minTraceClearance = designSettings.m_MinClearance
        min_value = min(designSettings.m_MinThroughDrill, designSettings.m_ViasMinSize)
        minHoleSize = min_value if min_value != 0 else None

        tracks: "list[PCB_TRACK]" = self.board_manager.board.Tracks()
        for i in tracks:
            type_id = i.Type()
            if type_id in (PCB_TRACE_T, PCB_ARC_T):
                if minTraceWidth is None:
                    minTraceWidth = i.GetWidth()
                    continue
                minTraceWidth = min(minTraceWidth, i.GetWidth())
            elif type_id == PCB_VIA_T:
                if minHoleSize is None:
                    minHoleSize = i.GetDrillValue()
                    continue
                minHoleSize = min(minHoleSize, i.GetDrillValue())

        if minTraceWidth is None:
            minTraceWidth = 0
        if minTraceClearance is None:
            minTraceClearance = 0
        self.set_min_trace(
            pcbnew.ToMils(minTraceWidth), pcbnew.ToMils(minTraceClearance)
        )
        if minHoleSize is None:
            minHoleSize = 0
        self.set_min_hole(pcbnew.ToMM(minHoleSize))
