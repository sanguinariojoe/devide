#!/usr/bin/env python
# generated by wxGlade 0.3.1 on Tue Sep 30 00:10:24 2003

from wxPython.wx import *
from wxPython.html import *

class htmlWindowFrame(wxFrame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: htmlWindowFrame.__init__
        kwds["style"] = wxDEFAULT_FRAME_STYLE
        wxFrame.__init__(self, *args, **kwds)
        self.panel_1 = wxPanel(self, -1)
        self.htmlWindow = wxHtmlWindow(self.panel_1, -1)
        self.closeButtonId  =  wxNewId()
        self.closeButton = wxButton(self.panel_1, self.closeButtonId , "Close")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: htmlWindowFrame.__set_properties
        self.SetTitle("frame_1")
        self.SetSize((400, 400))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: htmlWindowFrame.__do_layout
        sizer_1 = wxBoxSizer(wxVERTICAL)
        sizer_2 = wxBoxSizer(wxVERTICAL)
        sizer_3 = wxBoxSizer(wxVERTICAL)
        sizer_3.Add(self.htmlWindow, 1, wxEXPAND, 0)
        sizer_3.Add(self.closeButton, 0, wxTOP|wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 7)
        sizer_2.Add(sizer_3, 1, wxALL|wxEXPAND, 7)
        self.panel_1.SetAutoLayout(1)
        self.panel_1.SetSizer(sizer_2)
        sizer_2.Fit(self.panel_1)
        sizer_2.SetSizeHints(self.panel_1)
        sizer_1.Add(self.panel_1, 1, wxEXPAND, 0)
        self.SetAutoLayout(1)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

# end of class htmlWindowFrame

