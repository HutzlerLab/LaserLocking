# takeData.py

def main(redpitaya, timeout=10):
	redpitaya.startAcquisition()
	redpitaya.setTrigSource(redpitaya.trig_source)
	if waitForTrigger(redpitaya, timeout):
		redpitaya.data = readBothChannels(redpitaya)
		return True
	else:
		print('No data available, no trigger detected.')
		return False

def readBothChannels(redpitaya):
	data = []
	for ch in {1,2}:
		data.append(readSingleChannel(redpitaya, ch))
	return data


def readSingleChannel(redpitaya,channel):
	single_data = redpitaya.getLateProcessedData(channel)
	return single_data


def waitForTrigger(redpitaya, timeout=10):
	trig_result = redpitaya.runTriggerLoop()
	return trig_result
