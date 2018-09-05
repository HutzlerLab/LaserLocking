#initializeRP

from redpitaya_scpi import SCPI
from redpitaya_controller import RedPitaya
import visa
#import argparse

#parser = argparse.ArgumentParser(description='Initialize red pitaya')
#parser.add_argument('-ip',           		type=str, default='169.254.174.98', 				help='provide IP address for RedPitaya')
#args = parser.parse_args()

def main(ip, param_dict):
	rp_instrument = openConnection(ip)
	redpitaya = RedPitaya(rp_instrument)
	setParameters(redpitaya, param_dict)
	redpitaya.scpi.flashAllLED()
	return redpitaya

def openConnection(ip):
	delimiter = '\r\n'
	port = 5000
	rm = visa.ResourceManager('@py')
	rp_instrument = rm.open_resource('TCPIP::{}::{}::SOCKET'.format(ip, port), read_termination = delimiter)	
	return rp_instrument

def setParameters(redpitaya, param_dict):
	redpitaya.setTrigDelay(param_dict['Trigger Delay Fraction'],p=True)

	redpitaya.setTrigLevel(param_dict['Trigger Level'],p=True)

	redpitaya.setInputGain(param_dict['Gain1'],1,p=True)

	redpitaya.setInputGain(param_dict['Gain2'],2,p=True)

	redpitaya.setAvgStatus(param_dict['Averaging'],p=True)

	redpitaya.setDataUnits(param_dict['Acquisition Units'],p=True)

	redpitaya.setDataFormat(param_dict['Acquisiton Format'],p=True)

	redpitaya.trig_source = param_dict['Acquisition Trigger']
	print('Trigger source set to {}'.format(redpitaya.trig_source))

	redpitaya.stable_channel = param_dict['Stable Laser Channel']

	redpitaya.unstable_channel = param_dict['Unstable Laser Channel']

	redpitaya.feedback_channel = param_dict['Feedback Channel']

	redpitaya.setOutputWaveform(redpitaya.feedback_channel, param_dict['Feedback Waveform'])

	ramp_freq_Hz = param_dict['Ramp Frequency']
	redpitaya.ramp_time_ms = 10**3 * 1/ramp_freq_Hz *0.995
	redpitaya.setAcqTime(redpitaya.ramp_time_ms,p=True)
	print('Ramp time is {} ms'.format(redpitaya.ramp_time_ms))

	initial_amplitude = 0.0
	redpitaya.setOutputAmplitude(redpitaya.feedback_channel, initial_amplitude)

	redpitaya.error_scale = param_dict['Error Scale Factor']

if __name__ == '__main__':
	main(args.ip)