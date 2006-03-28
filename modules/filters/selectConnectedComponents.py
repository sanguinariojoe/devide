from moduleBase import moduleBase
from moduleMixins import scriptedConfigModuleMixin
import moduleUtils
import vtk
import vtkdevide
from module_kits.vtk_kit.mixins import VTKErrorFuncMixin

class selectConnectedComponents(scriptedConfigModuleMixin, moduleBase,
                                VTKErrorFuncMixin):
    """3D region growing.

    Finds all points connected to the seed points that have the same values
    as at the seed points.  This is primarily useful for selecting connected
    components.
    """

    def __init__(self, moduleManager):

        # call parent constructor
        moduleBase.__init__(self, moduleManager)

        self._imageCast = vtk.vtkImageCast()
        self._imageCast.SetOutputScalarTypeToUnsignedLong()
        self._selectccs = vtkdevide.vtkSelectConnectedComponents()
        self._selectccs.SetInput(self._imageCast.GetOutput())

        moduleUtils.setupVTKObjectProgress(self, self._selectccs,
                                           'Marking selected components')
        self.add_vtk_error_handler(self._selectccs)
        
        moduleUtils.setupVTKObjectProgress(self, self._imageCast,
                                           'Casting data to unsigned long')
        self.add_vtk_error_handler(self._imageCast)
        
        # we'll use this to keep a binding (reference) to the passed object
        self._inputPoints = None
        # this will be our internal list of points
        self._seedPoints = []

        # now setup some defaults before our sync
        self._config.outputConnectedValue = 1
        self._config.outputUnconnectedValue = 0

        configList = [
            ('Output Connected Value:', 'outputConnectedValue', 'base:int',
             'text', 'This value will be assigned to all points in the '
             'selected connected components.'),
            ('Output Unconnected Value:', 'outputUnconnectedValue', 'base:int',
             'text', 'This value will be assigned to all points NOT in the '
             'selected connected components.')
            ]

        scriptedConfigModuleMixin.__init__(self, configList)
        
        self._viewFrame = self._createViewFrame(
            {'Module (self)' : self,
             'vtkImageCast' : self._imageCast,
             'vtkSelectConnectedComponents' : self._selectccs})
           

        self.configToLogic()
        self.logicToConfig()
        self.configToView()

    def close(self):
        # we play it safe... (the graph_editor/module_manager should have
        # disconnected us by now)
        for inputIdx in range(len(self.getInputDescriptions())):
            self.setInput(inputIdx, None)

        # this will take care of all display thingies
        scriptedConfigModuleMixin.close(self)

        moduleBase.close(self)

        # get rid of our reference
        del self._imageCast
        del self._selectccs

    def getInputDescriptions(self):
        return ('VTK Connected Components (unsigned long)', 'Seed points')
    
    def setInput(self, idx, inputStream):
        if idx == 0:
            # will work for None and not-None
            self._imageCast.SetInput(inputStream)
            
        else:
            if inputStream != self._inputPoints:
                self._inputPoints = inputStream
    
    def getOutputDescriptions(self):
        return ('Selected connected components (vtkImageData)',)
    
    def getOutput(self, idx):
        return self._selectccs.GetOutput()

    def logicToConfig(self):
        self._config.outputConnectedValue = self._selectccs.\
                                            GetOutputConnectedValue()
        self._config.outputUnconnectedValue = self._selectccs.\
                                              GetOutputUnconnectedValue()

    def configToLogic(self):
        self._selectccs.SetOutputConnectedValue(self._config.\
                                                outputConnectedValue)
        self._selectccs.SetOutputUnconnectedValue(self._config.\
                                                  outputUnconnectedValue)

    def executeModule(self):
        self._sync_to_input_points()

        self._imageCast.Update()
        self.check_vtk_error()
        
        self._selectccs.Update()
        self.check_vtk_error()

    def _sync_to_input_points(self):
        # extract a list from the input points
        tempList = []
        if self._inputPoints:
            for i in self._inputPoints:
                tempList.append(i['discrete'])

        if tempList != self._seedPoints:
            self._seedPoints = tempList

            self._selectccs.RemoveAllSeeds()
            # we need to call Modified() explicitly as RemoveAllSeeds()
            # doesn't.  AddSeed() does, but sometimes the list is empty at
            # this stage and AddSeed() isn't called.
            self._selectccs.Modified()
            
            for seedPoint in self._seedPoints:
                self._selectccs.AddSeed(seedPoint[0], seedPoint[1],
                                        seedPoint[2])



