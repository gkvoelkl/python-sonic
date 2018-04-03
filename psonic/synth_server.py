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

    def send(self, command):
        pass

    def sleep(self, duration):
        time.sleep(duration)

    def sample(self, command):
        self.send(command)


## Connection classes ##
class SonicPi(SonicPiCommon):
    """Communiction to Sonic Pi"""

    UDP_PORT = 4557
    UDP_PORT_OSC_MESSAGE = 4559
    GUI_ID = 'SONIC_PI_PYTHON'

    RUN_COMMAND = "/run-code"
    STOP_COMMAND = "/stop-all-jobs"

    def __init__(self):
        self.client = udp_client.UDPClient(
            self.UDP_IP,
            self.UDP_PORT
        )
        self.client_for_messages = udp_client.UDPClient(
            self.UDP_IP,
            self.UDP_PORT_OSC_MESSAGE
        )

    def play(self, command):
        command = 'use_synth :{0}\n'.format(_current_synth.name) + command
        self.send(command)

    def synth(self, command):
        self.send(command)

    def run(self, command):
        self.send_command(SonicPi.RUN_COMMAND, command)

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
        msg.add_arg('SONIC_PI_PYTHON')
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
