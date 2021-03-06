import code
from code import softspace
import os
import sys
import wx
import new

def sanitise_text(text):
    """When we process text before saving or executing, we sanitise it
    by changing all CR/LF pairs into LF, and then nuking all remaining CRs.
    This consistency also ensures that the files we save have the correct
    line-endings depending on the operating system we are running on.

    It also turns out that things break when after an indentation
    level at the very end of the code, there is no empty line.  For
    example (thanks to Emiel v. IJsseldijk for reproducing!):
    def hello():
      print "hello" # and this is the last line of the text
    Will not completely define method hello.
    
    To remedy this, we add an empty line at the very end if there's
    not one already.

    """
    
    text = text.replace('\r\n', '\n')
    text = text.replace('\r', '')

    lines = text.split('\n')
    
    if lines and len(lines[-1]) != 0:
        return text + '\n'
    else:
        return text

def runcode(self, code):
    """Execute a code object.

    Our extra-special verson of the runcode method.  We use this when we
    want py_shell_mixin._run_source() to generate real exceptions, and
    not just output to stdout, for example when CodeRunner is executed
    as part of a network.  This runcode() is explicitly called by our local
    runsource() method.
    """
    try:
        exec code in self.locals
    except SystemExit:
        raise
    except:
        raise
        #self.showtraceback()
    else:
        if softspace(sys.stdout, 0):
            print

def runsource(self, source, filename="<input>", symbol="single",
              runcode=runcode):
    """Compile and run some source in the interpreter.

    Our extra-special verson of the runsource method.  We use this when we
    want py_shell_mixin._run_source() to generate real exceptions, and
    not just output to stdout, for example when CodeRunner is executed
    as part of a network.  This method calls our special runcode() method
    as well.

    Arguments are as for compile_command(), but pass in interp instance as
    first parameter!

    """
    try:
        # this could raise OverflowError, SyntaxEror, ValueError
        code = self.compile(source, filename, symbol)
    except (OverflowError, SyntaxError, ValueError):
        # Case 1
        raise
        #return False

    if code is None:
        # Case 2
        return True

    # Case 3
    runcode(self, code)
    return False


