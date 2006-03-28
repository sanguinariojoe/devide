# class generated by DeVIDE::createDeVIDEModuleFromVTKObject
from module_kits.vtk_kit.mixins import SimpleVTKClassModuleBase
import vtk

class vtkDataObjectToDataSetFilter(SimpleVTKClassModuleBase):
    def __init__(self, moduleManager):
        SimpleVTKClassModuleBase.__init__(
            self, moduleManager,
            vtk.vtkDataObjectToDataSetFilter(), 'Processing.',
            ('vtkDataObject',), ('vtkDataSet',),
            replaceDoc=True,
            inputFunctions=None, outputFunctions=None)