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
        super(ConsoleWidget, self).__init__(*args, **kwargs)

        self.kernel_manager = QtKernelManager(kernel_name=USE_KERNEL)
        self.kernel_manager.start_kernel()

        self.kernel_client = self.kernel_manager.client()
        self.kernel_client.start_channels()

        self.exit_requested.connect(self.stop)

        self.font_size = 8
        self.execute_command('%pylab')
        self.execute_command('import pywed as pd')
        
    def stop(self):
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

        # self.kernel_manager

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
