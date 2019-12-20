#analyzeData.py

import numpy as np
from scipy.optimize import curve_fit
import time

ANALYSIS_SUCCESSFUL = True

def main(controller):
	redpitaya = controller.redpitaya
	loop_begin = controller.loop_begin
	analysis_results = analyzeBothChannels(redpitaya)
	if len(analysis_results) == 2:
		redpitaya.fit_params = analysis_results
		redpitaya.error.append(calculateError(controller))
	else:
		print("Error performing analysis")
		if len(redpitaya.error) == 0:
			redpitaya.error.append(0)
		else:
			redpitaya.error.append(redpitaya.error[-1])
	redpitaya.error_time.append(time.time()-loop_begin)
	return

def gaussian(x,a,b,n,c):
	try:
		return n*np.exp(-(x-b)**2/(2*a))+c
	except RuntimeWarning:
		print('x={},a={},b={},n={},c={}'.format(x,a,b,n,c))
		return 1

def fitGaussian(xscale, data, guess, length):
	global ANALYSIS_SUCCESSFUL
	bounds = ([0,-1.1*length,0,0],[length**2,1.1*length,10,0.1])
	try:
		popt, pcov = curve_fit(gaussian, xscale, data, p0=guess, bounds=bounds,ftol=1e-3,xtol=1e-3) #bounds=([0,-3*length,0],[3*length**2,3*length,10]))
		ANALYSIS_SUCCESSFUL = True
		return [popt,pcov]
	except RuntimeError:
		print("Error - curve_fit failed")
		ANALYSIS_SUCCESSFUL = False
		return [[],[]]
	except ValueError:
		print("Error - guess is outside of bounds")
		ANALYSIS_SUCCESSFUL = False
		print("Guess: ",guess)
		print("Bounds: ",bounds)
		return [[],[]]

def getMean(single_fit_params):
	mean = single_fit_params[1]
	return mean

def getVariance(single_fit_params):
	variance = single_fit_params[0]
	return variance

def calculateError(controller):
	redpitaya = controller.redpitaya
	stable = redpitaya.stable_channel - 1
	unstable = redpitaya.unstable_channel - 1
	mean_stable = getMean(redpitaya.fit_params[stable])
	mean_unstable = getMean(redpitaya.fit_params[unstable])
	redpitaya.means[stable].append(mean_stable)
	redpitaya.means[unstable].append(mean_unstable)
	error = mean_stable - mean_unstable
	#if controller.use_control:
	#	error = error - controller.pid.set_point
	max_error = redpitaya.ramp_time_ms
	scaled_error = error/max_error
	if abs(scaled_error) > 1:
		scaled_error=scaled_error/abs(scaled_error)
	return scaled_error

def analyzeSingleChannel(redpitaya, channel):
	guess = makeGuess(redpitaya, redpitaya.data[channel-1])
	[single_fit_params, covariance] = fitGaussian(redpitaya.time_scale,redpitaya.data[channel-1], guess,redpitaya.ramp_time_ms)
	return single_fit_params

def analyzeBothChannels(redpitaya):
	analysis = []
	for ch in {1,2}:
		result = analyzeSingleChannel(redpitaya, ch)
		if ANALYSIS_SUCCESSFUL:
			analysis.append(result)
	return analysis

def makeGuess(redpitaya, data):
	finesse = 123
	max_guess = np.amax(data)
	if max_guess<0:
		max_guess=0
	mean_guess = np.argmax(data)/redpitaya.ramp_samples*redpitaya.ramp_time_ms
	var_guess = (redpitaya.ramp_time_ms/finesse)**2
	offset_guess = 0
	guess = [var_guess, mean_guess, max_guess,offset_guess]
	return guess