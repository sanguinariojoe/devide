# class generated by DeVIDE::createDeVIDEModuleFromVTKObject
from module_kits.vtk_kit.mixins import SimpleVTKClassModuleBase
import vtk

class vtkExtractVectorComponents(SimpleVTKClassModuleBase):
    def __init__(self, module_manager):
        SimpleVTKClassModuleBase.__init__(
            self, module_manager,
            vtk.vtkExtractVectorComponents(), 'Processing.',
            ('vtkDataSet',), ('vtkDataSet', 'vtkDataSet', 'vtkDataSet'),
            replaceDoc=True,
            inputFunctions=None, outputFunctions=None)
