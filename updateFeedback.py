# updateFeedback.py

def main(redpitaya):
	output_value = processError(redpitaya)
	print(output_value)
	redpitaya.setOutputAmplitude(redpitaya.feedback_channel, output_value)
	return

def processError(redpitaya):
	recent_error = redpitaya.error[-1]
	max_error = redpitaya.buff_time_ms
	processed_error = recent_error/max_error
	return processed_error