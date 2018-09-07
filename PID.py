import time

# PID controller class, written by Arian Jadbabaie
class PIDclass(object): 

	def __init__(self, P=0.1, I=0, D=0, set_point=0):

		# Initialize P, I, D values and set point. 
		# feedback = Kp * (error) + Ki * (error * dt) + Kd * (delta_error/dt)
		self.Kp = P
		self.Ki = I
		self.Kd = D
		self.set_point = set_point
		print('PID initial parameters: \nP={}, I={}, D={} \nSet Point={}'.format(self.Kp,self.Ki,self.Kd,self.set_point))
		self.current_time = time.time()

		# Initialize everything at 0
		self.clear()

		# Properties are useful for caculating quantities on the fly
	@property
	def delta_t(self):
		# No time has elapsed for the first value
		if self.first:
			dt = 0
		else:
			dt = self.current_time - self.last_time
		return dt

	@property
	def delta_error(self):
		return self.error - self.last_error

	@property
	def feedback(self):
		return self.Pterm + self.Iterm + self.Dterm

	# Clear function re-initializes everything
	def clear(self):
		self.Pterm = 0
		self.Iterm = 0
		self.Dterm = 0
		self.error = 0
		self.last_time=self.current_time
		self.last_error = 0
		self.first = True
		self.feedback_history = [[],[]]

	# Update function generates next iteration of PID output
	def update(self, signal):
		self.current_time = time.time()

		# Calculate difference from set point
		self.error = signal - self.set_point

		# Update P, I, D terms
		self.calculateTerms()

		# Record feedback signal for plotting later
		self.storeHistory()

		# Store time in memory for next iteration
		self.last_time = self.current_time

		#No longer first
		if self.first:
			self.first = False
			
		return self.feedback

	# This function does the math
	def calculateTerms(self):
		self.Pterm = self.Kp * self.error
		self.Iterm += self.Ki * self.error * self.delta_t
		print("Iterm = ",self.Iterm)
		print("Ki = {}. Error = {}. Deltat = ")
		# Don't divide by 0
		if self.delta_t > 0:
			self.Dterm = self.delta_error/self.delta_t

	# Store feedback history in lists
	def storeHistory(self):
		self.feedback_history[0].append(self.feedback)

		# list[-1] will throw an error if len(list) = 0, need to catch initial case
		if self.first:
			self.feedback_history[1].append(self.delta_t)
		else:
			self.feedback_history[1].append(self.delta_t + self.feedback_history[1][-1])
