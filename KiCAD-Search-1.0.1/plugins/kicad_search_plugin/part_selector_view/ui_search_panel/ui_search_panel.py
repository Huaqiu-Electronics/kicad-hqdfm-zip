# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.0.0-0-g0efcecf)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc


###########################################################################
## Class UiSearchPanel
###########################################################################

class UiSearchPanel ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 711,39 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer7 = wx.BoxSizer( wx.VERTICAL )

		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

		self.description = wx.SearchCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TE_PROCESS_ENTER )
		self.description.ShowSearchButton( True )
		self.description.ShowCancelButton( False )
		bSizer9.Add( self.description, 1, wx.ALIGN_TOP|wx.EXPAND, 5 )


		bSizer9.Add( ( 10, 0), 0, wx.EXPAND, 0 )

		self.search_button = wx.Button( self, wx.ID_ANY, _(u"Search"), wx.DefaultPosition, wx.Size( 100,28 ), 0 )
		bSizer9.Add( self.search_button, 0, wx.ALIGN_CENTER|wx.RIGHT, 1 )


		bSizer7.Add( bSizer9, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer7 )
		self.Layout()

	def __del__( self ):
		pass


