# class generated by DeVIDE::createDeVIDEModuleFromVTKObject
from moduleMixins import simpleVTKClassModuleBase
import vtk

class vtkImageOpenClose3D(simpleVTKClassModuleBase):
    def __init__(self, moduleManager):
        simpleVTKClassModuleBase.__init__(
            self, moduleManager,
            vtk.vtkImageOpenClose3D(), 'Processing.',
            ('vtkImageData',), ('vtkImageData',),
            replaceDoc=True,
            inputFunctions=None, outputFunctions=None)
