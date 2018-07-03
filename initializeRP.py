#initializeRP

from redpitaya_scpi import SCPI
from redpitaya_controller import RedPitaya
import visa
import argparse

#parser = argparse.ArgumentParser(description='Initialize red pitaya')
#parser.add_argument('-ip',           		type=str, default='169.254.174.98', 				help='provide IP address for RedPitaya')
#args = parser.parse_args()

def main(ip,name='laser_locking_parameters.txt'):
	rp_instrument = openConnection(ip)
	redpitaya = RedPitaya(rp_instrument)
	parameters = readFile(name)
	setParameters(redpitaya, parameters)
	redpitaya.scpi.flashAllLED()
	return redpitaya

def openConnection(ip)
	delimiter = '\r\n'
	port = 5000
	rm = visa.ResourceManager('@py')
	rp_instrument = rm.open_resource('TCPIP::{}::{}::SOCKET'.format(ip, port), read_termination = delimiter)	
	return rp_instrument


def readFile(name):
	#parameters = {
	#	}
	parameters=[]
	with open(name,'r') as f:
		text = f.readlines()[1:]

		for line in text:
			words = line.split('=')
			param = words[1].strip('\n').strip()
			parameters.append(param)

	return parameters

def setParameters(redpitaya, parameters):
	sample_time = float(parameters[0])
	redpitaya.setAcqTime(sample_time)

	delay_fraction = float(parameters[1])
	redpitaya.setTrigDelay(delay_fraction)

	trigger_level = float(parameters[2])
	redpitaya.setTrigLevel(trigger_level)

	gain1 = parameters[3]
	redpitaya.setInputGain(gain1,1)

	gain2 = parameters[4]
	redpitaya.setInputGain(gain2,2)

	averaging = parameters[5]
	redpitaya.setAvgStatus(averaging)

	data_units = parameters[6]
	redpitaya.setDataUnits(data_units)

	data_format = parameters[7]
	redpitaya.setDataFormat(data_format)

	trigger_source = parameters[8]
	redpitaya.trig_source = trigger_source

	stable_laser = int(parameters[9])
	redpitaya.stable_channel = stable_laser

	unstable_laser = int(parameters[10])
	redpitaya.unstable_channel = unstable_laser

	feedback_channel = int(parameters[11])
	redpitaya.feedback_channel = feedback_channel

	feedback_waveform = parameters[12]
	redpitaya.setOutputWaveform(redpitaya.feedback_channel, feedback_waveform)

	ramp_freq_Hz = float(parameters[13])
	redpitaya.ramp_time_ms = 10**3 * 1/ramp_freq_Hz
	print('Ramp time is {} ms'.format(redpitaya.ramp_time_ms))

	initial_amplitude = 0
	redpitaya.setOutputAmplitude(redpitaya.feedback_channel, initial_amplitude)

if __name__ == '__main__':
	main(args.ip)