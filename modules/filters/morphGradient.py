import gen_utils
from module_base import ModuleBase
from module_mixins import ScriptedConfigModuleMixin
import module_utils
import vtk

class morphGradient(ScriptedConfigModuleMixin, ModuleBase):
    def __init__(self, module_manager):
        # initialise our base class
        ModuleBase.__init__(self, module_manager)

        # main morph gradient
        self._imageDilate = vtk.vtkImageContinuousDilate3D()
        self._imageErode = vtk.vtkImageContinuousErode3D()
        self._imageMath = vtk.vtkImageMathematics()
        self._imageMath.SetOperationToSubtract()

        self._imageMath.SetInput1(self._imageDilate.GetOutput())
        self._imageMath.SetInput2(self._imageErode.GetOutput())

        # inner gradient
        self._innerImageMath = vtk.vtkImageMathematics()
        self._innerImageMath.SetOperationToSubtract()
        self._innerImageMath.SetInput1(None) # has to take image
        self._innerImageMath.SetInput2(self._imageErode.GetOutput())

        # outer gradient
        self._outerImageMath = vtk.vtkImageMathematics()
        self._outerImageMath.SetOperationToSubtract()
        self._outerImageMath.SetInput1(self._imageDilate.GetOutput()) 
        self._outerImageMath.SetInput2(None) # has to take image
        
        
        module_utils.setup_vtk_object_progress(self, self._imageDilate,
                                           'Performing greyscale 3D dilation')
        

        module_utils.setup_vtk_object_progress(self, self._imageErode,
                                           'Performing greyscale 3D erosion')
        

        module_utils.setup_vtk_object_progress(self, self._imageMath,
                                           'Subtracting erosion from '
                                           'dilation')
        

        module_utils.setup_vtk_object_progress(self, self._innerImageMath,
                                           'Subtracting erosion from '
                                           'image (inner)')
        

        module_utils.setup_vtk_object_progress(self, self._outerImageMath,
                                           'Subtracting image from '
                                           'dilation (outer)')
        
                                           
        self._config.kernelSize = (3, 3, 3)


        configList = [
            ('Kernel size:', 'kernelSize', 'tuple:int,3', 'text',
             'Size of the kernel in x,y,z dimensions.')]
        ScriptedConfigModuleMixin.__init__(
            self, configList,
            {'Module (self)' : self,
             'vtkImageContinuousDilate3D' : self._imageDilate,
             'vtkImageContinuousErode3D' : self._imageErode,
             'vtkImageMathematics' : self._imageMath})

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
        del self._imageDilate
        del self._imageErode
        del self._imageMath

    def get_input_descriptions(self):
        return ('vtkImageData',)

    def set_input(self, idx, inputStream):
        self._imageDilate.SetInput(inputStream)
        self._imageErode.SetInput(inputStream)
        self._innerImageMath.SetInput1(inputStream)
        self._outerImageMath.SetInput2(inputStream)

    def get_output_descriptions(self):
        return ('Morphological gradient (vtkImageData)',
                'Morphological inner gradient (vtkImageData)',
                'Morphological outer gradient (vtkImageData)')

    def get_output(self, idx):
        if idx == 0:
            return self._imageMath.GetOutput()
        if idx == 1:
            return self._innerImageMath.GetOutput()
        else:
            return self._outerImageMath.GetOutput()

    def logic_to_config(self):
        # if the user's futzing around, she knows what she's doing...
        # (we assume that the dilate/erode pair are in sync)
        self._config.kernelSize = self._imageDilate.GetKernelSize()
    
    def config_to_logic(self):
        ks = self._config.kernelSize
        self._imageDilate.SetKernelSize(ks[0], ks[1], ks[2])
        self._imageErode.SetKernelSize(ks[0], ks[1], ks[2])
    
    def execute_module(self):
        # we only execute the main gradient
        self._imageMath.Update()
        


