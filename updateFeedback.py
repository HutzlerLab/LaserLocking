# updateFeedback.py

def main(redpitaya):
	error = redpitaya.error[-1]
	calibration = 0.004
	output_value = error - redpitaya.amplitude_volts - calibration
	print(output_value)
	redpitaya.setOffset(redpitaya.feedback_channel, output_value)
	return