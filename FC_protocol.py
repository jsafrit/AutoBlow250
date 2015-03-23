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

# Commands
PRO_CMD_NOP = 0
PRO_CMD_TAKE_IGN_ALC_TEST = 1
PRO_CMD_SLEEP = 3
PRO_CMD_BEGIN_LOW_POWER = 4
PRO_CMD_BEGIN_WARMUP = 5
PRO_CMD_DO_BIST_FUNCTION = 6
PRO_CMD_DO_CLST_FUNCTION = 7
PRO_CMD_READ_HANDSET_STATUS_PKT = 8
PRO_CMD_READ_CALIBRATION_PKT = 9
PRO_CMD_READ_HANDSET_OPTIONS_PKT = 10
PRO_CMD_READ_RELAY_OPTIONS_PKT = 11
PRO_CMD_READ_RELAY_STATUS_PKT = 12
PRO_CMD_READ_EVENT_LOG_DATA_PKT = 13
PRO_CMD_CLEAR_EVENT_LOG_DATA = 14
PRO_CMD_FORMAT_FLASH = 15
PRO_CMD_BEGIN_PWR_ON_SELF_TEST = 16
PRO_CMD_WRITE_HANDSET_OPTIONS_PKT = 17
PRO_CMD_WRITE_RELAY_OPTIONS_PKT = 18
PRO_CMD_READ_DATES_PKT = 19
PRO_CMD_READ_SERVICE_PROVIDER_PKT = 20
PRO_CMD_READ_HANDSET_ENGINEERING_PKT = 21
PRO_CMD_READ_FACTORY_PKT = 22
PRO_CMD_READ_USER_PKT = 23
PRO_CMD_READ_EVT_LOG_MASTER_PKT = 24
PRO_CMD_REQUEST_CONNECTION = 25
PRO_CMD_RESET_GRACE_PERIODS = 26
PRO_CMD_STOP_SENDING_EVENT_DATA = 27
PRO_CMD_DO_WET_BATH_SIMULATOR_TEST = 28
PRO_CMD_DO_HUMAN_ALCOHOL_TEST = 29
PRO_CMD_DO_WET_BATH_CALIBRATION = 30
PRO_CMD_STOP_SENDING_BINARY_BLOCKS = 31
PRO_CMD_READ_APP_DESCRIPTOR_PKT = 32
PRO_CMD_ERASE_APPLICATION = 33
PRO_CMD_ZAP_DATES_PKT = 34
PRO_CMD_ZAP_SERVICE_PROVIDER_PKT = 35
PRO_CMD_ZAP_HANDSET_ENGINEERING_PKT = 36
PRO_CMD_ZAP_FACTORY_PKT = 37
PRO_CMD_ZAP_USER_PKT = 38
PRO_CMD_ZAP_EVT_LOG_MASTER_PKT = 39
PRO_CMD_ZAP_HANDSET_OPTIONS_PKT = 40
PRO_CMD_READ_MULTIPLE_PKTS = 41
PRO_CMD_DO_WET_BATH_HOT_CAL_ADJUST = 42
PRO_CMD_DO_WET_BATH_COLD_CAL_ADJUST = 43
PRO_CMD____UNUSED___ = 44
PRO_CMD_TEST_WDT = 45
PRO_CMD_HS_FORMAT_FLASH = 46
PRO_CMD_HS_CAL_STORE_CONVERGENCE = 47
PRO_CMD_HS_SET_FC_RESISTORS = 48
PRO_CMD_HS_GET_ALC_RESPONSE_PLOTS = 49
PRO_CMD_HS_TEST_LOW_POWER_COMPATIBILITY = 50
PRO_CMD_ZAP_CALIBRATION_PKT = 51
PRO_CMD_RESET_HOT_CAL_MODEL = 52
PRO_CMD_RESET_COLD_CAL_MODEL = 53
PRO_CMD_UPDATE_MODEL_COFS = 54
PRO_CMD_HS_OVERRIDE_CAL = 55
PRO_CMD_HS_SET_IR_LED = 56
PRO_CMD_HS_DRIVE_CAM_ABORT = 57
PRO_CMD_CLR_FAILED = 58
PRO_CMD_UPDATE_CAL_MODEL = 59
PRO_CMD_READ_BINARY_IMAGE_PKT = 60
PRO_CMD_RESET = 61
PRO_CMD_SET_INTERVAL = 62
PRO_CMD_ENGINEERING_TEST = 63
PRO_CMD_SET_HIGH_CLIMATIC_FAC = 64
PRO_CMD_READ_TEMP_HISTOGRAM = 65
PRO_CMD_ZAP_TEMP_HISTOGRAM = 66
PRO_CMD_READ_VOLTAGE_HISTOGRAM = 67
PRO_CMD_ZAP_VOLTAGE_HISTOGRAM = 68
PRO_CMD_FORMAT_HS_SD_CARD = 69
PRO_CMD_HS_DOWNLOAD_IMAGES = 70
PRO_CMD_HS_ACK_LAST_PACKET = 71
PRO_CMD_READ_BLOW_PKT = 72
PRO_CMD_READ_FC_ANALYSIS_PACKET = 73
PRO_CMD_READ_INFO_PKT = 74
PRO_REL_CMD_NOP = 100
PRO_REL_CMD_OPEN_STARTER_RELAY = 101
PRO_REL_CMD_CLOSE_HORN_RELAY = 102
PRO_REL_CMD_OPEN_HORN_RELAY = 103
PRO_REL_CMD_CLOSE_LIGHT_RELAY = 104
PRO_REL_CMD_OPEN_LIGHT_RELAY = 105
PRO_REL_CMD_CLEAR_FOR_FREE_START = 106
PRO_REL_CMD_END_STALL_PROTECT = 107
PRO_REL_CMD_START_SOUND = 108
PRO_REL_CMD_END_SOUND = 109
PRO_REL_CMD_READ_EVENT_LOG_DATA_PKT = 110
PRO_REL_CMD_READ_EVT_LOG_MASTER_PKT = 111
PRO_REL_CMD_CLEAR_EVENT_LOG_DATA = 112
PRO_REL_CMD_CLOSE_STARTER_RELAY = 113
PRO_REL_CMD_TEST_LOW_POWER_COMPATIBILITY = 114
PRO_REL_CMD_READ_RELAY_OPTIONS_PKT = 115
PRO_REL_CMD_READ_RELAY_STATUS_PKT = 116
PRO_REL_CMD_FORMAT_FLASH = 117
PRO_REL_CMD_WRITE_RELAY_OPTIONS_PKT = 118
PRO_REL_CMD_READ_DATES_PKT = 119
PRO_REL_CMD_READ_FACTORY_PKT = 120
PRO_REL_CMD_READ_USER_PKT = 121
PRO_REL_CMD_CAMERA_POWER = 122
PRO_REL_CMD_READ_HANDSET_OPTIONS_PKT = 123
PRO_REL_CMD_READ_HANDSET_STATUS_PKT = 124
PRO_REL_CMD_READ_ENGINEERING_PKT = 125
PRO_REL_CMD_READ_CALIBRATION_DATA = 126
PRO_REL_CMD_GENERATE_EVENTS = 127
PRO_REL_CMD_READ_CLIENT_OPTIONS_PKT = 128
PRO_REL_CMD_READ_SERVICE_PROVIDER_PKT = 129
PRO_REL_CMD_READ_HISTORY_LOG_PKT = 130
PRO_REL_CMD_ZAP_HISTORY_LOG_PKT = 131
PRO_REL_CMD_ZAP_DATES_PKT = 132
PRO_REL_CMD_CLEAR_FAILURE_FLAGS = 133
PRO_REL_CMD_OPEN_HEARING_IMPARED_RELAY = 134
PRO_REL_CMD_CLOSE_HEARING_IMPARED_RELAY = 135
PRO_REL_CMD_ZAP_RELAY_STATUS = 136
PRO_REL_CMD_HANDSET_POWER = 137
PRO_CAM_CMD_POWER = 200
PRO_CAM_CMD_CLEAR_EVENT_IMAGES = 201
PRO_CAM_CMD_CLEAR_CLIENT_IMAGE = 202
PRO_CAM_CMD_RESET = 203
PRO_CAM_CMD_SET_LED = 204
PRO_CAM_CMD_STORE_EVENT_IMAGE = 205
PRO_CAM_CMD_STORE_CLIENT_IMAGE = 206
PRO_CAM_CMD_ACQUIRE_IMAGE = 207
PRO_CAM_CMD_READ_IMAGE_INFO_PKT = 208
PRO_CAM_CMD_READ_IMAGE_DATA_PKT = 209
PRO_CAM_CMD_READ_CAMERA_STATUS_PKT = 210
PRO_CAM_CMD_LEGACY_ACK_LAST_PACKET = 11
PRO_CAM_CMD_ACK_LAST_PACKET = 211
PRO_CAM_CMD_NETWORK_DISCONNECT = 212
PRO_CAM_CMD_PROVISION_CELL_CHIP = 213
PRO_CAM_CMD_PLAY_AUDIO = 214
PRO_CAM_CMD_ERASE_AUDIO = 215
PRO_CAM_CMD_WRITE_AUDIO = 216
PRO_CAM_CMD_READ_FACTORY_PKT = 217
PRO_CAM_CMD_READ_ENGINEERING_PKT = 218
PRO_CAM_CMD_PLAY_TONE = 219
PRO_CAM_CMD_PLAY_PHRASE = 220
PRO_CAM_CMD_SET_MODE = 221
PRO_CAM_CMD_DETECT_TARGET = 222
PRO_CAM_CMD_TRACK_TARGET = 223
PRO_CAM_CMD_START_WDMS_CLIENT = 224
PRO_CAM_CMD_DOWNLOAD_EVENT_LOG_DATA = 225
PRO_CAM_CMD_DOWNLOAD_IMAGES = 226
PRO_CAM_CMD_ZAP_STATUS = 227
PRO_CAM_CMD_ALCOHOL_TEST = 228
PRO_CAM_CMD_SET_EARLY_RECALL = 229
PRO_CAM_CMD_SET_DAC_VALUE = 230
PRO_CAM_CMD_BEGIN_CLST = 231
PRO_CAM_CMD_WDMS_SET_PORT = 232
PRO_CAM_CMD_CLEAR_EARLY_RECALL = 233
PRO_CAM_CMD_READ_ADDON_OPTIONS = 234
PRO_CAM_CMD_DOWNLOAD_EVENT_LOG_MASTER = 235
PRO_CAM_CMD_ZAP_OPTIONS = 236
PRO_CAM_CMD_READ_OPTIONS_PKT = 237
PRO_CAM_CMD_CANCEL_DOWNLOAD = 238
PRO_CAM_CMD_CRAM_IMAGES = 239
PRO_HMB_CMD_NOP = 300
PRO_HMB_CMD_READ_DEVICE_OPTIONS_PKT = 301
PRO_HMB_CMD_READ_STATUS_PKT = 302
PRO_HMB_CMD_READ_DATES_PKT = 303
PRO_HMB_CMD_READ_CLIENT_OPTIONS_PKT = 304
PRO_HMB_CMD_SET_LED = 305
PRO_HMB_CMD_SET_POWER = 306
PRO_HMB_CMD_ZAP_CLIENT_OPTIONS_PKT = 307
PRO_HMB_CMD_ZAP_FACTORY_PKT = 308
PRO_HMB_CMD_ZAP_HMB_STATUS_PKT = 309
PRO_HMB_CMD_CLEAR_MEMORY = 310
PRO_HMB_CMD_RESET = 311
PRO_HMB_CMD_BEGIN_CLST = 312


