# decimateFLT.py copyright (c) 2003 by Charl P. Botha http://cpbotha.net/
# $Id$
# module that triangulates and decimates polygonal input

import gen_utils
from module_base import ModuleBase
from module_mixins import ScriptedConfigModuleMixin
import module_utils
import vtk
import gen_utils
from module_base import ModuleBase
from module_mixins import ScriptedConfigModuleMixin
import module_utils
import vtk


class decimate(ScriptedConfigModuleMixin, ModuleBase):

    def __init__(self, module_manager):

        # call parent constructor
        ModuleBase.__init__(self, module_manager)

        # the decimator only works on triangle data, so we make sure
        # that it only gets triangle data
        self._triFilter = vtk.vtkTriangleFilter()
        self._decimate = vtk.vtkDecimatePro()
        self._decimate.PreserveTopologyOn()
        self._decimate.SetInput(self._triFilter.GetOutput())

        module_utils.setup_vtk_object_progress(self, self._triFilter,
                                           'Converting to triangles')
        
        module_utils.setup_vtk_object_progress(self, self._decimate,
                                           'Decimating mesh')
        
                                           
        # now setup some defaults before our sync
        self._config.target_reduction = self._decimate.GetTargetReduction() \
                                        * 100.0

        config_list = [
            ('Target reduction (%):', 'target_reduction', 'base:float', 'text',
             'Decimate algorithm will attempt to reduce by this much.')]

        ScriptedConfigModuleMixin.__init__(
            self, config_list,
            {'Module (self)' : self,
             'vtkDecimatePro' : self._decimate,
             'vtkTriangleFilter' : self._triFilter})

        self.sync_module_logic_with_config()
        
    def close(self):
        # we play it safe... (the graph_editor/module_manager should have
        # disconnected us by now)
        self.set_input(0, None)

        # this will take care of all display thingies
        ScriptedConfigModuleMixin.close(self)

        ModuleBase.close(self)

        # get rid of our reference
        del self._decimate
        del self._triFilter

    def get_input_descriptions(self):
	return ('vtkPolyData',)
    
    def set_input(self, idx, inputStream):
        self._triFilter.SetInput(inputStream)
    
    def get_output_descriptions(self):
	return (self._decimate.GetOutput().GetClassName(),)
    
    def get_output(self, idx):
        return self._decimate.GetOutput()

    def logic_to_config(self):
        self._config.target_reduction = self._decimate.GetTargetReduction() \
                                        * 100.0

    def config_to_logic(self):
        self._decimate.SetTargetReduction(
            self._config.target_reduction / 100.0)

    def execute_module(self):
        # get the filter doing its thing
        self._triFilter.Update()
        
        self._decimate.Update()
        

