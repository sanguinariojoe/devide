#!/usr/bin/env python
# generated by wxGlade 0.2.1cvs on Wed Jan 22 15:57:42 2003

from wxPython.wx import *

class filenameViewModuleMixinFrame(wxFrame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: filenameViewModuleMixinFrame.__init__
        kwds["style"] = wxCAPTION|wxMINIMIZE_BOX|wxMAXIMIZE_BOX|wxSYSTEM_MENU|wxRESIZE_BORDER
        wxFrame.__init__(self, *args, **kwds)
        self.label_8 = wxStaticText(self, -1, "Filename")
        self.filenameText = wxTextCtrl(self, -1, "")
        self.browseButtonId  =  wxNewId()
        self.browseButton = wxButton(self, self.browseButtonId , "Browse")
        self.label_1 = wxStaticText(self, -1, "Examine the")
        self.objectChoiceId  =  wxNewId()
        self.objectChoice = wxChoice(self, self.objectChoiceId , choices=["vtkMarchingCubes"])
        self.label_2 = wxStaticText(self, -1, "or")
        self.pipelineButtonId  =  wxNewId()
        self.pipelineButton = wxButton(self, self.pipelineButtonId , "Pipeline")
        self.cancel_button = wxButton(self, wxID_CANCEL, "Cancel")
        self.SYNC_ID  =  wxNewId()
        self.sync_button = wxButton(self, self.SYNC_ID , "Sync")
        self.APPLY_ID  =  wxNewId()
        self.apply_button = wxButton(self, self.APPLY_ID , "Apply")
        self.EXECUTE_ID  =  wxNewId()
        self.execute_button = wxButton(self, self.EXECUTE_ID , "Execute")
        self.ok_button = wxButton(self, wxID_OK, "OK")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: filenameViewModuleMixinFrame.__set_properties
        self.SetTitle("SomeModule")
        self.objectChoice.SetSelection(0)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: filenameViewModuleMixinFrame.__do_layout
        sizer_1 = wxBoxSizer(wxVERTICAL)
        sizer_2 = wxBoxSizer(wxHORIZONTAL)
        sizer_4 = wxBoxSizer(wxHORIZONTAL)
        sizer_3 = wxBoxSizer(wxHORIZONTAL)
        sizer_3.Add(self.label_8, 0, wxLEFT|wxRIGHT|wxALIGN_CENTER_VERTICAL, 2)
        sizer_3.Add(self.filenameText, 1, 0, 0)
        sizer_3.Add(self.browseButton, 0, 0, 0)
        sizer_1.Add(sizer_3, 1, wxALL|wxEXPAND, 5)
        sizer_4.Add(self.label_1, 0, wxLEFT|wxRIGHT|wxALIGN_CENTER_VERTICAL, 2)
        sizer_4.Add(self.objectChoice, 0, wxALIGN_CENTER_VERTICAL, 0)
        sizer_4.Add(self.label_2, 0, wxLEFT|wxRIGHT|wxALIGN_CENTER_VERTICAL, 2)
        sizer_4.Add(self.pipelineButton, 0, wxALIGN_CENTER_VERTICAL, 0)
        sizer_1.Add(sizer_4, 1, wxALL|wxEXPAND, 5)
        sizer_2.Add(self.cancel_button, 0, wxALL, 2)
        sizer_2.Add(self.sync_button, 0, wxALL, 2)
        sizer_2.Add(self.apply_button, 0, wxALL, 2)
        sizer_2.Add(self.execute_button, 0, wxALL, 2)
        sizer_2.Add(self.ok_button, 0, wxALL, 2)
        sizer_1.Add(sizer_2, 0, wxALL, 5)
        self.SetAutoLayout(1)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        sizer_1.SetSizeHints(self)
        self.Layout()
        # end wxGlade

# end of class filenameViewModuleMixinFrame


