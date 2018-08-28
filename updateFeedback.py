# updateFeedback.py

def main(controller):
	redpitaya = controller.redpitaya
	error = redpitaya.error[-1]
	#calibration = 0.004
	if controller.pidON:
		output_value = 0
	else:
		output_value = error - controller.pid.set_point # - redpitaya.amplitude_volts - calibration
		output_value /= redpitaya.error_scale

	redpitaya.setOutputOffset(redpitaya.feedback_channel, output_value)
	return

#def calculateFeedback(error, pid):
#	feedback = pid.main(error)
#	return feedback