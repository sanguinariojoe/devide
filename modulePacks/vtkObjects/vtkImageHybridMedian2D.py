# class generated by DeVIDE::createDeVIDEModuleFromVTKObject
from moduleMixins import simpleVTKClassModuleBase
import vtk

class vtkImageHybridMedian2D(simpleVTKClassModuleBase):
    def __init__(self, moduleManager):
        simpleVTKClassModuleBase.__init__(
            self, moduleManager,
            vtk.vtkImageHybridMedian2D(), 'Processing.',
            ('vtkImageData',), ('vtkImageData',),
            replaceDoc=True,
            inputFunctions=None, outputFunctions=None)