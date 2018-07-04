import time
import numpy as np
from redpitaya_scpi import SCPI
import math

class RedPitaya:

    def __init__(self, instrument):
        self.instrument = instrument
        self.scpi = SCPI(instrument)
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
        self.ramp_time_ms = 0

    # Output attributes
        self.feeedback_waveform = None
        self.frequency_Hz = 1000
        self.amplitude_volts = 1
        self.offset_volts = 0

    # Finished initializing
        self.scpi.flashAllLED()

    @property
    def buff_time_ms(self):
        return self.decimation*131.072 * 10**-3

    @property
    def ramp_samples(self):
        return int(self.ramp_time_ms/self.buff_time_ms*self.buff_size)

    @property
    def time_scale(self):
        return np.linspace(0,self.ramp_time_ms,self.ramp_samples)
    

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
            dec_list = [x for x in dec_list if x > desired_dec]
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

    def getAllRawData(self, channel):
        raw_data = self.scpi.getAllRawData(channel)
        return raw_data
 
    def processASCIIDataVolts(self, raw_data):
        stripped_data = raw_data.strip('{}\n\r').replace("  ", "").split(',')
        data_array = np.fromiter(stripped_data, float)
        # alternatives: map(float, buff_string) or np.array(list(map(float,buff_string))) or can try np.fromiter(map(float,buff_string))
        return data_array

    def getAllProcessedData(self,channel):
        self.scpi.turnOnLED(6)
        raw_data = self.scpi.getAllRawData(channel)
        if self.data_format=='ASCII' and self.data_units=='VOLTS':
            data_array = self.processASCIIDataVolts(raw_data)
        self.scpi.turnOffLED(6)
        return data_array

    def getLateProcessedData(self,channel):
        self.scpi.turnOnLED(6)
        samples = self.ramp_samples
        raw_data = self.scpi.getLateRawData(channel, samples)
        if self.data_format=='ASCII' and self.data_units=='VOLTS':
            data_array = self.processASCIIDataVolts(raw_data)
        self.scpi.turnOffLED(6)
        return data_array

    def getEarlyProcessedData(self,channel):
        self.scpi.turnOnLED(6)
        samples = self.ramp_samples
        raw_data = self.scpi.getEarlyRawData(channel, samples)
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
        self.scpi.setAmplitude(channel, amplitude_volts)
        self.amplitude_volts = amplitude_volts

    def setOutputOffset(self, channel, offset_volts):
    	self.scpi.setOffset(channel, offset_volts)
    	self.offset_volts = offset_volts

    def enableOutput(self, channel):
        self.scpi.enableOutput(channel)
        self.scpi.turnOnLED(4)
        print('Output {} enabled.'.format(channel))

    def disableOutput(self,channel):
        self.scpi.disableOutput(channel)
        self.scpi.turnOffLED(4)
        print('Output {} disabled.'.format(channel))