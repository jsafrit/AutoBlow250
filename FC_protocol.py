import struct
from enum import IntEnum

# packet constants
STX = 2
ETX = 3
PACKET_MAGIC_NUMBER = 0xC613


# packet types
class PacketType(IntEnum):
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
class DeviceType(IntEnum):
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
class ProCommands(IntEnum):
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


# handset state table    // const tStaStateTable sStaStateTable[] =
class HandsetState(IntEnum):
    STA_POWER_ON_RESET = 0
    STA_POWER_DOWN_GRAPHIC = 1
    STA_POWER_DOWN = 2
    STA_POWER_ON_HOLD_DOWN_BUTTON = 3
    STA_SERVICE_CODE_43 = 4
    STA_SERVICE_NO_BLOW_POSSIBLE = 5
    STA_ENTER_OVERRIDE_CODE = 6
    STA_INVALID_OVERRIDE_CODE = 7
    STA_POST_FC_CONTROL = 8
    STA_POWER_ON_WELCOME = 9
    STA_POWER_CHECK_LOW_CAR_BATTERY = 10
    STA_FLUTTER_PUMP = 11
    STA_SERVICE_DATE_REMINDER = 12
    STA_OVERRIDE_REMINDER = 13
    STA_MAIN_MENU = 14
    STA_SETTINGS = 15
    STA_HELP_CONTACT_INFO = 16
    STA_SERVICE_INFO = 17
    STA_WARMUP_SETTINGS = 18
    STA_EDIT_WARMUP_TIME = 19
    STA_WAIT_FOR_CALIBRATION_WARMUP = 20
    STA_WAIT_FOR_TEST_INTERVAL_CAL = 21
    STA_B4_CALIBRATION_BLOW_LOW_EMI = 22
    STA_WAIT_FOR_CALIBRATION_BLOW = 23
    STA_BLOWING_CALIBRATION = 24
    STA_WAIT_FOR_SOLENOID_CAL = 25
    STA_WAIT_FOR_CAL_PEAK = 26
    STA_WAIT_FOR_CAL_RESULTS = 27
    STA_LSA_CALIBRATION_COMPLETE = 28
    STA_FIGURE_CAL_RESULTS = 29
    STA_CALIBRATION_FAIL = 30
    STA_ABORT_BLOWING_CAL = 31
    STA_SELECT_USER = 32
    STA_ENTER_USER_PASSKEY = 33
    STA_INVALID_USER_PASSKEY = 34
    STA_INIT_BLOW = 35
    STA_INIT_TEST_CHECK_FAILS = 36
    STA_INIT_TEST = 37
    STA_WAIT_FOR_WARMUP = 38
    STA_B4_BLOW_LOW_EMI = 39
    STA_WAIT_FOR_BLOW = 40
    STA_WAIT_FOR_TARGET_DETECT = 41
    STA_LOW_CELL_SIGNAL = 42
    STA_BLOWING = 43
    STA_WAIT_FOR_SOLENOID = 44
    STA_WAIT_FOR_PEAK = 45
    STA_WAIT_FOR_RESULTS = 46
    STA_WAIT_FOR_SOLENOID_RELEASE = 47
    STA_PBT_RESULTS = 48
    STA_INVALID_SAMPLE = 49
    STA_PASS_DISP_WAIT = 50
    STA_INIT_ABORT_DISP_WAIT = 51
    STA_BLOWING_TIPS = 52
    STA_ABORT_DISP_WAIT = 53
    STA_RUN = 54
    STA_SERVICE = 55
    STA_DISPLAY_SERVICE_CODES = 56
    STA_LSA_ALCOHOL_TEST_RESULTS = 57
    STA_PBT_DISPLAY_DISCLAIMER = 58
    STA_PBT_INIT_TEST_CHECK_FAILS = 59
    STA_PBT_INIT_TEST = 60
    STA_PBT_WAIT_FOR_WARMUP = 61
    STA_PBT_B4_BLOW_LOW_EMI = 62
    STA_PBT_WAIT_FOR_BLOW = 63
    STA_PBT_BLOWING = 64
    STA_PBT_WAIT_FOR_SOLENOID = 65
    STA_PBT_WAIT_FOR_PEAK = 66
    STA_PBT_WAIT_FOR_RESULTS = 67
    STA_PBT_WAIT_FOR_SOLENOID_RELEASE = 68
    STA_PBT_BLOWING_TIPS = 69
    STA_PBT_ABORT_DISP_WAIT = 70
    STA_PBT_PBT_RESULTS = 71
    STA_CLST_LITHIUM_BATT = 72
    STA_CLST_REAL_TIME_CLK_PART = 73
    STA_CLST_REAL_TIME_CLK_XTAL = 74
    STA_CLST_FC_CONTINUITY = 75
    STA_CLST_FC_BASELINE = 76
    STA_CLST_FC_GAIN = 77
    STA_CLST_ABS_PRESS_SENS = 78
    STA_CLST_BREATH_TEMP = 79
    STA_CLST_CELL_TEMP = 80
    STA_CLST_UNIT_CASE_TEMP = 81
    STA_CLST_CASE_HEAT = 82
    STA_CLST_30V_BOOST = 83
    STA_CLST_COMMON_FAILSAFE = 84
    STA_CLST_PUMP = 85
    STA_CLST_FC_HEAT = 86
    STA_CLST_OLED_DISPLAY = 87
    STA_CLST_UI_I2C = 88
    STA_CLST_SSA_I2C = 89
    STA_CLST_FLASH_MEMORY = 90
    STA_CLST_3_3V_SWITCH = 91
    STA_CLST_DIFF_PRESS = 92
    STA_CLST_KEYPAD = 93
    STA_CLST_KEYPAD_LED = 94
    STA_CLST_SPEAKER = 95
    STA_CLST_VOLT_DIV = 96
    STA_CLST_PASSED = 97
    STA_CLST_FAILED = 98
    STA_ABIST_UI_I2C = 99
    STA_ABIST_SSA_I2C = 100
    STA_ABIST_RTC_BATT_SENSE = 101
    STA_ABIST_FLASH = 102
    STA_ABIST_RS485 = 103
    STA_ABIST_CASE_TEMP = 104
    STA_ABIST_BREATH_TEMP = 105
    STA_ABIST_CELL_TEMP = 106
    STA_ABIST_FC_TEST = 107
    STA_ABIST_3_3V_SWITCH = 108
    STA_ABIST_30V_PUMP_BOOST = 109
    STA_ABIST_DIFF_PRESSURE = 110
    STA_ABIST_ABSOLUTE_PRESSURE = 111
    STA_ABIST_SOLENOID = 112
    STA_ABIST_FAILSAFE = 113
    STA_ABIST_KEYPAD = 114
    STA_ABIST_OLED = 115
    STA_ABIST_SPEAKER = 116
    STA_ABIST_LEDS = 117
    STA_ABIST_VOLTAGE_DIVIDER = 118
    STA_ABIST_DISPLAY_RESULTS = 119
    STA_ABIST = 120
    STA_INVALID_STATE_ID = 121


