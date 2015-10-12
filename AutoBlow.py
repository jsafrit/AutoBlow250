import struct
import datetime
import sys
from msvcrt import getch, kbhit
from FC250 import FC250Handset
from FC_protocol import HandsetState, HeaterState, PKT_PREAMBLE, BLOCK, PREAMBLE
import ftd2xx as ft
from time import time

log = None
handset_uut = None
my_relay = None
paused = False
capturing = False
start_time = time()
key_help = {'a': 'Alcohol Test request',
            'r': 'Report Handset info',
            's': 'Sleep Handset',
            'p': 'Pause/Resume status',
            'c': 'Start Capture',
            'z': 'Stop Capture',
            '?': 'This help menu',
            'x': 'Exit program'
            }
ALL_OFF = b'\000'
RELAY_ON = b'\001'


def hex_dump(data):
    return ''.join('{:02X}'.format(x) for x in data)


def poll(interval=1):
    incoming_packet = handset_uut.cmd_get_status(interval)
    if not incoming_packet:
        return

    # get the format of the status packet
    preamble = incoming_packet[PREAMBLE]
    layout_ver, *_ = struct.unpack('<B', preamble[4:5])

    # extract relevant data from packet
    block = incoming_packet[BLOCK]
    status_lookup = create_status_dict(block, layout_version=layout_ver)

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


def create_status_dict(block, layout_version=0):
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

    if layout_version in [7, 8]:
        # for F/W v1.17 or v1.23
        my_data3 = struct.unpack('<fHIiiBBBB', block[226:248])
    else:
        # for F/W v1.18
        my_data3 = struct.unpack('<fHIiiBBBB', block[230:252])

    lookup3 = dict(zip(my_labels3, my_data3))
    status_lookup = lookup.copy()
    status_lookup.update(lookup2)
    status_lookup.update(lookup3)
    return status_lookup


def handle_keystrokes(forced_key=None):
    global paused
    global capturing
    global start_time
    if kbhit() or forced_key:
        if not forced_key:
            my_key = ord(getch())
        else:
            my_key = forced_key

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
            start_time = time()
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
    my_relay.close()
    sys.exit(1)


def main():
    global log
    global handset_uut
    global my_relay
    global capturing

    # initialize UUT from commandline args
    handset_uut = FC250Handset(sys.argv[1], sys.argv[2])

    # initialize relay
    # open board and setup for Async BitBing Mode
    try:
        my_relay = ft.open(0)
    except ft.DeviceError:
        print('Cannot open device: {}'.format(ft.DeviceError))
        sys.exit(2)

    result = my_relay.setBitMode(0xFF, 0x1)
    if not result:
        print('Setup successful.')
        details = ft.getDeviceInfoDetail()
        print('Description: {}'.format(details['description'].decode()))
        my_relay.write(ALL_OFF)
    else:
        print('Failed to setup relay. Exiting...')
        sys.exit(3)

    # setup results logging
    log = open(sys.argv[2]+'.csv', mode='a', buffering=1)

    legend = 'time,BreathPressure,S/N,HandsetState,HeaterState'
    print(legend, file=log)

    last_capture_state = capturing
    relay_closed = False
    next_blow_time = time() + 60
    total_blows = 6

    try:
        while True:
            handle_keystrokes()
            if paused:
                continue
            if capturing:
                poll(.039)
            if relay_closed and delay_to_open:
                delay_to_open -= 1
            elif relay_closed:
                my_relay.write(ALL_OFF)
            if not last_capture_state and capturing:
                my_relay.write(RELAY_ON)
                relay_closed = True
                delay_to_open = 20
            last_capture_state = capturing

            current_time = time()
            if (current_time - start_time) > 5:
                capturing = False
                # if total_blows == 1:
                #     closeout()

            if current_time > next_blow_time:
                next_blow_time = time() + 35
                total_blows -= 1
                if total_blows:
                    handle_keystrokes(99)
                else:
                    closeout()

    except KeyboardInterrupt:
        closeout()


if __name__ == '__main__':
    main()
