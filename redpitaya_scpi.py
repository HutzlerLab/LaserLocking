#! /usr/bin/python
"""SCPI access to Red Pitaya."""

import socket
import time
import numpy as np
import math

__author__ = "Luka Golinar and Iztok Jeras made the SCPI class. Arian Jadbabaie modified the SCPI class."

class SCPI (object):
    """SCPI class used to access Red Pitaya over an IP network."""
    delimiter = '\r\n'

    def __init__(self, host, timeout=15, port=5000):
        """Initialize object and open IP connection.
        Host IP should be a string in parentheses, like '192.168.1.100'.
        """
        self.host    = host
        self.port    = port
        self.timeout = timeout

        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            if timeout is not None:
                self._socket.settimeout(timeout)

            self._socket.connect((host, port))

        except socket.error as e:
            print('SCPI >> connect({!s:s}:{!s:d}) failed: {!s:s}'.format(host,port,e))

    def __del__(self):
        if self._socket is not None:
            self._socket.close()
        self._socket = None

    def close(self):
        """Close IP connection."""
        self.__del__()

    def rx_txt(self, chunksize = 4096):
        """Receive text string and return it after removing the delimiter."""
        msg = ''
        while 1:
            chunk = self._socket.recv(chunksize + len(self.delimiter)).decode('utf-8') # Receive chunk size of 2^n preferably
            msg += chunk
            if (len(chunk) and chunk[-2:] == self.delimiter):
                break
        return msg[:-2]


    #NOT WORKING
    def rx_arb(self):
        numOfBytes = 0
        """ Recieve binary data from scpi server"""
        str=''
        while (len(str) != 1):
            str = (self._socket.recv(1)).decode()
        #print(str)
        if not (str == '#'):
            return False
        #print(str)
        str=''
        while (len(str) != 1):
            str = (self._socket.recv(1)).decode()
        #print(str)
        numOfNumBytes = int(str)
        if not (numOfNumBytes > 0):
            return False
        str=''
        while (len(str) != numOfNumBytes):
            str += (self._socket.recv(1)).decode()
        #print(str)
        numOfBytes = int(str)
        str=''
        while (len(str) != numOfBytes):
            str += (self._socket.recv(1)).decode('utf-8','replace')
        #print(str)
        return str

    def tx_txt(self, msg):
        """Send text string ending and append delimiter."""
        return self._socket.send((msg + self.delimiter).encode('utf-8'))

    def txrx_txt(self, msg):
        """Send/receive text string."""
        self.tx_txt(msg)
        return self.rx_txt()

# Custom Acquisition Commands

    def getDecimation(self):
        decimation = self.txrx_txt('ACQ:DEC?')
        return int(decimation)

    def setDecimation(self, new_dec):
        self.tx_txt('ACQ:DEC {}'.format(new_dec))
        return

    def enableAvg(self):
        avg = 'ON'
        self.tx_txt('ACQ:AVG {}'.format(avg))

    def disableAvg(self):
        avg = 'OFF'
        self.tx_txt('ACQ:AVG {}'.format(avg))

    def getAvgStatus(self):
        avg_status = self.txrx_txt('ACQ:AVG?')
        #print('Averaging status is {}'.format(avg_status))
        return avg_status

    def resetAcq(self):
        self.tx_txt('ACQ:RST')
        return

    def stopAcq(self):
        self.tx_txt('ACQ:STOP')
        return

    def startAcq(self):
        self.tx_txt('ACQ:START')
        return

    def setTrigSource(self,source):
        self.tx_txt('ACQ:TRIG {}'.format(source))
        return

    def getTrigStatus(self):
        trig_status = self.txrx_txt('ACQ:TRIG:STAT?')
        return trig_status

    def setTrigDelay(self, delay_samples):
        self.tx_txt('ACQ:TRIG:DLY {}'.format(delay_samples))
        return

    def getTrigDelay(self):
        delay_samples = self.txrx_txt('ACQ:TRIG:DLY?')
        return int(delay_samples)

    def setTrigLevel(self, level_mV):
        self.tx_txt('ACQ:TRIG:LEV {}'.format(level_mV/1000))
        return

    def getTrigLevel(self):
        level_V = self.txrx_txt('ACQ:TRIG:LEV?')
        level_mV = float(level_V)*1000
        #print('Trig level is {} mV'.format(level_mV))
        return level_mV

    def setInputLowV(self, channel):
        self.tx_txt('ACQ:SOUR{}:GAIN LV'.format(channel))
        #print('Channel {} input setting is Low'.fomrat(channel))
        return

    def setInputHighV(self, channel):
        self.tx_txt('ACQ:SOUR{}:GAIN HV'.format(channel))
        #print('Channel {} input setting is High'.fomrat(channel))
        return

    def setAcqUnitsVolts(self):
        self.tx_txt('ACQ:DATA:UNITS VOLTS')
        #print('Acquisiton units set to volts')
        return

    def setAcqUnitsRaw(self):
        self.tx_txt('ACQ:DATA:UNITS RAW')
        #print('Acquisition units set to raw')
        return

    def setDataFormatASCII(self):
        self.tx_txt('ACQ:DATA:FORMAT ASCII')
        #print('Acquisition format set to ASCII')
        return

    def setDataFormatBinary(self):
        self.tx_txt('ACQ:DATA:FORMAT BIN')
        #print('Acquisition format set to binary')
        return

    def getBuffSize(self):
        buff_size = self.txrx_txt('ACQ:BUF:SIZE?')
        #print('Buffer size is {} samples'.format(buff_size))
        return int(buff_size)

    def startAcq(self):
        self.tx_txt('ACQ:START')

    def getAllRawData(self, channel):
        raw_data = self.txrx_txt('ACQ:SOUR{}:DATA?'.format(channel))
        return raw_data

    def getLateRawData(self, channel, samples):
        raw_data = self.txrx_txt('ACQ:SOUR{}:DATA:LAT:N? {}'.format(channel,samples))
        return raw_data

    def getEarlyRawData(self,channel, samples):
        raw_data = self.txrx_txt('ACQ:SOUR{}:DATA:OLD:N? {}'.format(channel,samples))
        return raw_data

