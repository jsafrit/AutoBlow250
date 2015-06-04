import serial
import sys
import logging
from FC_protocol import command_packet, ProCommands

do_alcohol_test = command_packet(ProCommands.PRO_CMD_DO_HUMAN_ALCOHOL_TEST)
go_to_sleep = command_packet(ProCommands.PRO_CMD_SLEEP)

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
        self.logging.basicConfig(format='%(asctime)s %(message)s',
                                 datefmt='%Y-%m-%d %H:%M:%S',
                                 filename=logfile_name,
                                 level=logging.INFO)

        self.logging.info('*** Initialization ***')
        self.logging.info('Creating FC250 Handset object "{}" on {}'.format(self.name, self.comm))

        # initiate serial connection to handset
        self.s = None
        try:
            self.s = serial.Serial(self.comm, 921600, timeout=2, writeTimeout=2)
        except serial.SerialException:
            error_code = str(sys.exc_info()[1]).split(':')[0]
            self.logging.info('Error: {}'.format(error_code))
            print(error_code)
            sys.exit(2)

        if not self.s or not self.s.isOpen():
            self.logging.info('Unable to open comm port')
            print('Could not open comm {}'.format(self.comm))
            sys.exit(2)

        self.logging.info('Created FC250 Handset object "{}" on {}'.format(self.name, self.comm))

    def close(self):
        """
        Close UUT
        :rtype : None
        """
        self.s.close()
        self.logging.info('Closing FC250 Handset object "%s" on %s', self.name, self.comm)

    def cmd_alcohol_test(self):
        """
        Initiate Alcohol Test
        :rtype : None
        """
        self.s.write(command_packet(ProCommands.PRO_CMD_DO_HUMAN_ALCOHOL_TEST))
        self.logging.info('Alcohol Test requested')

    def cmd_go_sleep(self):
        """
        Send Handset to sleep state
        :rtype : None
        """
        self.s.write(command_packet(ProCommands.PRO_CMD_SLEEP))
        self.logging.info('Handset Sleep requested')
