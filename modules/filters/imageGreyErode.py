import gen_utils
from module_base import ModuleBase
from module_mixins import ScriptedConfigModuleMixin
import module_utils
import vtk


class imageGreyErode(ScriptedConfigModuleMixin, ModuleBase):

    def __init__(self, module_manager):
        # initialise our base class
        ModuleBase.__init__(self, module_manager)


        self._imageErode = vtk.vtkImageContinuousErode3D()
        
        module_utils.setup_vtk_object_progress(self, self._imageErode,
                                           'Performing greyscale 3D erosion')
        
                                           
        self._config.kernelSize = (3, 3, 3)


        configList = [
            ('Kernel size:', 'kernelSize', 'tuple:int,3', 'text',
             'Size of the kernel in x,y,z dimensions.')]
        ScriptedConfigModuleMixin.__init__(
            self, configList,
            {'Module (self)' : self,
             'vtkImageContinuousErode3D' : self._imageErode})

        self.sync_module_logic_with_config()
        
    def close(self):
        # we play it safe... (the graph_editor/module_manager should have
        # disconnected us by now)
        for input_idx in range(len(self.get_input_descriptions())):
            self.set_input(input_idx, None)

        # this will take care of all display thingies
        ScriptedConfigModuleMixin.close(self)

        ModuleBase.close(self)
        
        # get rid of our reference
        del self._imageErode

    def get_input_descriptions(self):
        return ('vtkImageData',)

    def set_input(self, idx, inputStream):
        self._imageErode.SetInput(inputStream)

    def get_output_descriptions(self):
        return (self._imageErode.GetOutput().GetClassName(), )

    def get_output(self, idx):
        return self._imageErode.GetOutput()

    def logic_to_config(self):
        self._config.kernelSize = self._imageErode.GetKernelSize()
    
    def config_to_logic(self):
        ks = self._config.kernelSize
        self._imageErode.SetKernelSize(ks[0], ks[1], ks[2])
    
    def execute_module(self):
        self._imageErode.Update()
 
    def streaming_execute_module(self):
        self._imageErode.Update()
       