def hex_dump(data):
    # return str.encode(data)
    return ' '.join('{:02x}'.format(x) for x in data)


def command_packet(command, detail1=0, detail2=0, detail3=0):
    header = struct.pack('<BHB BLBL BHHH', STX, PACKET_MAGIC_NUMBER, PRO_PKT_TYPE_COMMAND,
                         PRO_FC250_RELAY_DEVICE, 0x01234567, PRO_FC250_HANDSET_DEVICE, 0x0,
                         0x0, 1080, 0x0, 23)
    preamble = struct.pack('<LBH', 0, 0, 23)

    # add block here
    block = struct.pack('<LLLL', command, detail1, detail2, detail3)

    packet_checksum = sum(header[1:] + preamble + block) % 0xFFFF
    footer = struct.pack('<HB', packet_checksum, ETX)
    # print(hex_dump(footer))
    # print('0x{:04x}'.format(packet_checksum))
    full_packet = header + preamble + block + footer
    return full_packet


def wrap_packet(block=b''):
    header = struct.pack('<BHB BLBL BHHH', STX, PACKET_MAGIC_NUMBER, PRO_PKT_TYPE_SLAVE_SPEAK,
                         PRO_PC_DEVICE, 0x01234567, PRO_FC250_HANDSET_DEVICE, 0x0,
                         0x0, 1080, 0x0, 0x0)
    # add block here

    packet_checksum = sum(header[1:] + block) % 0xFFFF
    footer = struct.pack('<HB', packet_checksum, ETX)
    # print(hex_dump(footer))
    # print('0x{:04x}'.format(packet_checksum))
    full_packet = header + footer
    return full_packet


if __name__ == '__main__':
    print(hex_dump(wrap_packet()))
    print(hex_dump(command_packet(PRO_REL_CMD_HANDSET_POWER)))