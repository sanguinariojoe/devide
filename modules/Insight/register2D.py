from genMixins import subjectMixin, updateCallsExecuteModuleMixin
from moduleBase import moduleBase
import moduleUtils
import InsightToolkit as itk
import ConnectVTKITKPython as CVIPy
import vtk
import wx

class transformStackClass(list,
                          subjectMixin,
                          updateCallsExecuteModuleMixin):
    
    def __init__(self, d3Module):
        # call base ctors
        subjectMixin.__init__(self)
        updateCallsExecuteModuleMixin.__init__(self, d3Module)

    def close(self):
        subjectMixin.close(self)
        updateCallsExecuteModuleMixin.close(self)

class register2D(moduleBase):
    """Registers a stack of 2D images and generates a list of transforms.

    This is BAD-ASSED CODE(tm) and can crash the whole of DSCAS3 without
    even saying sorry afterwards.  You have been warned.
    """

    def __init__(self, moduleManager):
        moduleBase.__init__(self, moduleManager)

        # input
        self._imageStack = None
        # output is a transform stack
        self._transformStack = transformStackClass(self)

        self._createViewFrames()
        self._bindEvents()

        # FIXME: add current transforms to config stuff

    def close(self):
        moduleBase.close(self)

        # take care of pipeline thingies
        del self._rescaler1
        del self._itkExporter1
        del self._vtkImporter1

        del self._rescaler2
        del self._itkExporter2
        del self._vtkImporter2

        # nasty trick to take care of RenderWindow
        self._threedRenderer.RemoveAllProps()
        del self._threedRenderer
        self.viewerFrame.threedRWI.GetRenderWindow().WindowRemap()
        self.viewerFrame.Destroy()
        del self.viewerFrame
        
        # then do the controlFrame
        self.controlFrame.Destroy()
        del self.controlFrame

    def getInputDescriptions(self):
        return ('ITK Image Stack',)

    def setInput(self, idx, inputStream):
        # FIXME: also check for correct type!
        if inputStream != self._imageStack:
            # let's setup for a new stack!
            self._imageStack = inputStream
            self._showImagePair(1)
        
    def getOutputDescriptions(self):
        return ('2D Transform Stack',)

    def getOutput(self, idx):
        return self._transformStack

    def executeModule(self):
        pass

    def view(self, parent_window=None):
        # if the window is already visible, raise it
        if not self.viewerFrame.Show(True):
            self.viewerFrame.Raise()

        if not self.controlFrame.Show(True):
            self.controlFrame.Raise()

    # ----------------------------------------------------------------------
    # non-API methods start here -------------------------------------------
    # ----------------------------------------------------------------------

    def _bindEvents(self):
        pass
    
    def _createViewFrames(self):
        import modules.Insight.resources.python.register2DViewFrames
        reload(modules.Insight.resources.python.register2DViewFrames)

        viewerFrame = modules.Insight.resources.python.register2DViewFrames.\
                      viewerFrame
        self.viewerFrame = moduleUtils.instantiateModuleViewFrame(
            self, self._moduleManager, viewerFrame)

        self._threedRenderer = vtk.vtkRenderer()
        self._threedRenderer.SetBackground(0.5, 0.5, 0.5)
        self.viewerFrame.threedRWI.GetRenderWindow().AddRenderer(
            self._threedRenderer)
        

        # we need to have two converters from itk::Image to vtkImageData,
        # hmmmm kay?

        self._rescaler1 = itk.itkRescaleIntensityImageFilterF2UC2_New()
        self._rescaler1.SetOutputMinimum(0)
        self._rescaler1.SetOutputMaximum(255)
        self._itkExporter1 = itk.itkVTKImageExportUC2_New()
        self._itkExporter1.SetInput(self._rescaler1.GetOutput())
        self._vtkImporter1 = vtk.vtkImageImport()
        CVIPy.ConnectITKUC2ToVTK(self._itkExporter1.GetPointer(),
                                self._vtkImporter1)
        
        self._rescaler2 = itk.itkRescaleIntensityImageFilterF2UC2_New()
        self._rescaler2.SetOutputMinimum(0)
        self._rescaler2.SetOutputMaximum(255)
        self._itkExporter2 = itk.itkVTKImageExportUC2_New()
        self._itkExporter2.SetInput(self._rescaler2.GetOutput())
        self._vtkImporter2 = vtk.vtkImageImport()
        CVIPy.ConnectITKUC2ToVTK(self._itkExporter2.GetPointer(),
                                self._vtkImporter2)
        

        # controlFrame creation
        controlFrame = modules.Insight.resources.python.\
                       register2DViewFrames.controlFrame
        self.controlFrame = moduleUtils.instantiateModuleViewFrame(
            self, self._moduleManager, controlFrame)

        # display
        self.viewerFrame.Show(True)
        self.controlFrame.Show(True)
        
    def _showImagePair(self, pairNumber):
        """Set everything up to have the user interact with image pair
        pairNumber.

        pairNumber is 1 based, i.e. pairNumber 1 implies the registration
        between image 1 and image 0.
        """


        try:
            self._imageStack.Update()
            assert(len(self._imageStack) >= 2)
        except Exception:
            # if the Update call doesn't work or
            # if the input list is not long enough (or unsizable),
            # we don't do anything
            return
        

        self._rescaler1.SetInput(self._imageStack[0])
        self._rescaler1.Update() # give ITK a chance to complain...
        self._rescaler2.SetInput(self._imageStack[1])
        self._rescaler2.Update() # give ITK a chance to complain...

#        checker = vtk.vtkImageCheckerboard()
#        checker.SetNumberOfDivisions(10, 10, 1)
#        checker.SetInput1(self._vtkImporter1.GetOutput())
#        checker.SetInput2(self._vtkImporter2.GetOutput())

        self._ipw1 = vtk.vtkImagePlaneWidget()
        self._vtkImporter1.Update()
        self._ipw1.SetInput(self._vtkImporter1.GetOutput())
        self._ipw1.SetPlaneOrientation(2)        
        self._ipw1.SetInteractor(self.viewerFrame.threedRWI)
        self._ipw1.On()
        

        #self._imageViewer.SetInput(self._vtkImporter1.GetOutput())

        self.viewerFrame.threedRWI.GetRenderWindow().Render()