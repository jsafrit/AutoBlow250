import serial
import time
from FC_protocol import wrap_packet

# Handset Status Packet Blocks
PKT_PREAMBLE = slice(0, 21)
PREAMBLE = slice(21, 28)
BLOCK = slice(28, -3)
FOOTER = slice(-3, None)


def hex_dump(data):
    return ''.join('{:02X}'.format(x) for x in data)


def main():
    # print "press key"
    comm = 'COM80'
    my_comm = serial.Serial(comm, 921600, timeout=5, writeTimeout=5)
    print('Port opened: {}'.format(my_comm.isOpen()))

    my_comm.write(wrap_packet())

    time.sleep(1)

    incoming_bytes = my_comm.inWaiting()
    while not incoming_bytes:
        incoming_bytes = my_comm.inWaiting()

    incoming_packet = my_comm.read(incoming_bytes)
    print('Packet length: {}'.format(len(incoming_packet)))
    # print(hex_dump(incoming_packet))
    print('{:16}'.format('Packet Preamble:'), end='')
    print(hex_dump(incoming_packet[PKT_PREAMBLE]))
    print('{:16}'.format('Preamble: '), end='')
    print(hex_dump(incoming_packet[PREAMBLE]))
    print('{:16}'.format('Block: '), end='')
    print(hex_dump(incoming_packet[BLOCK]))
    print('{:16}'.format('Footer: '), end='')
    print(hex_dump(incoming_packet[FOOTER]))


if __name__ == '__main__':
    main()
