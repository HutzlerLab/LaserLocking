# updateFeedback.py

def main(controller):
	redpitaya = controller.redpitaya
	error = redpitaya.error[-1]
	if controller.error_sign == 'Negative':
		error *= -1
	calibration = 0.002
	if controller.pidON:
		pid = controller.pid
		output_value = pid.update(error)
	else:
		output_value = error - controller.pid.set_point # - redpitaya.amplitude_volts - calibration
		output_value /= redpitaya.error_scale
	output_value-=calibration
	if abs(output_value) > 1: 
		output_value/=abs(output_value)
	redpitaya.setOutputOffset(redpitaya.feedback_channel, output_value)
	return

#def calculateFeedback(error, pid):
#	feedback = pid.main(error)
#	return feedback