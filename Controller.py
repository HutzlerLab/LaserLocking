import time
import PID
import initializeRP
import takeData
import analyzeData
import updateFeedback
import updateDisplay
import datetime
import csv


class Controller:

	def __init__(self,ip,param_dict):
		self.params = param_dict
		self.redpitaya = initializeRP.main(ip, self.params)
		self.pid = PID()
		self.pidON = False

		self.clear()
		self.figure = updateDisplay.initialize3Plots(redpitaya)
		self.redpitaya.enableOutput(self.redpitaya.feedback_channel)

	@classmethod
	def getParams(cls,param_file):
		param_dict = {}
		with open(param_file,'r') as f:
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
		return cls(ip,param_dict)

	def clear(self):
		self.loop_begin = time.time()
		self.loop_iter = 0
		self.avg_loop_time = 0
		self.pid.clear()

	def controlLoop(self, set_point_widget):
		self.loop_begin = time.time()
		redpitaya = self.redpitaya
		try:
			while(True):
				loop_start = time.time()
				self.pid.set_point = set_point_widget.value
				# Take data
				acquisition_successful = takeData.main(redpitaya)

				# Trigger received
				if acquisition_successful:
					# Analyze data
					analyzeData.main(redpitaya, self.loop_begin)

					# Update feedback
					updateFeedback.main(redpitaya, self.pid)

					# Update display
					updateDisplay.main(redpitaya, self.figure)

					# Timing
					loop_end = time.time()
					loop_time = loop_end - loop_start
					self.avg_loop_time+=loop_time
					self.loop_iter+=1
				# No trigger
				else:
					self.stopRP(redpitaya)
					redpitaya.closeConnection()
					updateDisplay.closeAll()
					print('No trigger was detected so acquisition was stopped, the program was aborted, and the connection was closed.')
					break

		# Escape loop with interrupt
		except KeyboardInterrupt:
			self.stopRP()
			self.redpitaya.closeConnection()
			updateDisplay.closeAll()
			print('Program stopped.')
			if self.loop_iter > 0:
				print('Average loop time was {} seconds.'.format(self.avg_loop_time/self.loop_iter))
			pass

	def stopRP(self):
		redpitaya = self.redpitaya
		redpitaya.stopAcquisition()
		redpitaya.disableOutput(redpitaya.feedback_channel)
		name = 'Error_signal_'+datetime.datetime.today().strftime('%I%M%p_%Y%m%d')+'.csv'
		title = 'Error Value'
		with open(name,'w',newline='') as f:
			w = csv.writer(f)
			w.writerow([title,"Time (s)"])
			w.writerows(zip(redpitaya.error,redpitaya.error_time))
		name = 'Stable_Mean_'+datetime.datetime.today().strftime('%I%M%p_%Y%m%d')+'.csv'
		title = 'Mean Value'
		with open(name,'w',newline='') as f:
			w = csv.writer(f)
			w.writerow([title,"Time (s)"])
			w.writerows(zip(redpitaya.means[0]), redpitaya.error_time)