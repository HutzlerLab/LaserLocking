# updateFeedback.py

def main(redpitaya):
	output_value = redpitaya.error[-1]
	print(output_value)
	redpitaya.setOutputAmplitude(redpitaya.feedback_channel, output_value)
	return