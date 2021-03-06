#!/usr/bin/env python
# -*- coding: ansi_x3.4-1968 -*-
# generated by wxGlade 0.6.3 on Sat Feb 09 13:36:33 2008

import wx

# begin wxGlade: extracode
# end wxGlade



class resampleImageViewFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: resampleImageViewFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.viewFramePanel = wx.Panel(self, -1)
        self.label_1 = wx.StaticText(self.viewFramePanel, -1, "Interpolation type:")
        self.interpolationTypeChoice = wx.Choice(self.viewFramePanel, -1, choices=["Nearest Neighbour", "Linear", "Cubic"])
        self.label_2 = wx.StaticText(self.viewFramePanel, -1, "x,y,z Magnification:")
        self.magFactorXText = wx.TextCtrl(self.viewFramePanel, -1, "")
        self.label_3 = wx.StaticText(self.viewFramePanel, -1, ",")
        self.magFactorYText = wx.TextCtrl(self.viewFramePanel, -1, "")
        self.label_4 = wx.StaticText(self.viewFramePanel, -1, ",")
        self.magFactorZText = wx.TextCtrl(self.viewFramePanel, -1, "")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: resampleImageViewFrame.__set_properties
        self.SetTitle("frame_1")
        self.interpolationTypeChoice.SetSelection(0)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: resampleImageViewFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4.Add(self.label_1, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 3)
        sizer_4.Add(self.interpolationTypeChoice, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_3.Add(sizer_4, 1, wx.BOTTOM|wx.EXPAND, 7)
        sizer_5.Add(self.label_2, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 3)
        sizer_5.Add(self.magFactorXText, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 3)
        sizer_5.Add(self.label_3, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 3)
        sizer_5.Add(self.magFactorYText, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 3)
        sizer_5.Add(self.label_4, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 3)
        sizer_5.Add(self.magFactorZText, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_3.Add(sizer_5, 1, wx.EXPAND, 0)
        sizer_2.Add(sizer_3, 1, wx.ALL|wx.EXPAND, 7)
        self.viewFramePanel.SetSizer(sizer_2)
        sizer_1.Add(self.viewFramePanel, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

# end of class resampleImageViewFrame


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = resampleImageViewFrame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
