import struct

# packet constants
STX = 2
ETX = 3
PACKET_MAGIC_NUMBER = 0xC613

# packet types
PRO_PKT_TYPE_HANDSET_STATUS = 3
PRO_PKT_TYPE_HANDSET_CALIBRATION = 4
PRO_PKT_TYPE_RELAY_STATUS = 5
PRO_PKT_TYPE_FACTORY = 6
PRO_PKT_TYPE_HANDSET_OPTIONS = 7
PRO_PKT_TYPE_RELAY_OPTION = 8
PRO_PKT_TYPE_USER = 9
PRO_PKT_TYPE_SERVICE = 10
PRO_PKT_TYPE_HANDSET_INSTALL = 11
PRO_PKT_TYPE_COMMAND = 12
PRO_PKT_TYPE_RELAY_COMMAND = 13
PRO_PKT_TYPE_EVENT_LOG_MASTER = 14
PRO_PKT_TYPE_EVT_LOG_DATA = 15
PRO_PKT_TYPE_HANDSET_ENGINEERING = 16
PRO_PKT_TYPE_SERVICE_PROVIDER = 17
PRO_PKT_TYPE_SLAVE_SPEAK = 18

# PRO_DEVICE_TYPE
PRO_FC200_HANDSET_DEVICE = 0
PRO_FC200_RELAY_DEVICE = 2
PRO_PC_ON_DSUCM_DEVICE = 3
PRO_PC_DEVICE = 5
PRO_HANDSET_BOOTLOADER_DEVICE = 10
PRO_BROADCAST_DEVICE = 11
PRO_RELAY_BOOTLOADER_DEVICE = 12
PRO_WIRELESS_CAMERA = 14
PRO_FC250_CAMERA_DEVICE = 22
PRO_CAMERA_BOOTLOADER_DEVICE = 23
PRO_FC250_HANDSET_DEVICE = 24
PRO_FC250_RELAY_DEVICE = 25
PRO_FC200_TEST_FIXTURE = 252
PRO_NULL_DEVICE = 253
PRO_LAST_DEVICE_TYPE = 255


def hex_dump(data):
    # return str.encode(data)
    return ' '.join('{:02x}'.format(x) for x in data)


def wrap_packet(block=b''):
    header = struct.pack('<BHB BLBL BHHH', STX, PACKET_MAGIC_NUMBER, PRO_PKT_TYPE_SLAVE_SPEAK,
                         PRO_PC_DEVICE, 0x01234567, PRO_FC250_HANDSET_DEVICE, 0x0,
                         0x0, 1080, 0x0, 0x0)
    # add block here

    packet_checksum = sum(header[1:]+block) % 0xFFFF
    footer = struct.pack('<HB', packet_checksum, ETX)
    # print(hex_dump(footer))
    # print('0x{:04x}'.format(packet_checksum))
    full_packet = header + footer
    return full_packet


if __name__ == '__main__':
    print(hex_dump(wrap_packet()))
