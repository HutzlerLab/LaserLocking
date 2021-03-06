# updateFeedback.py

def main(controller):
	redpitaya = controller.redpitaya
	error = redpitaya.error[-1]
	if controller.error_sign == 'Negative':
		error *= -1

	if controller.use_control:
		if controller.pidON:
			output_value = controller.pid.update(error)
		else:
			output_value = 0
	else:
		output_value = error - controller.pid.set_point # - redpitaya.amplitude_volts - calibration
		output_value /= redpitaya.error_scale
	output_value-=controller.calibration
	if abs(output_value) > 1: 
		output_value/=abs(output_value)
	redpitaya.setOutputOffset(redpitaya.feedback_channel, output_value)
	return

#def calculateFeedback(error, pid):
#	feedback = pid.main(error)
#	return feedback