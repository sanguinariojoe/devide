# class generated by DeVIDE::createDeVIDEModuleFromVTKObject
from moduleMixins import simpleVTKClassModuleBase
import vtk

class vtkEnSight6BinaryReader(simpleVTKClassModuleBase):
    def __init__(self, moduleManager):
        simpleVTKClassModuleBase.__init__(
            self, moduleManager,
            vtk.vtkEnSight6BinaryReader(), 'Reading vtkEnSight6Binary.',
            (), ('vtkEnSight6Binary',),
            replaceDoc=True,
            inputFunctions=None, outputFunctions=None)
