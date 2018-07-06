#analyzeData.py

import numpy as np
from scipy.optimize import curve_fit

ANALYSIS_SUCCESSFUL = True

def main(redpitaya):
	analysis_results = analyzeBothChannels(redpitaya)
	if len(analysis_results) == 2:
		redpitaya.fit_params = analysis_results
	else:
		print("Error performing analysis")
	redpitaya.error.append(calculateError(redpitaya))
	return

def gaussian(x,a,b,n):
	return n*np.exp(-(x-b)**2/(2*a))

def fitGaussian(xscale, data, guess):
	global ANALYSIS_SUCCESSFUL
	try:
		popt, pcov = curve_fit(gaussian, xscale, data, guess) #bounds=([0,-3*length,0],[3*length**2,3*length,10]))
		ANALYSIS_SUCCESSFUL = True
		return [popt,pcov]
	except RuntimeError:
		print("Error - curve_fit failed")
		ANALYSIS_SUCCESSFUL = False
		return [[],[]]

def getMean(single_fit_params):
	mean = single_fit_params[1]
	return mean

def getVariance(single_fit_params):
	variance = single_fit_params[0]
	return variance

def calculateError(redpitaya):
	mean_stable = getMean(redpitaya.fit_params[redpitaya.stable_channel - 1])
	mean_unstable = getMean(redpitaya.fit_params[redpitaya.unstable_channel - 1])
	error = mean_stable - mean_unstable
	max_error = redpitaya.ramp_time_ms
	scaled_error = error/max_error
	if abs(scaled_error) > 1:
		scaled_error=scaled_error/abs(scaled_error)
	return scaled_error

def analyzeSingleChannel(redpitaya, channel):
	guess = makeGuess(redpitaya, redpitaya.data[channel-1])
	[single_fit_params, covariance] = fitGaussian(redpitaya.time_scale,redpitaya.data[channel-1], guess)
	return single_fit_params

def analyzeBothChannels(redpitaya):
	analysis = []
	for ch in {1,2}:
		result = analyzeSingleChannel(redpitaya, ch)
		if ANALYSIS_SUCCESSFUL:
			analysis.append(result)
	return analysis

def makeGuess(redpitaya, data):
	finesse = 300
	max_guess = np.amax(data)
	mean_guess = np.argmax(data)/redpitaya.ramp_samples*redpitaya.ramp_time_ms
	var_guess = (redpitaya.ramp_time_ms/finesse)**2
	guess = [var_guess, mean_guess, max_guess]
	return guess