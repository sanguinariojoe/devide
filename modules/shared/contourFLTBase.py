import genUtils
from moduleBase import moduleBase
from moduleMixins import vtkPipelineConfigModuleMixin
import moduleUtils
from wxPython.wx import *
import vtk

class contourFLTBase(moduleBase, vtkPipelineConfigModuleMixin):

    def __init__(self, moduleManager, contourFilterText):

        # call parent constructor
        moduleBase.__init__(self, moduleManager)

        self._contourFilterText = contourFilterText
        if contourFilterText == 'marchingCubes':
            self._contourFilter = vtk.vtkMarchingCubes()
        else: # contourFilter == 'contourFilter'
            self._contourFilter = vtk.vtkKitwareContourFilter()

        # following is the standard way of connecting up the dscas3 progress
        # callback to a VTK object; you should do this for all objects in
        # your module - you could do this in __init__ as well, it seems
        # neater here though
        self._contourFilter.SetProgressText('Extracting iso-surface')
        mm = self._moduleManager
        self._contourFilter.SetProgressMethod(lambda s=self, mm=mm:
                                               mm.vtk_progress_cb(
            s._contourFilter))
        

        # now setup some defaults before our sync
        self._config.isoValue = 128;
        self._config.rtu = 0

        self._viewFrame = None
        self._createViewFrame()

        # transfer these defaults to the logic
        self.configToLogic()

        # then make sure they come all the way back up via self._config
        self.syncViewWithLogic()

    def close(self):
        # we play it safe... (the graph_editor/module_manager should have
        # disconnected us by now)
        self.setInput(0, None)
        # don't forget to call the close() method of the vtkPipeline mixin
        vtkPipelineConfigModuleMixin.close(self)
        # take out our view interface
        self._viewFrame.Destroy()
        # get rid of our reference
        del self._contourFilter

    def getInputDescriptions(self):
	return ('vtkImageData',)
    

    def setInput(self, idx, inputStream):
        self._contourFilter.SetInput(inputStream)

    def getOutputDescriptions(self):
	return (self._contourFilter.GetOutput().GetClassName(),)
    

    def getOutput(self, idx):
        return self._contourFilter.GetOutput()

    def logicToConfig(self):
        self._config.isoValue = self._contourFilter.GetValue(0)

    def configToLogic(self):
        self._contourFilter.SetValue(0, self._config.isoValue)

    def viewToConfig(self):
        try:
            self._config.isoValue = float(
                self._viewFrame.isoValueText.GetValue())
        except:
            pass
        
        self._config.rtu = self._viewFrame.realtimeUpdateCheckBox.GetValue()

    def configToView(self):
        self._viewFrame.isoValueText.SetValue(str(self._config.isoValue))
        self._viewFrame.realtimeUpdateCheckBox.SetValue(self._config.rtu)

    def executeModule(self):
        self._contourFilter.Update()

        # tell the vtk log file window to poll the file; if the file has
        # changed, i.e. vtk has written some errors, the log window will
        # pop up.  you should do this in all your modules right after you
        # caused some VTK processing which might have resulted in VTK
        # outputting to the error log
        self._moduleManager.vtk_poll_error()

    def view(self, parent_window=None):
        # if the window was visible already. just raise it
        if not self._viewFrame.Show(True):
            self._viewFrame.Raise()

    def _createViewFrame(self):

        # import the viewFrame (created with wxGlade)
        import modules.resources.python.contourFLTBaseViewFrame
        reload(modules.resources.python.contourFLTBaseViewFrame)

        # find our parent window and instantiate the frame
        pw = self._moduleManager.get_module_view_parent_window()
        self._viewFrame = modules.resources.python.contourFLTBaseViewFrame.\
                          contourFLTBaseViewFrame(pw, -1, 'dummy')

        self._viewFrame.objectChoice.Clear()
        self._viewFrame.objectChoice.Append(self._contourFilter.GetClassName())
        self._viewFrame.objectChoice.SetSelection(0)
        self._viewFrame.SetTitle('%s View' % (self._contourFilterText))

        # make sure that a close of that window does the right thing
        EVT_CLOSE(self._viewFrame,
                  lambda e, s=self: s._viewFrame.Show(False))

        # default binding for the buttons at the bottom
        moduleUtils.bindCSAEO(self, self._viewFrame)        

        # connect slider to its callback for instant processing
        EVT_TEXT_ENTER(self._viewFrame,
                       self._viewFrame.isoValueTextId,
                       self._isoTextCallback)

        # the checkbox should directly modify its own bit of the self._config
        EVT_CHECKBOX(self._viewFrame,
                     self._viewFrame.realtimeUpdateCheckBoxId,
                     self._realtimeUpdateCheckBoxCallback)

        # and now the standard examine object/pipeline stuff
        EVT_CHOICE(self._viewFrame, self._viewFrame.objectChoiceId,
                   self.vtkObjectChoiceCallback)
        EVT_BUTTON(self._viewFrame, self._viewFrame.pipelineButtonId,
                   self.vtkPipelineCallback)
        
    def _isoTextCallback(self):
        if self._config.rtu:
            self.applyViewToLogic()
            self.executeModule()

    def _realtimeUpdateCheckBoxCallback(self, event):
        self._config.rtu = self._viewFrame.realtimeUpdateCheckBox.GetValue()
        

    def vtkObjectChoiceCallback(self, event):
        self.vtkObjectConfigure(self._viewFrame, None,
                                self._contourFilter)

    def vtkPipelineCallback(self, event):
        # move this to module utils too, or to base...
        self.vtkPipelineConfigure(self._viewFrame, None,
                                  (self._contourFilter,))
