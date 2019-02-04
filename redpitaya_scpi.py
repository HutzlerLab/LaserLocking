#! /usr/bin/python
"""SCPI access to Red Pitaya."""

#import socket
import time
import numpy as np
import math

class SCPI (object):
    """SCPI class used to access Red Pitaya over an IP network."""
    delimiter = '\r\n'

    def __init__(self, instrument, timeout_ms=15000):
        """Initialize object and open IP connection.
        Host IP should be a string in parentheses, like '192.168.1.100'.
        """
        self.rp = instrument
        self.rp.timeout = timeout_ms

    #     try:
    #         self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #         if timeout is not None:
    #             self._socket.settimeout(timeout)

    #         self._socket.connect((host, port))

    #     except socket.error as e:
    #         print('SCPI >> connect({!s:s}:{!s:d}) failed: {!s:s}'.format(host,port,e))

    # def __del__(self):
    #     if self._socket is not None:
    #         self._socket.close()
    #     self._socket = None

    def close(self):
        self.rp.close()

            # def rx_txt(self, chunksize = 4096):
    #     """Receive text string and return it after removing the delimiter."""
    #     msg = ''
    #     while 1:
    #         chunk = self._socket.recv(chunksize + len(self.delimiter)).decode('utf-8') # Receive chunk size of 2^n preferably
    #         msg += chunk
    #         if (len(chunk) and chunk[-2:] == self.delimiter):
    #             break
    #     return msg[:-2]


    # #NOT WORKING
    # def rx_arb(self):
    #     numOfBytes = 0
    #     """ Recieve binary data from scpi server"""
    #     str=''
    #     while (len(str) != 1):
    #         str = (self._socket.recv(1)).decode()
    #     #print(str)
    #     if not (str == '#'):
    #         return False
    #     #print(str)
    #     str=''
    #     while (len(str) != 1):
    #         str = (self._socket.recv(1)).decode()
    #     #print(str)
    #     numOfNumBytes = int(str)
    #     if not (numOfNumBytes > 0):
    #         return False
    #     str=''
    #     while (len(str) != numOfNumBytes):
    #         str += (self._socket.recv(1)).decode()
    #     #print(str)
    #     numOfBytes = int(str)
    #     str=''
    #     while (len(str) != numOfBytes):
    #         str += (self._socket.recv(1)).decode('utf-8','replace')
    #     #print(str)
    #     return str

    # def tx_txt(self, msg):
    #     """Send text string ending and append delimiter."""
    #     return self._socket.send((msg + self.delimiter).encode('utf-8'))

    # def txrx_txt(self, msg):
    #     """Send/receive text string."""
    #     self.rp.write(msg)
    #     return self.rx_txt()   

# Custom Acquisition Commands

    def getDecimation(self):
        decimation = self.rp.query('ACQ:DEC?')
        return int(decimation)

    def setDecimation(self, new_dec):
        self.rp.write('ACQ:DEC {}'.format(new_dec))
        return

    def enableAvg(self):
        avg = 'ON'
        self.rp.write('ACQ:AVG {}'.format(avg))

    def disableAvg(self):
        avg = 'OFF'
        self.rp.write('ACQ:AVG {}'.format(avg))

    def getAvgStatus(self):
        avg_status = self.rp.query('ACQ:AVG?')
        #print('Averaging status is {}'.format(avg_status))
        return avg_status

    def resetAcq(self):
        self.rp.write('ACQ:RST')
        return

    def stopAcq(self):
        self.rp.write('ACQ:STOP')
        return

    def startAcq(self):
        self.rp.write('ACQ:START')
        return

    def setTrigSource(self,source):
        self.rp.write('ACQ:TRIG {}'.format(source))
        return

    def getTrigStatus(self):
        trig_status = self.rp.query('ACQ:TRIG:STAT?')
        return trig_status

    def setTrigDelay(self, delay_samples):
        self.rp.write('ACQ:TRIG:DLY {}'.format(delay_samples))
        return

    def getTrigDelay(self):
        delay_samples = self.rp.query('ACQ:TRIG:DLY?')
        return int(delay_samples)

    def setTrigLevel(self, level_mV):
        self.rp.write('ACQ:TRIG:LEV {}'.format(level_mV/1000))
        return

    def getTrigLevel(self):
        level_V = self.rp.query('ACQ:TRIG:LEV?')
        level_mV = float(level_V)*1000
        #print('Trig level is {} mV'.format(level_mV))
        return level_mV

    def setInputLowV(self, channel):
        self.rp.write('ACQ:SOUR{}:GAIN LV'.format(channel))
        #print('Channel {} input setting is Low'.fomrat(channel))
        return

    def setInputHighV(self, channel):
        self.rp.write('ACQ:SOUR{}:GAIN HV'.format(channel))
        #print('Channel {} input setting is High'.fomrat(channel))
        return

    def setAcqUnitsVolts(self):
        self.rp.write('ACQ:DATA:UNITS VOLTS')
        #print('Acquisiton units set to volts')
        return

    def setAcqUnitsRaw(self):
        self.rp.write('ACQ:DATA:UNITS RAW')
        #print('Acquisition units set to raw')
        return

    def setDataFormatASCII(self):
        self.rp.write('ACQ:DATA:FORMAT ASCII')
        #print('Acquisition format set to ASCII')
        return

    def setDataFormatBinary(self):
        self.rp.write('ACQ:DATA:FORMAT BIN')
        #print('Acquisition format set to binary')
        return

    def getBuffSize(self):
        buff_size = self.rp.query('ACQ:BUF:SIZE?')
        #print('Buffer size is {} samples'.format(buff_size))
        return int(buff_size)

    def startAcq(self):
        self.rp.write('ACQ:START')

    def getAllRawData(self, channel):
        raw_data = self.rp.query('ACQ:SOUR{}:DATA?'.format(channel))
        return raw_data

    # Not Working
    def getASCIIData(self, channel):
        data_array = self.rp.query_ascii_values('ACQ:SOUR{}:DATA?'.format(channel))
        return data_array

    # Not Working
    def getBINData(self,channel):
        data_array = self.rp.query_binary_values('ACQ:SOUR{}:DATA?'.format(channel), datatype='h', container=np.array)
        return data_array

    def getLateRawData(self, channel, samples):
        raw_data = self.rp.query('ACQ:SOUR{}:DATA:LAT:N? {}'.format(channel,samples))
        return raw_data

    def getEarlyRawData(self,channel, samples):
        raw_data = self.rp.query('ACQ:SOUR{}:DATA:OLD:N? {}'.format(channel,samples))
        return raw_data

