class ControlLoop:

	def __init__(self,ip,param_file):
		self.ip = ip
		self.params = self.getParams(param_file)
		

	def getParams(self, file):

