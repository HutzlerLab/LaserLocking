# updateDisplay.py
import matplotlib.pyplot as plt
import numpy as np
import time

def main(redpitaya, figure):
	axes = figure.axes
	for ch in {1,2}:
		fit = convertFitToData(redpitaya.time_scale, redpitaya.fit_params[ch-1])
		updateTransmissionData(axes[ch-1],redpitaya.data[ch-1],fit)
	updateErrorData(axes[-1],redpitaya.error)

	figure.canvas.draw()
	time.sleep(0.00001)



def initialize3Plots(redpitaya):
	fig = plt.figure()
	stable_ax = fig.add_subplot(3,1,redpitaya.stable_channel)
	unstable_ax = fig.add_subplot(3,1,redpitaya.unstable_channel)
	error_ax = fig.add_subplot(313)
	time_xdata = redpitaya.time_scale
	zero_ydata = np.zeros(redpitaya.buff_size)
	error_xdata = []
	error_ydata = []
	line_stable_data, = stable_ax.plot(time_xdata, zero_ydata)
	line_stable_fit, = stable_ax.plot(time_xdata, zero_ydata)
	line_unstable_data, = unstable_ax.plot(time_xdata, zero_ydata)
	line_unstable_fit, = unstable_ax.plot(time_xdata, zero_ydata)
	line_error = error_ax.plot(error_xdata,error_ydata)
	fig.canvas.draw()
	return fig

def closeAll():
	plt.close('all')

def updateTransmissionData(axis, data, fit_data):
	lines = axis.get_lines()
	line_data = lines[0]
	line_fit = lines[1]
	line_data.set_ydata(data)
	line_fit.set_ydata(fit_data)
	axis.autoscale_view(True, True, True)

def updateErrorData(axis,data):
	line = axis.get_lines()[0]
	line.set_ydata(data)
	line.set_xdata(np.linspace(1,len(data),len(data)))
	axis.relim()
	axis.autoscale_view(True,True,True)

def gaussian(x,a,b,n):
	return n*np.exp(-(x-b)**2/(2*a))

def convertFitToData(xscale, fit_params):
	return gaussian(xscale,*fit_params)