class PythonShellMixin:

    def __init__(self, shell_window, module_manager):
        # init close handlers
        self.close_handlers = []
        self.shell_window = shell_window
        self.module_manager = module_manager

        self._last_fileselector_dir = ''

    def close(self, exception_printer):
        for ch in self.close_handlers:
            try:
                ch()
            except Exception, e:
                exception_printer(
                    'Exception during PythonShellMixin close_handlers: %s' %
                    (str(e),))

        del self.shell_window

    def _open_python_file(self, parent_window):
        filename = wx.FileSelector(
                'Select file to open into current edit',
                self._last_fileselector_dir, "", "py",
                "Python files (*.py)|*.py|All files (*.*)|*.*",
                wx.OPEN, parent_window)

        if filename:
            # save directory for future use
            self._last_fileselector_dir = \
                    os.path.dirname(filename)

            f = open(filename, 'r')
                
            t = f.read()
            t = sanitise_text(t)
            f.close()
                
            return filename, t

        else:
            return (None, None)

    def _save_python_file(self, filename, text):
        text = sanitise_text(text)
        
        f = open(filename, 'w')
        f.write(text)
        f.close()
        
    def _saveas_python_file(self, text, parent_window):
        filename = wx.FileSelector(
                'Select filename to save current edit to',
                self._last_fileselector_dir, "", "py",
                "Python files (*.py)|*.py|All files (*.*)|*.*",
                wx.SAVE, parent_window)

        if filename:
            # save directory for future use
            self._last_fileselector_dir = \
                    os.path.dirname(filename)

            # if the user has NOT specified any fileextension, we
            # add .py.  (on Win this gets added by the
            # FileSelector automatically, on Linux it doesn't)
            if os.path.splitext(filename)[1] == '':
                filename = '%s.py' % (filename,)

            self._save_python_file(filename, text)

            return filename
        
        return None
                
    def _run_source(self, text, raise_exceptions=False):
        """Compile and run the source given in text in the shell interpreter's
        local namespace.

        The idiot pyshell goes through the whole shell.push -> interp.push
        -> interp.runsource -> InteractiveInterpreter.runsource hardcoding the
        'mode' parameter (effectively) to 'single', thus breaking multi-line
        definitions and whatnot.

        Here we do some deep magic (ha ha) to externally override the interp
        runsource.  Python does completely rule.

        We do even deeper magic when raise_exceptions is True: we then
        raise real exceptions when errors occur instead of just outputting to
        stederr.
        """

        text = sanitise_text(text)
        interp = self.shell_window.interp

        if raise_exceptions:
            # run our local runsource, don't do any stdout/stderr redirection,
            # this is happening as part of a network.
            more = runsource(interp, text, '<input>', 'exec')
            
        else:
            # our 'traditional' version for normal in-shell introspection and
            # execution.  Exceptions are turned into nice stdout/stderr
            # messages.
            
            stdin, stdout, stderr = sys.stdin, sys.stdout, sys.stderr
            sys.stdin, sys.stdout, sys.stderr = \
                       interp.stdin, interp.stdout, interp.stderr
            
            # look: calling class method with interp instance as first
            # parameter comes down to the same as interp calling runsource()
            # as its parent method.
            more = code.InteractiveInterpreter.runsource(
                interp, text, '<input>', 'exec')

            # make sure the user can type again
            self.shell_window.prompt()

            sys.stdin = stdin
            sys.stdout = stdout
            sys.stderr = stderr

        return more

    def output_text(self, text):
        self.shell_window.write(text + '\n')
        self.shell_window.prompt()
    
    def support_vtk(self, interp):
        if hasattr(self, 'vtk_renderwindows'):
            return

        import module_kits
        if 'vtk_kit' not in module_kits.module_kit_list:
            self.output_text('No VTK support.')
            return
        
        from module_kits import vtk_kit
        vtk = vtk_kit.vtk

        def get_render_info(instance_name):
            instance = self.module_manager.get_instance(instance_name)

            if instance is None:
                return None
            
            class RenderInfo:
                pass

            render_info = RenderInfo()

            render_info.renderer = instance.get_3d_renderer()
            render_info.render_window = instance.get_3d_render_window()
            render_info.interactor = instance.\
                                     get_3d_render_window_interactor()
            

            return render_info

        new_dict = {'vtk' : vtk,
                    'vtk_get_render_info' : get_render_info}

        interp.locals.update(new_dict)
        self.__dict__.update(new_dict)

        self.output_text('VTK support loaded.')

    def support_matplotlib(self, interp):
        if hasattr(self, 'mpl_figure_handles'):
            return

        import module_kits

        if 'matplotlib_kit' not in module_kits.module_kit_list:
            self.output_text('No matplotlib support.')
            return

        from module_kits import matplotlib_kit
        pylab = matplotlib_kit.pylab
        
        # setup shutdown logic ########################################
        self.mpl_figure_handles = []

        def mpl_close_handler():
            for fh in self.mpl_figure_handles:
                pylab.close(fh)
        
        self.close_handlers.append(mpl_close_handler)
        
        # hook our mpl_new_figure method ##############################

        # mpl_new_figure hook so that all created figures are registered
        # and will be closed when the module is closed
        def mpl_new_figure(*args, **kwargs):
            handle = pylab.figure(*args, **kwargs)
            self.mpl_figure_handles.append(handle)
            return handle

        def mpl_close_figure(handle):
            """Close matplotlib figure.
            """
            pylab.close(handle)
            if handle in self.mpl_figure_handles:
                idx = self.mpl_figure_handles.index(handle)
                del self.mpl_figure_handles[idx]

        # replace our hook's documentation with the 'real' documentation
        mpl_new_figure.__doc__ = pylab.figure.__doc__

        # stuff the required symbols into the module's namespace ######
        new_dict = {'matplotlib' : matplotlib_kit.matplotlib,
                    'pylab' : matplotlib_kit.pylab,
                    'mpl_new_figure' : mpl_new_figure,
                    'mpl_close_figure' : mpl_close_figure}
        
        interp.locals.update(new_dict)
        self.__dict__.update(new_dict)

        self.output_text('matplotlib support loaded.')

