# -*- coding: utf-8 -*-
"""
Taken from https://github.com/jupyter/qtconsole/blob/master/examples/embed_qtconsole.py
"""
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.manager import QtKernelManager

# The ID of an installed kernel, e.g. 'bash' or 'ir'.
USE_KERNEL = 'python3'

 
class ConsoleWidget(RichJupyterWidget):
    """Jupyter kernel client in Qt"""

    def __init__(self, *args, **kwargs):
        super().__init__()

        kernel_manager = QtKernelManager(kernel_name=USE_KERNEL)
        kernel_manager.start_kernel()
    
        kernel_client = kernel_manager.client()
        kernel_client.start_channels()

        self.kernel_manager = kernel_manager
        self.kernel_client = kernel_client

        self.exit_requested.connect(self.stop)

        self.font_size = 8
        # setup scientific mode and import WEST database access module
        self.execute_command('%pylab')
        self.execute_command('import pywed as pd')
        self.execute_command('from pywed import *')

    def stop(self):
        print('Shutting down kernel...')
        self.kernel_client.stop_channels()
        self.kernel_manager.shutdown_kernel()

    def push_vars(self, variableDict):
        """
        Given a dictionary containing name / value pairs, push those variables
        to the Jupyter console widget
        """
        self.kernel_manager.kernel.shell.push(variableDict)

    def clear(self):
        """
        Clears the terminal
        """
        self._control.clear()

    def print_text(self, text):
        """
        Prints some plain text to the console
        """
        self._append_plain_text(text)

    def execute_command(self, command):
        """
        Execute a command in the frame of the console widget
        """
        self.print_text(command + '\n')
        self._execute(command, False)
