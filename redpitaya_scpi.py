#! /usr/bin/python
"""SCPI access to Red Pitaya."""

import socket
import time
import numpy as np
import math

__author__ = "Luka Golinar and Iztok Jeras made the SCPI class. Arian Jadbabaie modified the SCPI class and made the RedPitaya class."

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

    def rx_arb(self):
        numOfBytes = 0
        """ Recieve binary data from scpi server"""
        str=''
        while (len(str) != 1):
            str = (self._socket.recv(1))
        if not (str == '#'):
            return False
        str=''
        while (len(str) != 1):
            str = (self._socket.recv(1))
        numOfNumBytes = int(str)
        if not (numOfNumBytes > 0):
            return False
        str=''
        while (len(str) != numOfNumBytes):
            str += (self._socket.recv(1))
        numOfBytes = int(str)
        str=''
        while (len(str) != numOfBytes):
            str += (self._socket.recv(1))
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

    def getRawData(self, channel):
        raw_data = self.txrx_txt('ACQ:SOUR{}:DATA?'.format(channel))
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


class RedPitaya:

    def __init__(self,scpi):
        self.scpi = scpi
        self.scpi.disableOutput(1)
        self.scpi.disableOutput(2)
        self.scpi.resetAcq()
        self.scpi.resetOutput()

    # Acquisition attributes
        self.avg = self.scpi.getAvgStatus()
        self.decimation = self.scpi.getDecimation()
        self.buff_size = self.scpi.getBuffSize()
        self.trig_level  = 0
        self.trig_status = None
        self.trig_source = None
        self.data_format = None
        self.data_units  = None
        self.trig_delay = self.getTrigDelay()

    # Data attributes
        self.data        = None
        self.error       = []
        self.fit_params  = None
        self.stable_channel = None
        self.unstable_channel = None
        self.feedback_channel = None

    # Output attributes
        self.feeedback_waveform = None
        self.frequency_Hz = 1000
        self.amplitude_volts = 1

    # Finished initializing
        self.scpi.flashAllLED()

    @property
    def buff_time_ms(self):
        return self.decimation*131.072 * 10**-3

    @property
    def time_scale(self):
        return np.linspace(0,self.buff_time_ms,self.buff_size)
    

# General commands
    def closeConnection(self):
        self.scpi.turnOffAllLED()
        self.scpi.close()
        print('Connection at {} closed.'.format(self.scpi.host))

# Acquisition commands
    def startAcquisition(self):
        self.scpi.startAcq()
        self.scpi.turnOnLED(7)
        print('Acquisition started.')
        time.sleep(self.buff_time_ms*0.001)

    def stopAcquisition(self):
        self.scpi.stopAcq()
        self.scpi.turnOffLED(7)
        print('Acquisition stopped.')

    def getAcqTime(self):
        self.decimation = self.scpi.getDecimation()
        print('Decimation factor is {}'.format(self.decimation))
        print('Buffer time length is {} ms'.format(self.buff_time_ms))
        return self.buff_time_ms

    def setAcqTime(self,sample_time):
        desired_dec = int(2**(math.ceil(math.log2(sample_time/(131.072 * 10**-3)))))
        dec_list = [1,8,64,1024,8192,65536]
        if any(desired_dec != dec for dec in dec_list):
            actual_dec = min(dec_list, key=lambda x:abs(x-desired_dec))
        else:
            actual_dec = desired_dec
        self.scpi.setDecimation(actual_dec)
        self.getAcqTime()

    def setAvgStatus(self, avg):
        if avg=='ON':
            self.scpi.enableAvg()
        elif avg=='OFF':
            self.scpi.disableAvg()
        else:
            print('{} is not a recognized value for average status. Accepted values are ON and OFF.'.format(avg))
        self.getAvgStatus()

    def getAvgStatus(self):
        self.avg = self.scpi.getAvgStatus()
        print('Averaging is {}'.format(self.avg))
        return self.avg
    
    def setInputGain(self,gain,channel):
        bad = False
        if gain == 'HV':
            self.scpi.setInputHighV(channel)
        elif gain == 'LV':
            self.scpi.setInputLowV(channel)
        else:
            print('{} is not a recognized value for input gain. \nAccepted values are HV and LV.'.format(gain))
            bad = True

        if bad == False:
            print('Input {} gain setting is {}'.format(channel,gain))

    def setTrigDelay(self, delay_fraction):
        delay_samples = int((delay_fraction*2-1)*self.buff_size/2)
        self.scpi.setTrigDelay(delay_samples)
        self.getTrigDelay()

    def getTrigDelay(self):
        delay_samples = self.scpi.getTrigDelay()
        self.trig_delay = (2*delay_samples/self.buff_size+1)/2
        print('Trigger delay is {}% of the buffer'.format(self.trig_delay*100))
        return self.trig_delay

    def setTrigLevel(self, level_mV):
        self.scpi.setTrigLevel(level_mV)
        self.getTrigLevel()

    def getTrigLevel(self):
        self.trig_level = self.scpi.getTrigLevel()
        print('Trigger level is {} mV'.format(self.trig_level))

    def runTriggerLoop(self,timeout=10):
        self.scpi.turnOnLED(5)
        start = time.time()
        while True:
            self.trig_status = self.scpi.getTrigStatus()
            elapsed = time.time()-start 

            if self.trig_status == 'TD':
                self.scpi.turnOffLED(5)
                print('Triggered')
                return True

            elif elapsed > timeout:
                self.trig_status = None
                self.scpi.turnOffLED(5)
                self.scpi.turnOnLED(0)
                self.scpi.turnOnLED(1)
                print('Trigger timed out after {} seconds'.format(timeout))
                return False

    def setTrigSource(self,source):
        self.scpi.setTrigSource(source)
        self.trig_source = source
        print('Trigger source set to {}'.format(source))

