import struct
import datetime
import sys
from msvcrt import getch, kbhit
from FC250 import FC250Handset
from FC_protocol import HandsetState, HeaterState, CellHeatLevel, PKT_PREAMBLE, BLOCK

log = None
handset_uut = None


def hex_dump(data):
    return ''.join('{:02X}'.format(x) for x in data)


def poll(interval=1):
    incoming_packet = handset_uut.cmd_get_status(interval)
    if not incoming_packet:
        return

    # extract relevant data from packet
    block = incoming_packet[BLOCK]

    my_labels = ('fVoltageIn', 'fLithiumBatteryVoltage', 'fIoFcCaseTemperature', 'fIoBreathTemperature',
                 'fIoUnitCaseTemperature', 'fCurrentCellTemperatureSetpoint', 'fUtlRegulationTemperature')
    my_floats = struct.unpack('<fffffff', block[64:92])
    lookup = dict(zip(my_labels, my_floats))

    my_labels2 = ('uiTestActive', 'ucStaState', 'ucBasicState', 'ucStaHeaterState', 'ucUtlCellHeatLevel',
                  'ucClstStatus')
    my_data = struct.unpack('<LBBBBB', block[55:64])
    lookup2 = dict(zip(my_labels2, my_data))

    hs_serial, *_ = struct.unpack('<L',  incoming_packet[PKT_PREAMBLE][5:9])

    line = '{0:%H:%M:%S},'.format(datetime.datetime.now())
    line += '{:0.2f},'.format(lookup['fVoltageIn'])
    line += '{:0.2f},'.format(lookup['fIoFcCaseTemperature'])
    line += '{:0.2f},'.format(lookup['fIoUnitCaseTemperature'])
    line += '0x{:08X},'.format(hs_serial)
    line += '{},'.format(HandsetState(lookup2['ucStaState']).name)
    line += '{},'.format(HeaterState(lookup2['ucStaHeaterState']).name)
    line += '{}'.format(CellHeatLevel(lookup2['ucUtlCellHeatLevel']).name)
    print(line)
    print(line, file=log)


def closeout():
    # global log
    print('Closing log files and exiting.')
    log.close()
    handset_uut.close()
    sys.exit(1)


def main():
    global log
    global handset_uut

    handset_uut = FC250Handset(sys.argv[1], sys.argv[2])
    log = open(sys.argv[2]+'.csv', mode='a', buffering=1)
    legend = 'time,fVoltageIn,fIoFcCaseTemperature,fIoUnitCaseTemperature,S/N,HandsetState,HeaterState,CellHeaterLevel'
    print(legend, file=log)

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
                    handset_uut.cmd_alcohol_test()
                    print('Alcohol Test Requested...')
                    # print('## Alcohol Test Requested', file=log)
                elif my_key == 115:      # 's'
                    handset_uut.cmd_go_sleep()
                    print('Handset Sleep Requested...')
                    # print('## Handset Sleep Requested', file=log)
                else:
                    print("::{}::".format(my_key))
            poll(1)

    except KeyboardInterrupt:
        closeout()

if __name__ == '__main__':
    main()
