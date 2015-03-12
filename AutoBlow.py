import serial


def hex_dump(data):
    return ' '.join('{:02X}'.format(x) for x in data)


def main():
    # print "press key"
    comm = 'COM80'
    my_comm = serial.Serial(comm, 921600, timeout=5, writeTimeout=5)
    print('Port opened: {}'.format(my_comm.isOpen()))

    r = input("prompt: ")
    print('done: (%s)' % r)


if __name__ == '__main__':
    main()
