##! 
##! Copyright(c) 2022, 2023 Stanford Research Systems, All rights reserved
##! Subject to the MIT License
##! 

import logging
from .qt.QtCore import Signal

from .qt.QtGui import QKeySequence
from .qt.QtWidgets import QFrame, QMessageBox, QShortcut, \
                          QVBoxLayout, QHBoxLayout, QTextBrowser, QPushButton, QLineEdit
logger = logging.getLogger(__name__)


class CommandTerminal(QFrame):
    """
    Terminal to control instruments defined in the .taskconfig file

    Type a command in one of the following ways:

    - inst_name:remote_command

        'inst_name' is the first item after the prefix  "inst:" in a line in
        the .taskconfig file. 'Remote_command' after the colon is a raw remote
        command of the instrument. Terminals send the 'remote_command' directly
        to the instrument 'inst_name', and display a reply if the instrument
        sends one back.

        dut:\*idn?

        dut:mi10  - This is a RGA100 command to set scan initial mass to 10

    - inst_name.instrument_command

        When you use .before a command, the command is interpreted as a Python
        instrument command or a method defined in the Instrument subclass,
        which is the third item in the line starting with 'inst:' used
        in .taskconfig file.

        inst_name.(components.)dir  - it shows all available components, commands,
        and methods in the instrument or its component as a Python dictionary.

                rga.dir

                rga.status.dir

        rga.status.id_string - this returns the id string. It is a Python instrument
        command defined in the rga.status component.
        rga.scan.initial_mass = 10  - this changes the scan initial mass to 10.
        rga.scan.get_analog_scan()  - this is a method defined in the rga.scan component.

        With the prefix of 'inst_name:' or 'inst_name.', you can specify which
        instrument receive the following command, as either a raw remote command or
        a instrument command defined in a Instrument subclass.

    - command

        if you type a command without 'inst_name.' or 'inst_name:', the command goes
        to the first instrument in the .taskconfig file. A command with dot(s) is
        interpreted as a Python instrument command or a method. A command without
        any dot will be sent directly to the first instrument in the .taskconfig file
        as a raw remote command.
    """

    command_requested = Signal(str, str)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        if not hasattr(parent, 'inst_dict'):
            raise AttributeError('Parent has no inst_dict')

        self.setup_widget()
        self.history_buffer = []
        self.buffer_index = 0
        self.buffer_size = 40

    def setup_widget(self):
        """
        Set up the terminal widget
        """
        self.tbCommand = QTextBrowser(self)
        self.pbClear = QPushButton(self)
        self.pbClear.setText('Clear')
        self.leCommand = QLineEdit(self)
        self.pbSend = QPushButton(self)
        self.pbSend.setText('Send')

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.pbClear)
        h_layout.addWidget(self.leCommand)
        h_layout.addWidget(self.pbSend)

        v_layout = QVBoxLayout(self)
        v_layout.addWidget(self.tbCommand)
        v_layout.addLayout(h_layout)

        self.pbClear.clicked.connect(self.on_clear)
        self.pbSend.clicked.connect(self.on_send)
        self.leCommand.returnPressed.connect(self.on_send)
        self.leCommand.setText("Type  'help'  for more info")
        self.leCommand.selectAll()
        self.down_key = QShortcut(QKeySequence('DOWN'), self, self.on_down_pressed)
        self.up_key = QShortcut(QKeySequence('UP'), self, self.on_up_pressed)

    def on_clear(self):
        """
        When 'Clear' button is pressed, the terminal display and command input line is cleared.
        """
        self.tbCommand.clear()
        self.leCommand.clear()

    def on_up_pressed(self):
        """
        When the keyboard UP arrow key is pressed, the previous command in the history
        is displayed in the command input line.
        """
        try:
            if len(self.history_buffer) == 0:
                return
            self.buffer_index -= 1
            if self.buffer_index >= len(self.history_buffer):
                self.buffer_index = 0
            elif self.buffer_index < 0:
                self.buffer_index = len(self.history_buffer) - 1
            self.leCommand.setText(self.history_buffer[self.buffer_index])
        except Exception as e:
            self.tbCommand.append('{}'.format(e))

    def on_down_pressed(self):
        """
        When the keyboard DOWN arrow key is pressed, the next command in the history
        is displayed in the command input line.
        """

        try:
            if len(self.history_buffer) == 0:
                return
            self.buffer_index += 1
            if self.buffer_index >= len(self.history_buffer):
                self.buffer_index = 0
            elif self.buffer_index < 0:
                self.buffer_index = len(self.history_buffer) - 1
            self.leCommand.setText(self.history_buffer[self.buffer_index])
        except Exception as e:
            self.tbCommand.append('{}'.format(e))

    def on_send(self):
        """
        When the Send button is pressed, send the command in the command input line to the instrument.
        """
        try:
            cmd = self.leCommand.text().strip()
            reply = ''
            # self.tbCommand.append(cmd)
            self.leCommand.clear()

            self.history_buffer.append(cmd)
            if len(self.history_buffer) > self.buffer_size:
                self.history_buffer.pop(0)
            self.buffer_index = len(self.history_buffer)

            cmd_lower = cmd.lower()
            if cmd_lower == 'cls':
                self.tbCommand.clear()
                return

            if cmd_lower == 'help':
                self.tbCommand.append(self.__doc__)
                return
            self.command_requested.emit(cmd, '')

        except Exception as e:
            self.tbCommand.append('Error: {}'.format(str(e)))

    def handle_command(self, cmd, reply):
        """
        Display the processed command to the terminal display
        """
        try:
            if reply:
                self.tbCommand.append(f'{cmd}   ==>   {reply}')
            else:
                self.tbCommand.append(f'{cmd}')

        except Exception as e:
            self.tbCommand.append('Error from CommandTerminal: {}'.format(str(e)))
