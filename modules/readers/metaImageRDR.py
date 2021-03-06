# $Id$

from module_base import ModuleBase
from module_mixins import ScriptedConfigModuleMixin
import module_utils
import vtk
import wx


class metaImageRDR(ScriptedConfigModuleMixin, ModuleBase):
    
    def __init__(self, module_manager):
        ModuleBase.__init__(self, module_manager)

        self._reader = vtk.vtkMetaImageReader()

        module_utils.setup_vtk_object_progress(self, self._reader,
                                           'Reading MetaImage data.')
        

        self._config.filename = ''

        configList = [
            ('File name:', 'filename', 'base:str', 'filebrowser',
             'The name of the MetaImage file you want to load.',
             {'fileMode' : wx.OPEN,
              'fileMask' :
              'MetaImage single file (*.mha)|*.mha|MetaImage separate header '
              '(*.mhd)|*.mhd|All files (*.*)|*.*'})]

        ScriptedConfigModuleMixin.__init__(
            self, configList,
            {'Module (self)' : self,
             'vtkMetaImageReader' : self._reader})

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
        del self._reader

    def get_input_descriptions(self):
        return ()

    def set_input(self, idx, inputStream):
        raise Exception

    def get_output_descriptions(self):
        return ('vtkImageData',)

    def get_output(self, idx):
        return self._reader.GetOutput()

    def logic_to_config(self):
        self._config.filename = self._reader.GetFileName()

    def config_to_logic(self):
        self._reader.SetFileName(self._config.filename)
        
    def execute_module(self):
        self._reader.Update()
        

        
        
        
