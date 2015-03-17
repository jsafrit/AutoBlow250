import serial
import time
from FC_protocol import wrap_packet


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
    print(hex_dump(incoming_packet))
    print(len(incoming_packet))


if __name__ == '__main__':
    main()
