import wx
import wx.xrc


from .ui_search_panel import UiSearchPanel



class SearchView(UiSearchPanel):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        super().__init__(parent, id=id, pos=pos, size=size, style=style, name=name)

        self.description.SetHint("e.g:22pF C_Disc_D3.0mm_W2.0mm_P2.50mm")