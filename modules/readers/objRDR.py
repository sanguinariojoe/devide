# $Id$

from module_base import ModuleBase
from module_mixins import FilenameViewModuleMixin
import module_utils
import vtk
import os


class objRDR(FilenameViewModuleMixin, ModuleBase):
    
    def __init__(self, module_manager):
        """Constructor (initialiser) for the PD reader.

        This is almost standard code for most of the modules making use of
        the FilenameViewModuleMixin mixin.
        """
        
        # call the constructor in the "base"
        ModuleBase.__init__(self, module_manager)

        # setup necessary VTK objects
	self._reader = vtk.vtkOBJReader()
        
        # ctor for this specific mixin
        FilenameViewModuleMixin.__init__(
            self,
            'Select a filename',
            'Wavefront OBJ data (*.obj)|*.obj|All files (*)|*',
            {'vtkOBJReader': self._reader})

        module_utils.setup_vtk_object_progress(self, self._reader,
                                           'Reading Wavefront OBJ data')

        # set up some defaults
        self._config.filename = ''

	self.sync_module_logic_with_config()
        
    def close(self):
        del self._reader
        # call the close method of the mixin
        FilenameViewModuleMixin.close(self)

    def get_input_descriptions(self):
	return ()
    
    def set_input(self, idx, input_stream):
	raise Exception
    
    def get_output_descriptions(self):
        # equivalent to return ('vtkPolyData',)
	return (self._reader.GetOutput().GetClassName(),)
    
    def get_output(self, idx):
	return self._reader.GetOutput()

    def logic_to_config(self):
        filename = self._reader.GetFileName()
        if filename == None:
            filename = ''

        self._config.filename = filename

    def config_to_logic(self):
        self._reader.SetFileName(self._config.filename)

    def view_to_config(self):
        self._config.filename = self._getViewFrameFilename()

    def config_to_view(self):
        self._setViewFrameFilename(self._config.filename)

    def execute_module(self):
        # get the vtkSTLReader to try and execute (if there's a filename)
        if len(self._reader.GetFileName()):        
            self._reader.Update()
            

