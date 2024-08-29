##! 
##! Copyright(c) 2022, 2023 Stanford Research Systems, All rights reserved
##! Subject to the MIT License
##! 

import time

import socket
import select

from srsgui.inst.exceptions import InstCommunicationError, InstLoginFailureError
from .interface import Interface

EMPTY_BYTES = b''   # When socekt.recv() returns b'', the socket is closed.


class TcpipInterface(Interface):
    """Interface to use Ethernet TCP/IP communication"""

    NAME = 'tcpip'

    def __init__(self):
        super(TcpipInterface, self).__init__()
        self.type = TcpipInterface.NAME
        try:
            # Create an AF_INET, STREAM socket (TCPIP)
            self.socket = None
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except OSError as msg:
            raise InstCommunicationError(
                'Failed to create socket. Error code: {0} , Error message : {1}'
                .format(msg.errno, msg.strerror))

        self._is_connected = False
        self._ip_address = ''
        self._userid = ''
        self._password = ''
        self._tcp_port = 23  # TELNET port
        self._timeout = 20

    def _send(self, cmd):
        """
        Send a command over TCP/IP without the lock.
        This is a protected method that a user should not call directly,
        because it is not thread-safe. Use send instead.

        :param cmd: a string of command that will be internally converted to bytes
        :return: None
        """

        byte_cmd = bytes(cmd, 'utf-8')
        if self._term_char not in byte_cmd:
            byte_cmd += self._term_char

        try:
            self.socket.sendall(byte_cmd)
        except OSError:
            raise InstCommunicationError("Sending cmd '{}' to IP address: '{}' failed"
                                         .format(cmd, self._ip_address))

    def _write_binary(self, binary_array):
        if type(binary_array) not in (bytes, bytearray):
            raise TypeError('_write_binary requires bytes or bytearray')
        try:
            self.socket.sendall(binary_array)
        except OSError:
            raise InstCommunicationError("Writing binary '{}' to IP address: '{}' failed"
                                         .format((*map(hex, binary_array),), self._ip_address))

    def _recv(self):
        """
        Receive a reply over TCP/IP without the lock.
        This is a protected method that a user should not call directly,
        because it is not thread-safe.  Use recv instead.

        :return: bytes. It should be converted to string explicitly
        """

        reply = None
        try:
            # Now receive data
            ready, _, _ = select.select([self.socket], [], [], self._timeout)
            if self.socket in ready:
                reply = self.socket.recv(1024)
                if reply == EMPTY_BYTES:
                    self.disconnect()
                    raise InstCommunicationError("Connection closed with cmd: '{}' on IP: '{}' "
                                                 .format(self._cmd_in_waiting, self._ip_address))
        except TimeoutError:
            raise InstCommunicationError("Socket timeout with cmd: '{}' on IP: '{}' "
                                         .format(self._cmd_in_waiting, self._ip_address))
        except ConnectionResetError:
            self.disconnect()
            raise InstCommunicationError("Connection Reset with cmd: '{}' on IP: '{}' "
                                         .format(self._cmd_in_waiting, self._ip_address))
        except OSError:
            self.disconnect()
            raise InstCommunicationError("Connection closed with socket error with cmd: '{}' on IP: '{}' "
                                         .format(self._cmd_in_waiting, self._ip_address))

        if reply is None:
            raise InstCommunicationError("Timeout with Cmd: '{}' on IP: '{}' "
                                         .format(self._cmd_in_waiting, self._ip_address))
        return reply

    def _read_binary(self, length=4):

        try:
            data_buffer = b''
            rem = length
            while rem > 0:
                ready, _, _ = select.select([self.socket], [], [], self._timeout)
                if ready:
                    data = self.socket.recv(rem)
                else:
                    raise InstCommunicationError("Timeout with _read_binary")
                if data == EMPTY_BYTES:
                    self.disconnect()
                    raise InstCommunicationError(" Connection closed with _read_binary ")
                data_buffer += data
                rem = length - len(data_buffer)
            return data_buffer
        except TimeoutError:
            raise InstCommunicationError("Socket timeout with _read_binary")
        except ConnectionResetError:
            self.disconnect()
            raise InstCommunicationError("Connection Reset with _read_binary")
        except OSError:
            self.disconnect()
            raise InstCommunicationError("Connection closed with OSError in _read_binary")

    def query_text(self, cmd):
        with self.get_lock():
            self._cmd_in_waiting = cmd
            self._send(cmd)
            reply = self._recv()
            if self._term_char not in reply:
                time.sleep(0.5)
                reply += self._recv()
            self._cmd_in_waiting = None
            decoded_reply = reply.decode(encoding='utf-8').strip()  # returns a string not bytes
            if self._query_callback:
                self._query_callback('Queried Cmd: {} Reply: {}'.format(cmd, decoded_reply))
            return decoded_reply

    def set_timeout(self, seconds):
        self._timeout = seconds
        if self.socket:
            self.socket.settimeout(seconds)

    def get_timeout(self):
        return self._timeout

    def connect_without_login(self, ip_address, port=23):
        """
        Connect to a instrument that does not require login
        """

        self.socket.settimeout(self._timeout)
        try:
            self.socket.settimeout(self._timeout)
            self.socket.connect((ip_address, port))
            self._is_connected = True
            self._ip_address = ip_address
            self._tcp_port = port
            if self._connect_callback:
                self._connect_callback('Connected TCPIP IP:{} port:()'
                                       .format(ip_address, port))

        except TimeoutError:
            raise InstCommunicationError('Timeout connecting to ' + str(ip_address))
        except OSError:
            raise InstCommunicationError('Failed connecting to ' + str(ip_address))

    def connect_with_login(self, ip_address, userid, password, port=818):
        """
        Connect and login to an instrument

        Parameters
        -----------
            ip_address: str
                IP address of the instrument to connect, e.g., "192.168.1.100"
            userid: str
                User name to login
            password: str
                Password to login
            port: int, optional
                the default is 818, SRS RGA port.
        """

        self.socket.settimeout(self._timeout)
        try:
            self.socket.connect((ip_address, port))
            self._is_connected = True
        except TimeoutError:
            raise InstCommunicationError('Timeout connecting to ' + str(ip_address))
        except OSError:
            raise InstCommunicationError('Failed connecting to ' + str(ip_address))

        rep = 3
        i = 0
        with self._lock:
            for i in range(rep):
                self._send(' ')  # Send a blank command
                time.sleep(2.0)  # This delay is important to sync the log in prompts.
                                 # 1.0 s is not enough for VPN connection during backup.
                reply = self._recv()
                a = reply.split(b'\r')
                if reply is not None:
                    if b'Name:' in a[-1]:  # Is the last prompt 'Name:' ?
                        break
            if i == rep - 1:
                raise InstCommunicationError('No login prompt error')

            self._send(userid)
            time.sleep(0.5)
            self._recv()

            self._send(password)
            time.sleep(0.5)
            reply = self._recv()

            if b'Welcome' in reply:
                self._ip_address = ip_address
                self._tcp_port = port
                self._userid = userid
                self._password = password
                self.socket.setblocking(False)  # this is for using select instead of timeout setting
                if self._connect_callback:
                    self._connect_callback('Connected TCPIP IP: {} port: {}'
                                           .format(ip_address, port))

            else:
                self.disconnect()
                raise InstLoginFailureError('Check if user id and password are correct.')

    def connect(self, *args):
        num = len(args)
        if num == 4 or num == 3:
            self.connect_with_login(*args)
        elif num == 2 or num == 1:
            self.connect_without_login(*args)
        else:
            raise TypeError("Invalid Parameters for TcpipInterface")

    def disconnect(self):
        self._is_connected = False
        self.socket.close()
        if self._disconnect_callback:
            self._disconnect_callback('Disconnected TCPIP IP: {} port: {}'
                                      .format(self._ip_address, self._tcp_port))

    @staticmethod
    def parse_parameter_string(param_string):
        connect_parameters = []
        params = param_string.split(':')
        num = len(params)
        interface_type = params[0].strip().lower()
        if interface_type != TcpipInterface.NAME:
            return None
        if num > 5:
            raise ValueError('Too many parameters in "{}"'.format(param_string))

        connect_parameters.append(interface_type)  # 'tcpip'
        if num == 2:
            connect_parameters.append(params[1])  # ip address
        elif num == 3:
            connect_parameters.append(params[1])  # ip address
            connect_parameters.append(int(params[2]))  # port number
        elif num == 4:
            connect_parameters.append(params[1])  # ip address
            connect_parameters.append(params[2])  # user name
            connect_parameters.append(params[3])  # password
        elif num == 5:
            connect_parameters.append(params[1])  # ip address
            connect_parameters.append(params[2])  # user name
            connect_parameters.append(params[3])  # password
            connect_parameters.append(int(params[4]))  # port number
        return connect_parameters

    def clear_buffer(self):
        """
        It does not do anything for TCPIP interface
        """
        pass

    def get_info(self):
        return {'type': self.type,
                'ip_address': self._ip_address,
                'port': self._tcp_port}
