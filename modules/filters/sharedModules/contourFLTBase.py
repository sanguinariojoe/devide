from moduleBase import moduleBase
from moduleMixins import vtkPipelineConfigModuleMixin
import moduleUtils
import vtk

class contourFLTBase(moduleBase, vtkPipelineConfigModuleMixin):

    def __init__(self, moduleManager, contourFilterText):

        # call parent constructor
        moduleBase.__init__(self, moduleManager)

        self._contourFilterText = contourFilterText
        if contourFilterText == 'marchingCubes':
            self._contourFilter = vtk.vtkMarchingCubes()
        else: # contourFilter == 'contourFilter'
            self._contourFilter = vtk.vtkContourFilter()

        moduleUtils.setupVTKObjectProgress(self, self._contourFilter,
                                           'Extracting iso-surface')

        # now setup some defaults before our sync
        self._config.isoValue = 128;

        self._viewFrame = None
        self._createViewFrame()

        # transfer these defaults to the logic
        self.configToLogic()

        # then make sure they come all the way back up via self._config
        self.logicToConfig()
        self.configToView()

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
        
    def configToView(self):
        self._viewFrame.isoValueText.SetValue(str(self._config.isoValue))

    def executeModule(self):
        self._contourFilter.Update()

    def view(self, parent_window=None):
        # if the window was visible already. just raise it
        if not self._viewFrame.Show(True):
            self._viewFrame.Raise()

    def _createViewFrame(self):

        # import the viewFrame (created with wxGlade)
        import modules.Filters.resources.python.contourFLTBaseViewFrame
        reload(modules.Filters.resources.python.contourFLTBaseViewFrame)

        self._viewFrame = moduleUtils.instantiateModuleViewFrame(
            self, self._moduleManager,
            modules.Filters.resources.python.contourFLTBaseViewFrame.\
            contourFLTBaseViewFrame)

        objectDict = {'contourFilter' : self._contourFilter}
        moduleUtils.createStandardObjectAndPipelineIntrospection(
            self, self._viewFrame, self._viewFrame.viewFramePanel,
            objectDict, None)

        moduleUtils.createECASButtons(
            self, self._viewFrame, self._viewFrame.viewFramePanel)
            