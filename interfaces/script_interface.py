import copy
from logging_mixin import LoggingMixin
import os
from simple_api_mixin import SimpleAPIMixin

class ScriptInterface(SimpleAPIMixin, LoggingMixin):

    def __init__(self, devide_app):
        self.devide_app = devide_app

        # initialise logging mixin
        LoggingMixin.__init__(self)

        print "Initialising script interface..."
        
    def handler_post_app_init(self):
        """DeVIDE-required method for interfaces."""

        pass

    def quit(self):
        pass

    def start_main_loop(self):
        self.log_message('Starting to execute script.')
        sv = self.devide_app.main_config.script
        script_params = self.devide_app.main_config.script_params

        if sv is None:
            self.log_error('No script name specified with --script.')
            self.log_error('Nothing to run, will exit.')

        else:
            g2 = {}
            g2.update(globals())
            g2['interface'] = self
            g2['script_params'] = script_params
            execfile(sv, g2)

        self.log_message('Shutting down.')
        self.quit()

    
