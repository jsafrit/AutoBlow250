import serial
import time
import struct
import datetime
import sys
from msvcrt import getch, kbhit
from FC_protocol import wrap_packet, command_packet, HandsetState, HandsetBasicState, ProCommands 

# Handset Status Packet Blocks
PKT_PREAMBLE = slice(0, 21)
PREAMBLE = slice(21, 28)
BLOCK = slice(28, -3)
FOOTER = slice(-3, None)

my_comm = None
log = None


def hex_dump(data):
    return ''.join('{:02X}'.format(x) for x in data)


def poll():
    # out_packet = command_packet(ProCommands.PRO_REL_CMD_HANDSET_POWER, 1)
    # out_packet = command_packet(ProCommands.PRO_REL_CMD_CAMERA_POWER, 1)
    out_packet = wrap_packet()
    # print('Outgoing length: {}'.format(len(out_packet)))
    my_comm.write(out_packet)

    time.sleep(1)

    incoming_bytes = my_comm.inWaiting()
    while not incoming_bytes:
        incoming_bytes = my_comm.inWaiting()

    incoming_packet = my_comm.read(incoming_bytes)
    # print('Packet length: {}'.format(len(incoming_packet)))
    # print(hex_dump(incoming_packet))
    # print('{:16}'.format('Packet Preamble:'), end='')
    # print(hex_dump(incoming_packet[PKT_PREAMBLE]))
    # print('{:16}'.format('Preamble: '), end='')
    # print(hex_dump(incoming_packet[PREAMBLE]))
    # print('{:16}'.format('Block: '), end='')
    # print(hex_dump(incoming_packet[BLOCK]))
    # print('{:16}'.format('Footer: '), end='')
    # print(hex_dump(incoming_packet[FOOTER]))

    block = incoming_packet[BLOCK]

    my_labels = ('fVoltageIn', 'fLithiumBatteryVoltage', 'fIoFcCaseTemperature', 'fIoBreathTemperature',
                 'fIoUnitCaseTemperature', 'fCurrentCellTemperatureSetpoint', 'fUtlRegulationTemperature')
    my_floats = struct.unpack('<fffffff', block[64:92])
    lookup = dict(zip(my_labels, my_floats))


    my_labels2 = ('uiTestActive', 'ucStaState', 'ucBasicState', 'ucStaHeaterState', 'ucUtlCellHeatLevel',
                  'ucClstStatus')
    my_data = struct.unpack('<LBBBBB', block[55:64])
    lookup2 = dict(zip(my_labels2, my_data))

    # my_date = struct.unpack('<BBBBBB', block[132:138])
    # print(my_date)
    # print('{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

    # for x in ['fVoltageIn', 'fIoFcCaseTemperature', 'fCurrentCellTemperatureSetpoint']:  # 'fIoUnitCaseTemperature']:
    #     print('{:32}   {: 0.2f}'.format(x, lookup[x]))

    line = '{0:%H:%M:%S},'.format(datetime.datetime.now())
    line += '{:0.2f},'.format(lookup['fVoltageIn'])
    line += '{:0.2f},'.format(lookup['fIoFcCaseTemperature'])
    line += '{:0.2f}'.format(lookup['fIoUnitCaseTemperature'])
    print(line)
    print(line, file=log)
    print(HandsetState(lookup2['ucStaState']).name, HandsetBasicState(lookup2['ucBasicState']).name)


def closeout():
    global log
    print('Closing log files and exiting.')
    log.close()
    sys.exit(1)


def main():

    do_alcohol_test = command_packet(ProCommands.PRO_CMD_DO_HUMAN_ALCOHOL_TEST)
    go_to_sleep = command_packet(ProCommands.PRO_CMD_SLEEP)

    try:
        comm = sys.argv[1]
    except IndexError:
        print('Defaulting to "COM80"')
        comm = 'COM80'
    global my_comm
    global log
    log = open(comm+'.csv', mode='a', buffering=1)

    try:
        my_comm = serial.Serial(comm, 921600, timeout=2, writeTimeout=2)
    except serial.SerialException:
        print('BOOM! @ %s' % comm)
        print(str(sys.exc_info()[1]).split(':')[0])
        sys.exit(2)

    print('time,fVoltageIn,fIoFcCaseTemperature,fIoUnitCaseTemperature', file=log)

    try:
        while True:
            if kbhit():
                my_key = ord(getch())
                if my_key == 0 or my_key == 224:        # a special function key
                    # so get the next code
                    my_key = ord(getch())
                    print("+:{}:+".format(my_key))
                elif my_key == 27:      # <escape>
                    print('Boo!')
                elif my_key == 120:     # 'x'
                    closeout()
                elif my_key == 97:      # 'a'
                    my_comm.write(do_alcohol_test)
                    print('Alcohol Test Requested...')
                    print('## Alcohol Test Requested', file=log)
                elif my_key == 115:      # 's'
                    my_comm.write(go_to_sleep)
                    print('Handset Sleep Requested...')
                    print('## Handset Sleep Requested', file=log)
                else:
                    print("::{}::".format(my_key))
            poll()
    except KeyboardInterrupt:
        closeout()

if __name__ == '__main__':
    main()