# Data commands

    def setDataUnits(self,units):
        bad = False
        if units == 'RAW':
            self.scpi.setAcqUnitsRaw()
            self.data_units = units
        elif units == 'VOLTS':
            self.scpi.setAcqUnitsVolts()
            self.data_units = units
        else:
            print('{} is not a recognized value for data units. \nAccepted values are RAW and VOLTS.'.format(units))
            bad = True

        if bad == False:
            print('Data units set to {}'.format(units))

    def setDataFormat(self,data_format):
        bad = False
        if data_format == 'ASCII':
            self.scpi.setDataFormatASCII()
        elif data_format == 'BIN':
            self.scpi.setDataFormatBinary()
        else:
            print('{} is not a recognized value for data format. \nAccepted values are ASCII and BIN.'.format(data_format))
            bad = True

        if bad == False:
            self.data_format = data_format

    def getRawData(self, channel):
        raw_data = self.scpi.getRawData(channel)
        return raw_data
 
    def processASCIIDataVolts(self, raw_data):
        stripped_data = raw_data.strip('{}\n\r').replace("  ", "").split(',')
        data_array = np.fromiter(stripped_data, float, self.buff_size)
        # alternatives: map(float, buff_string) or np.array(list(map(float,buff_string))) or can try np.fromiter(map(float,buff_string))
        return data_array

    def getProcessedData(self,channel):
        self.scpi.turnOnLED(6)
        raw_data = self.getRawData(channel)

        if self.data_format=='ASCII' and self.data_units=='VOLTS':
            data_array = self.processASCIIDataVolts(raw_data)
        self.scpi.turnOffLED(6)
        return data_array


# Output commands

    def setOutputFrequency(self, channel, frequency_Hz):
        self.scpi.setFreq(channel,frequency_Hz)
        self.frequency_Hz = frequency_Hz
        print('Output {} frequency set to {} Hz.'.format(channel, frequency_Hz))

    def setOutputWaveform(self, channel, waveform):
        self.scpi.setWaveform(channel, waveform)
        self.feedback_waveform = waveform
        print('Output {} waveform set to {}'.format(channel,waveform))

        if waveform == 'DC':
            self.setOutputFrequency(channel, 0)

    def setOutputAmplitude(self, channel, amplitude_volts):
        if abs(amplitude_volts) > 1:
            amplitude_volts = amplitude_volts/abs(amplitude_volts)

        self.scpi.setAmplitude(channel, amplitude_volts)
        self.amplitude_volts = amplitude_volts

    def enableOutput(self, channel):
        self.scpi.enableOutput(channel)
        self.scpi.turnOnLED(4)
        print('Output {} enabled.'.format(channel))

    def disableOutput(self,channel):
        self.scpi.disableOutput(channel)
        self.scpi.turnOffLED(4)
        print('Output {} disabled.'.format(channel))



