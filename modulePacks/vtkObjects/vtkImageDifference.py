# class generated by DeVIDE::createDeVIDEModuleFromVTKObject
from moduleMixins import simpleVTKClassModuleBase
import vtk

class vtkImageDifference(simpleVTKClassModuleBase):
    def __init__(self, moduleManager):
        simpleVTKClassModuleBase.__init__(
            self, moduleManager,
            vtk.vtkImageDifference(), 'Processing.',
            ('Input 1 (vtkImageData)', 'Input 2 (vtkImageData)'), ('vtkImageData',),
            replaceDoc=True,
            inputFunctions=('SetInput1(inputStream)', 'SetInput2(inputStream)'), outputFunctions=None)
