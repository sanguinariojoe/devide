#!/usr/bin/env python
# generated by wxGlade 0.3.2pre2 on Fri Feb 27 16:13:31 2004

import wx

class defaultModuleViewFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: defaultModuleViewFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.viewFramePanel = wx.Panel(self, -1)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: defaultModuleViewFrame.__set_properties
        self.SetTitle("frame_1")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: defaultModuleViewFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        self.viewFramePanel.SetSizer(sizer_2)
        sizer_1.Add(self.viewFramePanel, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

# end of class defaultModuleViewFrame


