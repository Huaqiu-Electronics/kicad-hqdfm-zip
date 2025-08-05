
import wx
import wx.xrc
from .ui_main_panel.main_panel_view import MainPanel
from .ui_main_panel.main_panel_model import MainPanelModel
import pcbnew
import os
import configparser
from pathlib import Path
import re
import textwrap
import base64
import random
import threading
from .api_route import ApiRoute, file_to_base64


import time

# Remove java offending characters
def search_n_strip(s):
    s = re.sub('[ΩµΦ]', '', s)
    return s


parameters = {
    "nets_total": _("nets total count"),
    "traces_total": _("traces total count"),
    "vias_total": _("vias total count"),
}


# message dialog style
wx_caption = "KiCad Freerouting Plugin"

# display warning text with a question to the user
def wx_show_warning(text):
    message = textwrap.dedent(text)
    style = wx.YES_NO | wx.ICON_WARNING
    dialog = wx.MessageDialog(None, message=message, caption=wx_caption, style=style)
    return dialog.ShowModal()

# display error text to the user
def wx_show_error(text):
    message = textwrap.dedent(text)
    style = wx.OK | wx.ICON_ERROR
    dialog = wx.MessageDialog(None, message=message, caption=wx_caption, style=style)
    dialog.ShowModal()
    dialog.Destroy()

# run functon inside gui-thread-safe context, requires wx.App on phoenix
def wx_safe_invoke(function, *args, **kwargs):
    wx.CallAfter(function, *args, **kwargs)


# verify required pcbnew api is present
def has_pcbnew_api():
    return hasattr(pcbnew, 'ExportSpecctraDSN') and hasattr(pcbnew, 'ImportSpecctraSES')


