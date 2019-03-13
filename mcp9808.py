#!/usr/bin/python3

# standard Python Libraries


# GPIO Libraries

# Adafruit Blinka Libraries
import board
import busio
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_bit import RWBit
from adafruit_register.i2c_bit import ROBit
from adafruit_register.i2c_bits import RWBits
from adafruit_register.i2c_bits import ROBits

# Adafruit Sensor Libraries
#import adafruit_mcp9808

I2CBUS = busio.I2C(board.SCL, board.SDA)
#SENSOR = adafruit_mcp9808.MCP9808(I2CBUS)

DEVICE_ADDRESS = 0x18
DEVICE_CONFIG_REG = 0x01
DEVICE_UPPER_TEMP_REG = 0x02
DEVICE_LOWER_TEMP_REG = 0x03
DEVICE_CRIT_TEMP_REG = 0x04
DEVICE_TEMP_REG = 0x05

device = I2CDevice(I2CBUS, DEVICE_ADDRESS)

class TempSensor:
    def __init__(self, i2c):
        self.i2c_device = i2c

    alert_output_mode = RWBit(DEVICE_CONFIG_REG, 0, 2)
    alert_output_polarity = RWBit(DEVICE_CONFIG_REG, 1, 2)
    alert_output_select = RWBit(DEVICE_CONFIG_REG, 2, 2)
    alert_output_control = RWBit(DEVICE_CONFIG_REG, 3, 2)
    alert_output_status = RWBit(DEVICE_CONFIG_REG, 4, 2)
    interrupt_clear = RWBit(DEVICE_CONFIG_REG, 5, 2)
    win_lock = RWBit(DEVICE_CONFIG_REG, 6, 2)
    crit_loc = RWBit(DEVICE_CONFIG_REG, 7, 2)

    temp_value = ROBits(12, DEVICE_TEMP_REG, 0, 2)
    temp_crit_flag = ROBit(DEVICE_TEMP_REG, 15,2)
    temp_upper_flag = ROBit(DEVICE_TEMP_REG, 14, 2)
    temp_lower_flag = ROBit(DEVICE_TEMP_REG, 13, 2)
    
    temp_upper_value = RWBits(11, DEVICE_UPPER_TEMP_REG, 2, 2)
    
    temp_lower_value = RWBits(11, DEVICE_LOWER_TEMP_REG, 2, 2)

    temp_crit_value = RWBits(11, DEVICE_CRIT_TEMP_REG, 2, 2)

def Dump_Registers():
    print('MCP9808 Config register settings: 0x01')
    print('bit 0 - alert output mode: {}'.format(config.alert_output_mode))
    print('bit 1 - alert output polarity: {}'.format(config.alert_output_polarity))
    print('bit 2 - alert output select: {}'.format(config.alert_output_select))
    print('bit 3 - alert output control: {}'.format(config.alert_output_control))
    print('bit 4 - alert output status: {}'.format(config.alert_output_status))
    print('bit 5 - interrupt clear: {}'.format(config.interrupt_clear))
    print('bit 6 - Window Lock: {}'.format(config.win_lock))
    print('bit 7 - Critical Lock: {}'.format(config.crit_loc))
    print(' ')

    print('MCP9808 Temp register settings: 0x05')
    print('temp value: {}'.format(config.temp_value))
    print('temp crit flag: {}'.format(config.temp_crit_flag))
    print('temp upper flag: {}'.format(config.temp_upper_flag))
    print('temp lower flag : {}'.format(config.temp_lower_flag))
    print(' ')
    print('MCP9808 Upper Temp register settings: 0x02')
    print('upper temp: {}'.format(config.temp_upper_value))
    print(' ')
    print('MCP9808 Lower Temp register settings: 0x03')
    print('lower temp: {}'.format(config.temp_lower_value))
    print(' ')
    print('MCP9808 Crit Temp register settings: 0x04')
    print('crit temp: {}'.format(config.temp_crit_value))

def temp_c(data):
    value = data[0] << 8 | data[1]
    temp = (value & 0xFFF) / 16.0
    if value & 0x1000:
        temp -= 256.0
    return temp

##### Main #####

config = TempSensor(device)

print(' ')
print('initial reg values')
print(' ')
Dump_Registers()
print(' ')
if (I2CBUS.try_lock()):
    I2CBUS.writeto(0x018, bytes([0x05]), stop=False)
    result = bytearray(2)
    I2CBUS.readfrom_into(0x18, result)
    temp1 = temp_c(result)
    I2CBUS.unlock()
else:
    temp1 = 'no value'
    print('lock failed')
print('temp reading: {}'.format(temp1))
print(' ')
print('setting config alert output control')

config.alert_output_mode = 1
config.alert_output_polarity = 1
config.alert_output_select = 1
config.alert_output_control = 1
config.alert_output_status = 1
config.interrupt_clear = 1
config.win_lock = 1
config.crit_loc = 1
print(' ')
print('setting upper to 7*c')
print('upper temp before : {}'.format(config.temp_upper_value))
config.temp_upper_value = 7
print('upper temp after: {}'.format(config.temp_upper_value))
print(' ')
print('setting lowwer to 8*c')
print('lower temp before: {}'.format(config.temp_lower_value))
config.temp_lower_value = 8
print('lower temp after: {}'.format(config.temp_lower_value))
print(' ')
print('reg values after changes')
print(' ')
Dump_Registers()
