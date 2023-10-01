"""SonicPi synth server"""

import time
from pythonosc import osc_message_builder  # osc support
from pythonosc import udp_client
from .synthesizers import BEEP

## Module attributes ##
_current_synth = BEEP

## Module methodes ##
def use_synth(synth):
    global _current_synth
    _current_synth = synth


## Compound classes ##
class SonicPiCommon:

    UDP_IP = "127.0.0.1"

    def __init__(self):
        self.udp_ip = self.UDP_IP

    def set_parameter(self, udp_ip=""):
        if udp_ip == "":
            self.udp_ip = self.UDP_IP
        else:
            self.udp_ip = udp_ip

    def send(self, command):
        pass

    def sleep(self, duration):
        time.sleep(duration)

    def sample(self, command):
        self.send(command)

## Sonic Pi version 4.X: Ports can be found in 
# Windows: C:/Users/<User>/.sonic-pi/log/spider.log
# Linux: ~/.sonic-pi/log/spider.log
# Both the server_port and Token are required
# Default OSC Cues Port is still 4560

## Connection classes ##
class SonicPi(SonicPiCommon):
    """Communiction to Sonic Pi"""

    #UDP_PORT = 4557
    UDP_PORT = 51235

    #UDP_PORT_OSC_MESSAGE = 4559
    UDP_PORT_OSC_MESSAGE = 4560

    RUN_COMMAND = "/run-code"
    STOP_COMMAND = "/stop-all-jobs"
    START_RECORDING_COMMAND = "/start-recording"
    STOP_RECORDING_COMMAND = "/stop-recording"
    SAVE_RECORDING_COMMAND = "/save-recording"

    def __init__(self):
        super().__init__()
        self.udp_port = self.UDP_PORT
        self.udp_port_osc_message = self.UDP_PORT_OSC_MESSAGE
        self.token=None

        self._init_client()

    def _init_client(self):
        self.client = udp_client.UDPClient(
            self.udp_ip,
            self.udp_port
        )
        self.client_for_messages = udp_client.UDPClient(
            self.udp_ip,
            self.udp_port_osc_message
        )

    def set_parameter(self, udp_ip = "", token = "", udp_port=-1, udp_port_osc_message=-1):
        super().set_parameter(udp_ip)
        if udp_port == -1: udp_port = self.UDP_PORT
        self.udp_port = udp_port
        self.token=token
        if udp_port_osc_message == -1: udp_port_osc_message = self.UDP_PORT_OSC_MESSAGE
        self.udp_port_osc_message = udp_port_osc_message

        self._init_client()

    def play(self, command):
        command = f'use_synth :{_current_synth.name}\n{command}'
        self.send(command)

    def synth(self, command):
        self.send(command)

    def run(self, command):
        self.send_command(SonicPi.RUN_COMMAND, command)

    def start_recording(self):
        self.send_command(SonicPi.START_RECORDING_COMMAND)

    def stop_recording(self):
        self.send_command(SonicPi.START_RECORDING_COMMAND)

    def save_recording(self, name):
        self.send_command(SonicPi.SAVE_RECORDING_COMMAND,name)


    def send(self,command):
        self.run(command)

    def stop(self):
        self.send_command(SonicPi.STOP_COMMAND)

    def test_connection(self):
        # OSC::Server.new(PORT)
        # abort("ERROR: Sonic Pi is not listening on #{PORT} - is it running?")
        pass

    def send_command(self, address, argument=''):
        msg = osc_message_builder.OscMessageBuilder(address=address)
        if self.token is None:
            raise RuntimeError("No token specified, please set token from file or manually before sending a command")
        msg.add_arg(self.token)
        if argument != "":
            msg.add_arg(argument)
        msg = msg.build()
        self.client.send(msg)

    def send_message(self, message, *parameters):
        msg = osc_message_builder.OscMessageBuilder(message)
        for p in parameters:
            msg.add_arg(p)
        msg = msg.build()
        self.client_for_messages.send(msg)

class SonicPiNew(SonicPiCommon):
    """Communiction to Sonic Pi"""

    UDP_PORT = 4559

    def __init__(self):
        self.client = udp_client.UDPClient(
            self.UDP_IP,
            self.UDP_PORT
        )
        self.commandServer = SonicPi()
        # x= 'live_loop :py do\n  nv=sync "/SENDOSC"\n  puts nv\n  eval(nv[0])\nend'
        # self.commandServer.run(x)

    def set_OSC_receiver(self, source):
        self.commandServer.run(source)

    def send(self, address, *message):
        msg = osc_message_builder.OscMessageBuilder(address)
        for m in message:
            msg.add_arg(m)
        msg = msg.build()
        self.client.send(msg)

    def play(self, command):
        self.send(command)
