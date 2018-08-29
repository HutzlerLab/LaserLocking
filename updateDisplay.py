# updateDisplay.py
import matplotlib
matplotlib.use('TKagg')
import matplotlib.pyplot as plt
import numpy as np
import time
from analyzeData import gaussian

def main(redpitaya, fig):
	axes = fig.axes
	xscale = redpitaya.time_scale
	for ch in {1,2}:
		fit_params = redpitaya.fit_params[ch-1]
		axis = axes[ch-1]
		cavity_data = redpitaya.data[ch-1]
		fit_gaussian = convertFitToData(xscale, fit_params)
		updateCavityData(axis, cavity_data, fit_gaussian)

	updateErrorData(axes[-1],redpitaya.error,redpitaya.error_time)

	fig.canvas.draw()
	plt.tight_layout()
	fig.canvas.flush_events()



def initialize3Plots(redpitaya):
	fig = plt.figure()

	time_xdata = redpitaya.time_scale
	zero_ydata = np.zeros(redpitaya.ramp_samples)
	error_xdata = []
	error_ydata = []

	stable_ax = fig.add_subplot(3,1,redpitaya.stable_channel)
	stable_ax.set_xlabel('Time (ms)')
	stable_ax.set_ylabel('Input {} (V)'.format(redpitaya.stable_channel))
	stable_ax.set_title('Stable Laser')
	line_stable_fit, = stable_ax.plot(time_xdata, zero_ydata,'--',label='Fit')
	line_stable_data, = stable_ax.plot(time_xdata, zero_ydata,label='Stable')
	stable_ax.legend()

	unstable_ax = fig.add_subplot(3,1,redpitaya.unstable_channel)
	unstable_ax.set_xlabel('Time (ms)')
	unstable_ax.set_ylabel('Input {} (V)'.format(redpitaya.unstable_channel))
	unstable_ax.set_title('Unstable Laser')
	line_unstable_fit, = unstable_ax.plot(time_xdata, zero_ydata,'--',label='Fit')
	line_unstable_data, = unstable_ax.plot(time_xdata, zero_ydata,label='Unstable')
	unstable_ax.legend()

	error_ax = fig.add_subplot(313)
	error_ax.set_xlabel('Time (s)')
	error_ax.set_ylabel('Output {} (V)'.format(redpitaya.feedback_channel))
	error_ax.set_title('Error')
	line_error, = error_ax.plot(error_xdata,error_ydata)

	fig.canvas.draw()
	plt.tight_layout()
	fig.canvas.flush_events()
	return fig

def closeAll():
	plt.close('all')

def updateCavityData(axis, data, fit_data):
	lines = axis.get_lines()
	line_fit = lines[0]
	line_data = lines[1]	
	line_data.set_ydata(data)
	line_fit.set_ydata(fit_data)
	axis.relim(True)
	axis.autoscale_view(True, True, True)

def updateErrorData(axis,data, time_data):
	keep_values = 100
	line = axis.get_lines()[0]
	if len(data) > keep_values:
		line.set_ydata(data[-keep_values:])
		line.set_xdata(time_data[-keep_values:])
	else:
		line.set_ydata(data)
		line.set_xdata(time_data)
		
	axis.relim()
	axis.autoscale_view(True,True,True)

def convertFitToData(xscale, fit_params):
	return gaussian(xscale,*fit_params)