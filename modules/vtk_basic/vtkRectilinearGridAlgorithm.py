# class generated by DeVIDE::createDeVIDEModuleFromVTKObject
from module_kits.vtk_kit.mixins import SimpleVTKClassModuleBase
import vtk

class vtkRectilinearGridAlgorithm(SimpleVTKClassModuleBase):
    def __init__(self, moduleManager):
        SimpleVTKClassModuleBase.__init__(
            self, moduleManager,
            vtk.vtkRectilinearGridAlgorithm(), 'Processing.',
            ('vtkRectilinearGrid',), ('vtkRectilinearGrid',),
            replaceDoc=True,
            inputFunctions=None, outputFunctions=None)