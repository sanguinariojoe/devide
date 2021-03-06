# Copyright (c) Charl P. Botha, TU Delft
# All rights reserved.
# See COPYRIGHT for details.

import itk
import gen_utils
import module_kits.itk_kit
from module_base import ModuleBase
from module_mixins import ScriptedConfigModuleMixin

class watershed(ScriptedConfigModuleMixin, ModuleBase):


    def __init__(self, module_manager):
        ModuleBase.__init__(self, module_manager)

        # pre-processing on input image: it will be thresholded
        self._config.threshold = 0.1
        # flood level: this will be the starting level of precipitation
        self._config.level = 0.1

        configList = [
            ('Threshold:', 'threshold', 'base:float', 'text',
             'Pre-processing image threshold (0.0-1.0).'),
            ('Level:', 'level', 'base:float', 'text',
             'Initial precipitation level (0.0-1.0).')]
        



        # setup the pipeline
        if3 = itk.Image[itk.F, 3]
        self._watershed = itk.WatershedImageFilter[if3].New()
        
        module_kits.itk_kit.utils.setupITKObjectProgress(
            self, self._watershed, 'itkWatershedImageFilter',
            'Performing watershed')

        iul3 = itk.Image[itk.UL, 3]
        # change this to SI or UI when this becomes available in the
        # wrappings
        iss3 = itk.Image[itk.SS, 3]
        self._relabel_components = \
                itk.RelabelComponentImageFilter[iul3, iss3].New()

        self._relabel_components.SetInput(self._watershed.GetOutput())

        module_kits.itk_kit.utils.setupITKObjectProgress(
            self, self._relabel_components,
            'itk.RelabelComponentImageFilter',
            'Relabeling watershed output components')


        # self._watershed could be changed later, so we don't add it
        # to the introspection list.
        ScriptedConfigModuleMixin.__init__(
            self, configList,
            {'Module (self)' : self})

        self.sync_module_logic_with_config()
        
    def close(self):
        # we play it safe... (the graph_editor/module_manager should have
        # disconnected us by now)
        for input_idx in range(len(self.get_input_descriptions())):
            self.set_input(input_idx, None)

        # this will take care of all display thingies
        ScriptedConfigModuleMixin.close(self)
        # and the baseclass close
        ModuleBase.close(self)
            
        # remove all bindings
        del self._watershed

    def execute_module(self):
        self._relabel_components.Update()
        # the watershed module is REALLY CRAP about setting progress to 100,
        # so we do it here.
        #self._module_manager.setProgress(100, "Watershed complete.")

    def get_input_descriptions(self):
        return ('ITK Image (3D, float)',)

    def set_input(self, idx, inputStream):
        try:
            self._watershed.SetInput(inputStream)

        except TypeError, e:
            # deduce the type
            itku = module_kits.itk_kit.utils
            ss = itku.get_img_type_and_dim_shortstring(inputStream)
            try:
                w = itk.WatershedImageFilter[getattr(itk.Image,ss)].New()
            except KeyError, e:
                emsg = 'Could not create Watershed with input type %s. '\
                        'Please try a different input type.' % (ss,)
                raise TypeError, emsg

            # if we get here, we have a new filter
            # disconnect old one
            self._watershed.SetInput(None)
            # replace with new one (old one should be garbage
            # collected)
            self._watershed = w
            # reconnect it to the input of the relabeler
            self._relabel_components.SetInput(self._watershed.GetOutput())
            # setup progress
            module_kits.itk_kit.utils.setupITKObjectProgress(
                self, self._watershed, 'itkWatershedImageFilter',
                'Performing watershed')
            # re-apply config
            self.sync_module_logic_with_config()
            # connect input and hope it works.
            self._watershed.SetInput(inputStream)

    def get_output_descriptions(self):
        return ('ITK Image (3D, unsigned long)',)

    def get_output(self, idx):
        return self._relabel_components.GetOutput()

    def config_to_logic(self):
        self._config.threshold = gen_utils.clampVariable(
            self._config.threshold, 0.0, 1.0)
        self._watershed.SetThreshold(self._config.threshold)
        
        self._config.level = gen_utils.clampVariable(
            self._config.level, 0.0, 1.0)
        self._watershed.SetLevel(self._config.level)

    def logic_to_config(self):
        self._config.threshold = self._watershed.GetThreshold()
        self._config.level = self._watershed.GetLevel()

