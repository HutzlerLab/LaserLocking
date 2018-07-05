#analyzeData.py

import numpy as np
from scipy.optimize import curve_fit

ANALYSIS_SUCCESSFUL = True

def main(redpitaya):
	analysis_results = analyzeBothChannels(redpitaya)
	if ANALYSIS_SUCCESSFUL:
		redpitaya.fit_params = analysis_results
	redpitaya.error.append(calculateError(redpitaya))
	return

def gaussian(x,a,b,n):
	return n*np.exp(-(x-b)**2/(2*a))

def fitGaussian(xscale, data, guess):
	try:
		popt, pcov = curve_fit(gaussian, xscale, data, guess) #bounds=([0,-3*length,0],[3*length**2,3*length,10]))
		ANALYSIS_SUCCESSFUL = True
	except RuntimeError:
		print("Error - curve_fit failed")
		ANALYSIS_SUCCESSFUL = False
		popt, pcov = [],[]
	return [popt,pcov]

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
	return scaled_error

def analyzeSingleChannel(redpitaya, channel):
	guess = makeGuess(redpitaya, redpitaya.data[channel-1])
	[single_fit_params, covariance] = fitGaussian(redpitaya.time_scale,redpitaya.data[channel-1], guess)
	return single_fit_params

def analyzeBothChannels(redpitaya):
	analysis = []
	for ch in {1,2}:
		analysis.append(analyzeSingleChannel(redpitaya, ch))
	return analysis

def makeGuess(redpitaya, data):
	finesse = 300
	max_guess = np.amax(data)
	mean_guess = np.argmax(data)/redpitaya.ramp_samples*redpitaya.ramp_time_ms
	var_guess = (redpitaya.ramp_time_ms/finesse)**2
	guess = [var_guess, mean_guess, max_guess]
	return guess