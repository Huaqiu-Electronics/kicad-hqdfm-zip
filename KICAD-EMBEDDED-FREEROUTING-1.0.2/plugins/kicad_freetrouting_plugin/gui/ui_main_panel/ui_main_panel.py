# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

###########################################################################
## Class UiMainPanel
###########################################################################

class UiMainPanel ( wx.Panel ):

    def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

        sizer = wx.BoxSizer( wx.VERTICAL )

        self.text = wx.StaticText( self, wx.ID_ANY, _(u"Launch or Cancel Freerouting"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.text.Wrap( -1 )

        sizer.Add( self.text, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 10 )

        self.line = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        sizer.Add( self.line, 0, wx.EXPAND |wx.ALL, 5 )

        bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

        self.aLaunch = wx.Button( self, wx.ID_ANY, _(u"Launch"), wx.DefaultPosition, wx.DefaultSize, 0 )

        self.aLaunch.SetDefault()
        bSizer3.Add( self.aLaunch, 0, wx.ALL, 5 )


        bSizer3.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.aCancel = wx.Button( self, wx.ID_ANY, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer3.Add( self.aCancel, 0, wx.ALL, 5 )


        sizer.Add( bSizer3, 1, wx.EXPAND, 5 )


        sizer.Add( ( 0, 0), 0, wx.EXPAND, 10 )

        self.m_gauge = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.m_gauge.SetValue( 0 )
        sizer.Add( self.m_gauge, 0, wx.ALL|wx.EXPAND, 5 )


        sizer.Add( ( 0, 0), 0, wx.EXPAND, 10 )

        sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"Tips") ), wx.VERTICAL )

        self.aDataView = wx.dataview.DataViewListCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_ROW_LINES )
        self.aDataView.SetMinSize( wx.Size( -1,100 ) )

        sbSizer1.Add( self.aDataView, 1, wx.ALL|wx.EXPAND, 5 )


        sizer.Add( sbSizer1, 2, wx.ALL|wx.EXPAND, 5 )


        self.SetSizer( sizer )
        self.Layout()
        sizer.Fit( self )

        # Connect Events
        self.aLaunch.Bind( wx.EVT_BUTTON, self.bttn_on_click )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def bttn_on_click( self, event ):
        event.Skip()