# handset basic state table
class HandsetBasicState(IntEnum):
    PRO_HS_BASIC_STATE_RESERVED = 0
    PRO_HS_BASIC_STATE_POWER_DOWN = 1
    PRO_HS_BASIC_STATE_IDLE = 2
    PRO_HS_BASIC_STATE_WAIT_FOR_PUFF = 3
    PRO_HS_BASIC_STATE_CLEARING = 4
    PRO_HS_BASIC_STATE_WAIT_FOR_BLOW = 5
    PRO_HS_BASIC_STATE_BLOWING = 6
    PRO_HS_BASIC_STATE_ANALYZING = 7
    PRO_HS_BASIC_STATE_ABORT = 8
    PRO_HS_BASIC_STATE_DIAGNOSTIC = 9


def hex_dump(data):
    # return str.encode(data)
    return ' '.join('{:02x}'.format(x) for x in data)


def command_packet(command, detail1=0, detail2=0, detail3=0):
    header = struct.pack('<BHB BL BL BHHH',
                         STX, PACKET_MAGIC_NUMBER, PacketType.PRO_PKT_TYPE_COMMAND,
                         DeviceType.PRO_FC250_RELAY_DEVICE, 0x01234567,
                         DeviceType.PRO_FC250_HANDSET_DEVICE, 0x0,
                         0x0, 1080, 0x0, 23)

    block_preamble = struct.pack('<LBH', 0, 0, 23)
    block = block_preamble + struct.pack('<LLLL', command, detail1, detail2, detail3)

    packet_checksum = sum(header[1:] + block) % 0xFFFF
    footer = struct.pack('<HB', packet_checksum, ETX)

    full_packet = header + block + footer
    return full_packet


def wrap_packet(block=b''):
    header = struct.pack('<BHB BL BL BHHH',
                         STX, PACKET_MAGIC_NUMBER, PacketType.PRO_PKT_TYPE_SLAVE_SPEAK,
                         DeviceType.PRO_PC_DEVICE, 0x01234567,
                         DeviceType.PRO_FC250_HANDSET_DEVICE, 0x0,
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
    print(hex_dump(command_packet(ProCommands.PRO_REL_CMD_HANDSET_POWER)))
    print(hex_dump(command_packet(ProCommands.PRO_CMD_DO_HUMAN_ALCOHOL_TEST)))
    print(int(HandsetState.STA_POWER_DOWN))
    print(HandsetState(2).name)
    print(dir(HandsetState))
    print(HandsetBasicState(1).name)