# Custom Output Commands

    def enableOutput(self, channel):
        self.rp.write('OUTPUT{}:STATE ON'.format(channel))
        return

    def disableOutput(self, channel):
        self.rp.write('OUTPUT{}:STATE OFF'.format(channel))
        return

    def setFreq(self, channel, frequency_Hz):
        self.rp.write('SOUR{}:FREQ:FIX {}'.format(channel, frequency_Hz))
        return

    def setWaveform(self, channel, waveform):
        self.rp.write('SOUR{}:FUNC {}'.format(channel,waveform))
        return

    def setAmplitude(self, channel, amplitude_volts):
        self.rp.write('SOUR{}:VOLT {}'.format(channel,amplitude_volts))
        return

    def setOffset(self,channel, offset_volts):
        self.rp.write('SOUR{}:VOLT:OFFS {}'.format(channel, offset_volts))
        return

    def setPhase(self, channel, phase_deg):
        self.rp.write('SOUR{}:PHAS {}'.format(channel, phase_deg))
        return

    def setDutyCycle(self,channel,duty_percent):
        self.rp.write('SOUR{}:DCYC {}'.format(channel,duty_percent))
        return

    def setArbWaveform(self, channel, array):
        self.rp.write('SOUR{}:TRAC:DATA:DATA {}'.format(channel, array))
        return

    def enableBurstMode(self, channel):
        self.rp.write('SOUR{}:BURS:STAT ON'.format(channel))
        return

    def disableBurstMode(self, channel):
        self.rp.write('SOUR{}:BURS:STAT OFF'.format(channel))
        return

    def setBurstCount(self, channel, cycles_per_burst):
        self.rp.write('SOUR{}:BURS:NCYC {}'.format(channel, cycles_per_burst))
        return

    def setBurstRep(self, channel, num_of_bursts):
        self.rp.write('SOUR{}:BURS:NOR {}'.format(channel, num_of_bursts))
        return

    def setGenTriggerSrc(self, channel, trig_src):
        self.rp.write('SOUR{}:TRIG:SOUR {}'.format(channel, trig_src))
        return

    def trigImmediately(self, channel):
        self.rp.write('SOUR{}:TRIG:IMM'.format(channel))
        return

    def trigAllImmediately(self):
        self.rp.write('TRIG:IMM')
        return

    def resetOutput(self):
        self.rp.write('GEN:RST')
        return

# LED Commands
    
    def turnOnLED(self, num):
        self.rp.write('DIG:PIN LED{},1'.format(num))
        return

    def turnOffLED(self,num):
        self.rp.write('DIG:PIN LED{},0'.format(num))
        return

    def turnOnAllLED(self):
        for i in range(8):
            self.turnOnLED(i)
        return

    def turnOffAllLED(self):
        for i in range(8):
            self.turnOffLED(i)
        return

    def flashAllLED(self,t_flash = 0.5):
        self.turnOnAllLED()
        time.sleep(t_flash)
        self.turnOffAllLED()
        return


# IEEE Mandated Commands

    def cls(self):
        """Clear Status Command"""
        return self.rp.write('*CLS')

    def ese(self, value: int):
        """Standard Event Status Enable Command"""
        return self.rp.write('*ESE {}'.format(value))

    def ese_q(self):
        """Standard Event Status Enable Query"""
        return self.rp.query('*ESE?')

    def esr_q(self):
        """Standard Event Status Register Query"""
        return self.rp.query('*ESR?')

    def idn_q(self):
        """Identification Query"""
        return self.rp.query('*IDN?')

    def opc(self):
        """Operation Complete Command"""
        return self.rp.write('*OPC')

    def opc_q(self):
        """Operation Complete Query"""
        return self.rp.query('*OPC?')

    def rst(self):
        """Reset Command"""
        return self.rp.write('*RST')

    def sre(self):
        """Service Request Enable Command"""
        return self.rp.write('*SRE')

    def sre_q(self):
        """Service Request Enable Query"""
        return self.rp.query('*SRE?')

    def stb_q(self):
        """Read Status Byte Query"""
        return self.rp.query('*STB?')

# :SYSTem

    def err_c(self):
        """Error count."""
        return self.rp.query('SYST:ERR:COUN?')

    def err_c(self):
        """Error next."""
        return self.rp.query('SYST:ERR:NEXT?')



