# updateFeedback.py

def main(redpitaya):
	error = redpitaya.error[-1]
	calibration = 0.004
	output_value = error - redpitaya.amplitude_volts - calibration
	redpitaya.setOutputOffset(redpitaya.feedback_channel, output_value)
	return

def calculateFeedback(error, pid):
	feedback = pid.main(error)
	return feedback