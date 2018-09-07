import time
import PID
import initializeRP
import takeData
import analyzeData
import updateFeedback
import updateDisplay
import datetime
import csv
import pathlib


class ControllerClass:

	def __init__(self,ip,param_dict):
		self.params = param_dict
		self.redpitaya = initializeRP.main(ip, self.params)
		pid_info = self.getPIDParams()
		self.pid = PID.PIDclass(P=pid_info[0], I=pid_info[1], D=pid_info[2], set_point=pid_info[3])
		self.pidON = pid_info[4]
		self.calibration = pid_info[5]
		self.error_sign = self.params['Error Sign']
		self.use_control = param_dict['Use Control']

		self.clear()
		self.figure = updateDisplay.initialize3Plots(self.redpitaya)
		self.redpitaya.enableOutput(self.redpitaya.feedback_channel)

	@classmethod
	def getParams(cls,ip,param_file='laser_locking_parameters.txt',pid_file='pid_parameters.txt'):
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
#		param_dict['Set Point'] = float(param_dict['Set Point'])
		param_dict['Error Scale Factor'] = float(param_dict['Error Scale Factor'])
		if param_dict['Use Control'] == 'True' or param_dict['Use Control'] == 'true':
			param_dict['Use Control'] = True
		else:
			param_dict['Use Control'] = False
		return cls(ip,param_dict)

	def clear(self):
		self.loop_begin = time.time()
		self.loop_iter = 0
		self.avg_loop_time = 0
		self.pid.clear()

	def getPIDParams(self, file = 'pid_parameters.txt'):
		parameters = []
		with open(file,'r') as f:
			text = f.readlines()[1:]
			for line in text:
				words = line.split('=')
				param_value = words[1].strip('\n').strip()
				if param_value == 'True':
					parameters.append(True)
				elif param_value == 'False':
					parameters.append(False)
				else:
					parameters.append(float(param_value))
		return parameters

	def updatePIDParams(self):
		frequency = 10
		prev_status = self.pidON
		before=[self.pid.Kp, self.pid.Ki, self.pid.Kd, self.pid.set_point]
		if self.loop_iter%frequency ==0 and self.loop_iter > 0:
			before=[self.pid.Kp, self.pid.Ki, self.pid.Kd, self.pid.set_point]
			parameters = self.getPIDParams()
			self.pidON = parameters[4]
			self.pid.Kp = parameters[0]
			self.pid.Ki = parameters[1]
			self.pid.Kd = parameters[2]
			self.pid.set_point = parameters[3]
			self.calibration = parameters[5]
			after = [self.pid.Kp, self.pid.Ki, self.pid.Kd, self.pid.set_point]
			if before[0] != after[0]:
				print('P=',after[0])
			elif before[1] != after[1]:
				print('I=',after[1])
			elif before[2] != after[2]:
				print('D=',after[2])
			elif before[3] != after[3]:
				print('Set Point=',after[3])
		if not self.pidON and prev_status: #turning off should clear pid history
			self.pid.clear()
			print('PID OFF')
		if self.pidON and not prev_status: #turning on should let user know values
			print('PID ON')

	def controlLoop(self):
		self.loop_begin = time.time()
		redpitaya = self.redpitaya
		try:
			while(True):
				loop_start = time.time()
				self.updatePIDParams()
				#self.pid.set_point = set_point_widget.value
				#print(self.pid.set_point)
				# Take data
				acquisition_successful = takeData.main(redpitaya)

				# Trigger received
				if acquisition_successful:
					# Analyze data
					analyzeData.main(self)

					# Update feedback
					updateFeedback.main(self)

					# Update display
					updateDisplay.main(self)

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
		redpitaya.setOutputOffset(redpitaya.feedback_channel, self.calibration)
		redpitaya.disableOutput(redpitaya.feedback_channel)
		file = 'ErrorLogs'
		name = 'Error_signal_'+datetime.datetime.today().strftime('%I%M%p_%Y%m%d')+'.csv'
		title = 'Error Value'
		path = pathlib.Path.cwd() / file
		path.mkdir(exist_ok=True)
		filename = file + '/' + name
		with open(filename,'w',newline='') as f:
			w = csv.writer(f)
			w.writerow([title,"Time (s)"])
			w.writerows(zip(redpitaya.error,redpitaya.error_time))
		name = 'Stable_Mean_'+datetime.datetime.today().strftime('%I%M%p_%Y%m%d')+'.csv'
		title = 'Mean Value'
		filename = file + '/' + name
		with open(filename,'w',newline='') as f:
			w = csv.writer(f)
			w.writerow([title,"Time (s)"])
			w.writerows(zip(redpitaya.means[0], redpitaya.error_time))