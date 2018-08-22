import time

class PID:

	def __init__(self, P=0.1, I=0, D=0):

		self.Kp = P
		self.Ki = I
		self.Kd = D

		self.sample_time = 0.00
		self.current_time = time.time()
		self.last_time = self.current_time

		self.clear()
