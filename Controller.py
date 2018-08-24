import time

class Controller:

	def __init__(self,ip,param_file):
		self.file = param_file
		self.params = self.getParams()
		self.redpitaya = initializeRP.main(ip, self.params)
		self.pid = PID(self.params)
		self.pidON = False
		self.loop_iter = 0
		self.figure = updateDisplay.initialize3Plots(redpitaya)

	def getParams(self):
		param_dict = {}
		with open(self.file,'r') as f:
			text = f.readlines()[1:]
			for line in text:
				words = line.split('=')
				if '(' in words[0]:
					param_name = words[0].split('(')[0].strip()
				else:
					param_name = words[0].strip()
				key = param_name
				param_value = words[1].strip('\n').strip()
				param_dict[key] = param_value
		param_dict['Trigger Delay Fraction'] = float(param_dict['Trigger Delay Fraction'])
		param_dict['Trigger Level'] = float(param_dict['Trigger Level'])
		param_dict['Stable Laser Channel'] = int(param_dict['Stable Laser Channel'])
		param_dict['Unstable Laser Channel'] = int(param_dict['Unstable Laser Channel'])
		param_dict['Feedback Channel'] = int(param_dict['Feedback Channel'])
		param_dict['Ramp Frequency'] = float(param_dict['Ramp Frequency'])
		param_dict['Set Point'] = float(param_dict['Set Point'])
		return param_dict

	def controlLoop(self):
		loop_begin = time.time()
		try:
			while True:

		except:
			KeyboardInterrupt