class MyFrame ( wx.Frame ):

    def __init__( self, parent=None ):
        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title=_("Freerouting"),
            pos=wx.DefaultPosition,
            size=  wx.Size(500, 600),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX,
        )
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
        self.here_path, self.file_name = os.path.split(os.path.abspath(__file__))

        self.main_panel = MainPanel(self)
        self.api_route = ApiRoute(self.main_panel.m_gauge)
        # Controls KiCAD session file imports (works only in KiCAD nigthly or 6)
        self.SPECCTRA=True


        self.timer = wx.Timer(self)
        # self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        bSizer2.Add( self.main_panel, 1, wx.ALL|wx.EXPAND, 5 )

        self.SetSizer( bSizer2 )
        self.Layout()

        self.Centre( wx.BOTH )
        self.nets_total = ""
        self.traces_total = ""
        self.vias_total = ""
        self.timer_interval = 2  # 定时器间隔时间（秒）

        self.main_panel.aLaunch.Bind(wx.EVT_BUTTON, self.Run)  
        self.main_panel.aCancel.Bind(wx.EVT_BUTTON, self.OnClose)
    

        self.part_details_data=[]
        self.init_UI()

    def init_UI(self):
        for k, v in parameters.items():
            self.part_details_data.append([v, " "])
        self.main_panel.update_data_view(self.part_details_data)



    def __del__( self ):
        pass


    # setup execution context
    def prepare(self):
        try:
            pcbnew.GetBoard().GetFileName()
            self.board = pcbnew.GetBoard()
        except Exception as e:
            for fp in (
                
                f"F:\demos\custom_pads_test\custom_pads_test.kicad_pcb",
                f"F:\demos\complex_hierarchy\complex_hierarchy.kicad_pcb",
                # f"F:\demos\sonde_xilinx\sonde_xilinx.kicad_pcb",
            ):
                if os.path.exists(fp):
                    self.board = pcbnew.LoadBoard(fp)


        self.dirpath, self.board_name = os.path.split(self.board.GetFileName())
        self.path_tuple = os.path.splitext(os.path.abspath(self.board.GetFileName()))
        self.board_prefix = self.path_tuple[0]

        config = configparser.ConfigParser()
        config_path = os.path.join(self.here_path, 'plugin.ini')
        config.read(config_path)

        # Convert dirpath to Path object
        self.dirpath = Path(self.dirpath)
        
        # Set temp filename using pathlib
        self.module_input = self.dirpath / 'freerouting.dsn'
        self.temp_input = self.dirpath / 'temp-freerouting.dsn'
        self.module_output = self.dirpath / 'freerouting.ses'
        self.module_rules = self.dirpath / 'freerouting.rules'
       
        # Remove previous temp files
        # try:
        #     os.remove(self.temp_input)
        # except:
        #     pass
        
        try:
            os.remove(self.module_output)
        except:
            pass
        
        try:
            os.remove(self.module_rules)
        except:
            pass
        
        # Create DSN file and remove java offending characters
        if not self.RunExport() :
            raise Exception("Failed to generate DSN file!")
        self.bFirstLine = True
        self.bEatNextLine = False
        fw = open(self.module_input, "w")
        fr = open(self.temp_input , "r", encoding="utf-8")
        for l in fr:
            if self.bFirstLine:
                fw.writelines('(pcb ' + self.module_input.name + '\n')
                self.bFirstLine = False
            elif self.bEatNextLine:
                self.bEatNextLine = l.rstrip()[-2:]!="))" 
                print(l)
                print(self.bEatNextLine)
                
            # Optional: remove one or both copper-pours before run freerouting 
            #elif l[:28] == "    (plane GND (polygon F.Cu":
            #    self.bEatNextLine = True
            #elif l[:28] == "    (plane GND (polygon B.Cu":
            #    self.bEatNextLine = True
            else:                                               
                fw.writelines(search_n_strip(l))
        fr.close()
        fw.close()
                        
    # export board.dsn file from pcbnew
    def RunExport(self):
        if self.SPECCTRA:
            ok = pcbnew.ExportSpecctraDSN( self.temp_input )
            if os.path.isfile(self.temp_input):
                return True
            if ok and os.path.isfile(self.temp_input):
                return True
            

            else:
                self.report_error("""
                Failed to invoke:
                 Failed to export DSN file
                """)
                return False
        else:
            return True

    def RunRouter(self):
        
        session_id = self.api_route.create_session()
        if session_id == "False":
            return False
        print(f"Session ID: {session_id}")
        # 排队任务
        random_integer = random.randint(10, 1000)
        random_name = str( random_integer ) + ".dsn"
        job_id = self.api_route.enqueue_job( session_id, random_name )
        if job_id == "False":
            return False
        
        status = self.api_route.settings_job( job_id )
        if status == "False":
            return False
        
        # 上传输入数据
        filename = os.path.basename(self.module_input)
        base64_data = file_to_base64(self.module_input)
        if base64_data:
            print("文件内容的Base64编码。")
        else:
            print("文件内容为空或无法读取。")
            return False
        status = self.api_route.upload_input(job_id, filename, base64_data)
        if status == "False":
            return False
        # 启动任务
        status = self.api_route.start_job(job_id)
        if status == "False":
            return False
        
        # 获取任务状态
        # status = self.api_route.get_job_status(job_id)
        # if status == "False":
        #     return False

        count = 20
        while True:
            time.sleep( self.timer_interval )
            count += ( 2 )
            if count < 85:
                self.main_panel.m_gauge.SetValue(count)
            content = self.api_route.get_job_status(job_id)
            print( f"计数：{count/3}" )

            if content == "False":
                return False
            if content['output'] ==None:
                continue
            status = content["state"]
            statistics = content['output']['statistics']
            self.nets_total = content['output']['statistics']['nets']['total_count']
            self.traces_total = content['output']['statistics']['traces']['total_count']
            self.vias_total = content['output']['statistics']['vias']['total_count']
            self.populate_part_list()
            
            if status == "COMPLETED":
                break
            time.sleep( self.timer_interval )

        # 获取任务输出
        ses_data = self.api_route.get_job_output(job_id)
        if ses_data == "False":
            return False
        self.main_panel.m_gauge.SetValue(90)
        self.dirpath.mkdir(parents=True, exist_ok=True)
        
        try:
            # 对 ses_data 进行 Base64 解码
            decoded_data = base64.b64decode(ses_data)
            
            # 打开文件并写入解码后的数据
            with open(self.module_output, 'wb') as file:  # 使用 'wb' 模式写入二进制数据
                file.write(decoded_data)
            print(f"解码后的数据已成功写入到 {self.module_output}")
            # os.remove(self.temp_input)

            self.RunImport()
            
            return True
        except Exception as e:
            print(f"写入文件时出错：{e}")
            return False
        



    def populate_part_list(self):
        self.part_details_data.clear()
        for k, v in parameters.items():
            if k == "nets_total":
                self.part_details_data.append([v, str( self.nets_total )])
            elif k == "traces_total":
                self.part_details_data.append([v, str( self.traces_total )])
            elif k == "vias_total":
                self.part_details_data.append([v, str( self.vias_total )])
        
        self.main_panel.update_data_view(self.part_details_data)


    # invoke chain of dependent methods
    def RunSteps(self):
        self.main_panel.m_gauge.SetValue(8)
        self.prepare()

        # if not self.RunRouter() :
        #     return

        # 在新线程中调用 RunRouter
        self.router_thread = threading.Thread(target=self.RunRouter)
        self.router_thread.start()



    # kicad plugin action entry
    def Run(self, event):
        if self.SPECCTRA:
            if has_pcbnew_api():
                self.RunSteps()
            else:
                self.report_error("""
                Missing required python API:
                 pcbnew.ExportSpecctraDSN
                 pcbnew.ImportSpecctraSES
                """)
        else:
            self.RunSteps()


    # import generated board.ses file into pcbnew
    def RunImport(self):
        if self.SPECCTRA:
            ok = pcbnew.ImportSpecctraSES(self.module_output)
            if ok and os.path.isfile(self.module_output):
                os.remove(self.module_input)
                os.remove(self.module_output)      
                
                self.main_panel.m_gauge.SetValue(100)
                wx.MessageBox(
                    _("Routing finish\r\n"),
                    _("Info"),
                    style=wx.ICON_INFORMATION,
                )
                self.Destroy()         
                return True
            else:
                self.report_error("""
                Failed to invoke:
                 Failed to import SES file
                """)
                return False
        else:
            return True
        
    def OnClose(self, evt):
        # self.api_route.cancel_job()
        self.Destroy()


    def report_error(self, reason):
        wx.MessageBox(
            _("Routing process failure:\r\n{reasons}\r\n").format(reasons=reason),
            _("Error"),
            style=wx.ICON_ERROR,
        )
        self.main_panel.m_gauge.SetValue(0)

