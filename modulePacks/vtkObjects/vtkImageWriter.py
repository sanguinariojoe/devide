# class generated by DeVIDE::createDeVIDEModuleFromVTKObject
from moduleMixins import simpleVTKClassModuleBase
import vtk

class vtkImageWriter(simpleVTKClassModuleBase):
    def __init__(self, moduleManager):
        simpleVTKClassModuleBase.__init__(
            self, moduleManager,
            vtk.vtkImageWriter(), 'Writing vtkImage.',
            ('vtkImage',), (),
            replaceDoc=True,
            inputFunctions=None, outputFunctions=None)
