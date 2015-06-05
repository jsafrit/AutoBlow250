import serial
import sys
import logging
from time import sleep
from FC_protocol import command_packet, wrap_packet, ProCommands, PKT_PREAMBLE, hs_status_id


#####################################################
# FC250 class
#####################################################
class FC250Handset(object):
    def __init__(self, comm, name=None):
        """
        FC250 Handset
        :param comm: Serial port unit is connected to (i.e. 'COM12')
        :param name: Name of unit for results and log files
        """
        self.comm = comm
        if name:
            assert isinstance(name, str)
            self.name = name
        else:
            self.name = comm

        # init logging
        logfile_name = self.name + '.log'
        logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=logfile_name,
                            level=logging.INFO)

        logging.info('*** Initialization ***')
        logging.info('Creating FC250 Handset object "{}" on {}'.format(self.name, self.comm))

        # initiate serial connection to handset
        self.s = None
        try:
            self.s = serial.Serial(self.comm, 921600, timeout=2, writeTimeout=2)
        except serial.SerialException:
            error_code = str(sys.exc_info()[1]).split(':')[0]
            logging.error('Error: {}'.format(error_code))
            print(error_code)
            sys.exit(2)

        if not self.s or not self.s.isOpen():
            logging.critical('Unable to open comm port')
            print('Could not open comm {}'.format(self.comm))
            sys.exit(2)

        logging.info('Created FC250 Handset object "{}" on {}'.format(self.name, self.comm))

    def __del__(self):
        if self.s and self.s.isOpen():
            self.s.close()
            logging.warning('Shutting down without proper close')
        logging.shutdown()

    def close(self):
        """
        Close UUT
        :rtype : None
        """
        self.s.close()
        logging.info('Closing FC250 Handset object "%s" on %s', self.name, self.comm)
        logging.shutdown()

    def cmd_alcohol_test(self):
        """
        Initiate Alcohol Test
        :rtype : None
        """
        self.s.write(command_packet(ProCommands.PRO_CMD_DO_HUMAN_ALCOHOL_TEST))
        logging.info('Alcohol Test requested')

    def cmd_go_sleep(self):
        """
        Send Handset to sleep state
        :rtype : None
        """
        self.s.write(command_packet(ProCommands.PRO_CMD_SLEEP))
        logging.info('Handset Sleep requested')

    def cmd_get_status(self, interval=1):
        """
        Request status from the Handset
        :param interval: time in seconds between poll
        :rtype : None
        """
        self.s.write(wrap_packet())
        logging.info('Handset Status requested')

        sleep(interval)

        incoming_bytes = self.s.inWaiting()
        while not incoming_bytes:
            logging.warning('Handset Status retrying request')
            self.s.write(wrap_packet())
            sleep(.5)
            incoming_bytes = self.s.inWaiting()

        incoming_packet = self.s.read(incoming_bytes)

        # Verify this is a handset status packet
        pkt_preamble = incoming_packet[PKT_PREAMBLE]
        if pkt_preamble[:4] != hs_status_id:
            return None

        return incoming_packet
