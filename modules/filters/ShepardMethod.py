from moduleBase import moduleBase
from moduleMixins import scriptedConfigModuleMixin
import moduleUtils
import vtk


class ShephardMethod(scriptedConfigModuleMixin, moduleBase):

    """Apply Shepard Method to input.
    
    """
    
    def __init__(self, moduleManager):
        # initialise our base class
        moduleBase.__init__(self, moduleManager)


        self._shepardFilter = vtk.vtkShepardMethod()
        
        moduleUtils.setupVTKObjectProgress(self, self._shepardFilter,
                                           'Applying Shepard Method.')
        
                                           
        self._config.maximum_distance = 1.0
        
                                           
                                           

        configList = [
            ('Kernel size:', 'kernelSize', 'tuple:int,3', 'text',
             'Size of the kernel in x,y,z dimensions.')]
        scriptedConfigModuleMixin.__init__(self, configList)        
        

        self._viewFrame = self._createWindow(
            {'Module (self)' : self,
             'vtkImageContinuousDilate3D' : self._imageDilate})

        # pass the data down to the underlying logic
        self.config_to_logic()
        # and all the way up from logic -> config -> view to make sure
        self.logic_to_config()
        self.config_to_view()

    def close(self):
        # we play it safe... (the graph_editor/module_manager should have
        # disconnected us by now)
        for inputIdx in range(len(self.get_input_descriptions())):
            self.set_input(inputIdx, None)

        # this will take care of all display thingies
        scriptedConfigModuleMixin.close(self)

        moduleBase.close(self)
        
        # get rid of our reference
        del self._imageDilate

    def get_input_descriptions(self):
        return ('vtkImageData',)

    def set_input(self, idx, inputStream):
        self._imageDilate.SetInput(inputStream)

    def get_output_descriptions(self):
        return (self._imageDilate.GetOutput().GetClassName(), )

    def get_output(self, idx):
        return self._imageDilate.GetOutput()

    def logic_to_config(self):
        self._config.kernelSize = self._imageDilate.GetKernelSize()
    
    def config_to_logic(self):
        ks = self._config.kernelSize
        self._imageDilate.SetKernelSize(ks[0], ks[1], ks[2])
    
    def execute_module(self):
        self._imageDilate.Update()
        

    def view(self, parent_window=None):
        # if the window was visible already. just raise it
        self._viewFrame.Show(True)
        self._viewFrame.Raise()


