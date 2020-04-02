'''
    Pyserial Class:
    https://pythonhosted.org/pyserial/pyserial_api.html#classes
    
    __init__(port=None, baudrate=9600, bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=False, inter_byte_timeout=None)
    
    Parameters:	
        port – Device name or None.
        baudrate (int) – Baud rate such as 9600 or 115200 etc.
        bytesize – Number of data bits. Possible values: FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS
        parity – Enable parity checking. Possible values: PARITY_NONE, PARITY_EVEN, PARITY_ODD PARITY_MARK, PARITY_SPACE
        stopbits – Number of stop bits. Possible values: STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO
        timeout (float) – Set a read timeout value.
        xonxoff (bool) – Enable software flow control.
        rtscts (bool) – Enable hardware (RTS/CTS) flow control.
        dsrdtr (bool) – Enable hardware (DSR/DTR) flow control.
        write_timeout (float) – Set a write timeout value.
        inter_byte_timeout (float) – Inter-character timeout, None to disable (default).
    Raises:	
        ValueError – Will be raised when parameter are out of range, e.g. baud rate, data bits.
        SerialException – In case the device can not be found or can not be configured.
'''

import serial

ser = serial.Serial('COM1')

print('端口名： ' + ser.name)
print('端口： ' + ser.port)
print()

print('串口默认配置：')
print('baudrate 波特率： ' + str(ser.baudrate))
print('bytesize 位宽： ' + str(ser.bytesize))
print('parity 校验位： ' + str(ser.parity))
print('stopbits 停止位： ' + str(ser.stopbits))
print('timeout 读超时： ' + str(ser.timeout))
print('writeTimeout 写超时： ' + str(ser.writeTimeout))
print('xonxoff 软件流控： ' + str(ser.xonxoff))
print('rtscts 硬件流控 RTS： ' + str(ser.rtscts))
print('dsrdtr 硬件流控 CTS： ' + str(ser.dsrdtr))
print('interCharTimeout 字符间隔超时： ' + str(ser.interCharTimeout))

# ser.open()
ser.flushOutput()
# ser.reset_output_buffer()
ser.write(b'hello\r\n')
ser.write(b'hello\r\n')
ser.write(b'hello\r\n')
ser.write(b'hello\r\n')
ser.write(b'hello\r\n')
ser.write(b'hello\r\n')
ser.close()