# Custom Output Commands

    def enableOutput(self, channel):
        self.tx_txt('OUTPUT{}:STATE ON'.format(channel))
        return

    def disableOutput(self, channel):
        self.tx_txt('OUTPUT{}:STATE OFF'.format(channel))
        return

    def setFreq(self, channel, frequency_Hz):
        self.tx_txt('SOUR{}:FREQ:FIX {}'.format(channel, frequency_Hz))
        return

    def setWaveform(self, channel, waveform):
        self.tx_txt('SOUR{}:FUNC {}'.format(channel,waveform))
        return

    def setAmplitude(self, channel, amplitude_volts):
        self.tx_txt('SOUR{}:VOLT {}'.format(channel,amplitude_volts))
        return

    def setOffset(self,offset_volts):
        self.tx_txt('SOUR{}:VOLT:OFFS {}'.format(channel, offset_volts))
        return

    def setPhase(self, channel, phase_deg):
        self.tx_txt('SOUR{}:PHAS {}'.format(channel, phase_deg))
        return

    def setDutyCycle(self,channel,duty_percent):
        self.tx_txt('SOUR{}:DCYC {}'.format(channel,duty_percent))
        return

    def setArbWaveform(self, channel, array):
        self.tx_txt('SOUR{}:TRAC:DATA:DATA {}'.format(channel, array))
        return

    def enableBurstMode(self, channel):
        self.tx_txt('SOUR{}:BURS:STAT ON'.format(channel))
        return

    def disableBurstMode(self, channel):
        self.tx_txt('SOUR{}:BURS:STAT OFF'.format(channel))
        return

    def setBurstCount(self, channel, cycles_per_burst):
        self.tx_txt('SOUR{}:BURS:NCYC {}'.format(channel, cycles_per_burst))
        return

    def setBurstRep(self, channel, num_of_bursts):
        self.tx_txt('SOUR{}:BURS:NOR {}'.format(channel, num_of_bursts))
        return

    def setGenTriggerSrc(self, channel, trig_src):
        self.tx_txt('SOUR{}:TRIG:SOUR {}'.format(channel, trig_src))
        return

    def trigImmediately(self, channel):
        self.tx_txt('SOUR{}:TRIG:IMM'.format(channel))
        return

    def trigAllImmediately(self):
        self.tx_txt('TRIG:IMM')
        return

    def resetOutput(self):
        self.tx_txt('GEN:RST')
        return

# LED Commands
    
    def turnOnLED(self, num):
        self.tx_txt('DIG:PIN LED{},1'.format(num))
        return

    def turnOffLED(self,num):
        self.tx_txt('DIG:PIN LED{},0'.format(num))
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
        return self.tx_txt('*CLS')

    def ese(self, value: int):
        """Standard Event Status Enable Command"""
        return self.tx_txt('*ESE {}'.format(value))

    def ese_q(self):
        """Standard Event Status Enable Query"""
        return self.txrx_txt('*ESE?')

    def esr_q(self):
        """Standard Event Status Register Query"""
        return self.txrx_txt('*ESR?')

    def idn_q(self):
        """Identification Query"""
        return self.txrx_txt('*IDN?')

    def opc(self):
        """Operation Complete Command"""
        return self.tx_txt('*OPC')

    def opc_q(self):
        """Operation Complete Query"""
        return self.txrx_txt('*OPC?')

    def rst(self):
        """Reset Command"""
        return self.tx_txt('*RST')

    def sre(self):
        """Service Request Enable Command"""
        return self.tx_txt('*SRE')

    def sre_q(self):
        """Service Request Enable Query"""
        return self.txrx_txt('*SRE?')

    def stb_q(self):
        """Read Status Byte Query"""
        return self.txrx_txt('*STB?')

# :SYSTem

    def err_c(self):
        """Error count."""
        return self.txrx_txt('SYST:ERR:COUN?')

    def err_c(self):
        """Error next."""
        return self.txrx_txt('SYST:ERR:NEXT?')



