import struct
import datetime
import sys
from msvcrt import getch, kbhit
from FC250 import FC250Handset
from FC_protocol import HandsetState, HeaterState, CellHeatLevel, PKT_PREAMBLE, BLOCK

log = None
handset_uut = None
paused = False
capturing = False
key_help = {'a': 'Alcohol Test request',
            'r': 'Report Handset info',
            's': 'Sleep Handset',
            'p': 'Pause/Resume status',
            'c': 'Start Capture',
            'z': 'Stop Capture',
            '?': 'This help menu',
            'x': 'Exit program'
            }


def hex_dump(data):
    return ''.join('{:02X}'.format(x) for x in data)


def poll(interval=1):
    incoming_packet = handset_uut.cmd_get_status(interval)
    if not incoming_packet:
        return

    # extract relevant data from packet
    block = incoming_packet[BLOCK]
    status_lookup = create_status_dict(block)

    hs_serial, *_ = struct.unpack('<L',  incoming_packet[PKT_PREAMBLE][5:9])

    # line = '{0:%H:%M:%S.%f},'.format(datetime.datetime.now())
    timestamp = datetime.datetime.now()
    line = '{:%H:%M:%S}.{:03d},'.format(timestamp, int(timestamp.microsecond / 1000))
    # line += '{:0.2f},'.format(status_lookup['fVoltageIn'])
    # line += '{:0.2f},'.format(status_lookup['fIoFcCaseTemperature'])
    # line += '{:0.2f},'.format(status_lookup['fIoUnitCaseTemperature'])
    line += '{:8d},'.format(status_lookup['iCurrentBreathPressure'])
    # line += '0x{:08X},'.format(hs_serial)
    line += '{:8d},'.format(hs_serial)
    line += '{},'.format(HandsetState(status_lookup['ucStaState']).name)
    line += '{}'.format(HeaterState(status_lookup['ucStaHeaterState']).name)
    # line += '{}'.format(CellHeatLevel(status_lookup['ucUtlCellHeatLevel']).name)
    print(line)

    if capturing:
        print(line, file=log)

    # trailing_count = 0
    # if status_lookup['ucStaState'] in (HandsetState.STA_BLOWING, HandsetState.STA_WAIT_FOR_BLOW):
    #     trailing_count = 10
    #     print(line, file=log)
    #
    # if status_lookup['ucStaState'] in (HandsetState.STA_INIT_ABORT_DISP_WAIT, HandsetState.STA_ABORT_DISP_WAIT):
    #     if trailing_count > 0:
    #         trailing_count -= 1
    #         print(line, file=log)


def create_status_dict(block):
    my_labels = ('fVoltageIn', 'fLithiumBatteryVoltage', 'fHardwareRevision', 'fIoFcCaseTemperature',
                 'fIoBreathTemperature', 'fIoUnitCaseTemperature', 'fCurrentCellTemperatureSetpoint',
                 'fUtlRegulationTemperature', 'iPressureTemperature', 'iCaseTemperature')
    my_floats = struct.unpack('<ffffffffii', block[64:104])
    lookup = dict(zip(my_labels, my_floats))
    my_labels2 = ('uiTestActive', 'ucStaState', 'ucBasicState', 'ucStaHeaterState', 'ucUtlCellHeatLevel',
                  'ucClstStatus')
    my_data = struct.unpack('<LBBBBB', block[55:64])
    lookup2 = dict(zip(my_labels2, my_data))
    my_labels3 = ('fBrac', 'usBrac', 'uiHumLevel', 'iCurrentBreathPressure', 'iCurrentAmbientPressure',
                  'ucHumLoudness', 'ucHumTone', 'ucHumQuality', 'bSolenoidPulled')
    my_data3 = struct.unpack('<fHIiiBBBB', block[230:252])
    lookup3 = dict(zip(my_labels3, my_data3))
    status_lookup = lookup.copy()
    status_lookup.update(lookup2)
    status_lookup.update(lookup3)
    return status_lookup


def handle_keystrokes():
    global paused
    global capturing
    if kbhit():
        my_key = ord(getch())
        if my_key == 0 or my_key == 224:        # a special function key
            # so get the next code
            my_key = ord(getch())
            print("+:{}:+".format(my_key))
        elif my_key == 63:      # '?'
            paused = True
            print("  Help Menu")
            for k, v in key_help.items():
                print('   {} : {}'.format(k, v))
            print("  -- press 'p' to resume -- ")
        elif my_key == 112:     # 'p'
            if not paused:
                print('-paused-')
            paused = not paused
        elif my_key == 97:      # 'a'
            handset_uut.cmd_alcohol_test()
            print(' Alcohol Test Requested...')
        elif my_key == 122:      # 'z'
            capturing = False
            print(' Stop Capture...')
        elif my_key == 99:      # 'c'
            capturing = True
            print(' Start Capture...')
        elif my_key == 115:      # 's'
            handset_uut.cmd_go_sleep()
            print(' Handset Sleep Requested...')
        elif my_key == 114:      # 'r'
            print(' ' + str(handset_uut))
        elif my_key == 120:     # 'x'
            closeout()
        elif my_key == 27:      # <escape>
            print('Boo!')
        else:
            print("::{}::".format(my_key))


def closeout():
    # global log
    print('Closing log files and exiting.')
    log.close()
    handset_uut.close()
    sys.exit(1)


def main():
    global log
    global handset_uut

    # initialize UUT from commandline args
    handset_uut = FC250Handset(sys.argv[1], sys.argv[2])

    # setup results logging
    log = open(sys.argv[2]+'.csv', mode='a', buffering=1)
    #legend = 'time,fVoltageIn,fIoFcCaseTemperature,fIoUnitCaseTemperature,S/N,HandsetState,HeaterState,CellHeaterLevel'
    legend = 'time,BreathPressure,S/N,HandsetState,HeaterState'
    print(legend, file=log)

    try:
        while True:
            handle_keystrokes()
            if paused:
                continue
            poll(.039)

    except KeyboardInterrupt:
        closeout()

if __name__ == '__main__':
    main()
