import ftd2xx as ft
import time
import struct
import sys


ALL_OFF = b'\000'


list_of_devices = ft.listDevices()
for i, d in enumerate(list_of_devices):
    print('{}: {}'.format(i, d.decode()))
index = input('Select relay device: ')

try:
    relay_board_index = int(index)
except ValueError:
    print('Value Error: Not a valid relay.')
    sys.exit(1)

# # find the first relay board
# for device in list_of_devices:
#     if device.decode().startswith('A'):
#         print('Found one: : {}'.format(device.decode()))
#         relay_board_index = list_of_devices.index(device)
#         break
#     else:
#         print('Nope')

# open board and setup for Async BitBing Mode
try:
    my_relay = ft.open(relay_board_index)
except ft.DeviceError:
    print('Cannot open device: {}'.format(ft.DeviceError))
    sys.exit(2)

result = my_relay.setBitMode(0xFF, 0x1)
if not result:
    print('Setup successful.')
    details = ft.getDeviceInfoDetail()
    print('Description: {}'.format(details['description'].decode()))
else:
    print('Failed to setup relay. Exiting...')
    sys.exit(3)

delay = 1
for out in range(4):
    send = struct.pack('B', out)
    my_relay.write(send)
    time.sleep(delay)

time.sleep(5)
my_relay.write(ALL_OFF)

my_relay.close()


# ul = c_ulong()
# pul = pointer(ul)
#
# lib_ftdi = WinDLL('ftd2xx')
# print('List devices...')
# c = c_ulong(0x80000000)
# result = lib_ftdi.FT_ListDevices(pul, None, c)
# if not result:
#     print('Devices found:', ul.value)
# else:
#     print('No devices found')
#
# print('\nOpening...')
# my_relay = c_int(2)
# print('Result:', lib_ftdi.FT_Open(my_relay, pul))
# print(ul)
#
# print(lib_ftdi.FT_CreateDeviceInfoList(pul))
# print(ul)