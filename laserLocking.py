# Initialize and lock laser

import sys
import time

import initializeRP
import takeData
import analyzeData
import updateFeedback
import updateDisplay

def main(ip, param_file='laser_locking_parameters.txt'):
	# Start/open communitation channel to Red Pitaya
	# Set parameters
	redpitaya = initializeRP.main(ip, param_file)

	# Initialize plotting
	figure = updateDisplay.initialize3Plots(redpitaya)

	# Start output at some value (usually 0).
	redpitaya.enableOutput(redpitaya.feedback_channel)

	# Timing
	i=0
	avg_loop_time = 0

	# Lock the laser in a loop. Exit loop with CTRL+C
	try:
		while(True):
			loop_start = time.time()
			# Take data
			acquisition_successful = takeData.main(redpitaya)

			# Trigger received
			if acquisition_successful:
				# Analyze data
				analyzeData.main(redpitaya)

				# Update feedback
				updateFeedback.main(redpitaya)

				# Update display
				updateDisplay.main(redpitaya, figure)

				# Timing
				i+=1
				loop_end = time.time()
				loop_time = loop_end - loop_start
				avg_loop_time+=loop_time
				print('Average loop time is {} seconds.'.format(avg_loop_time/i))
			# No trigger
			else:
				stopRP(redpitaya)
				redpitaya.closeConnection()
				updateDisplay.closeAll()
				print('No trigger was detected so acquisition was stopped, the program was aborted, and the connection was closed.')
				break

	# Escape loop with interrupt
	except KeyboardInterrupt:
		stopRP(redpitaya)
		redpitaya.closeConnection()
		updateDisplay.closeAll()
		print('Program stopped.')
		print('Average loop time was {} seconds.'.format(avg_loop_time/i))
		pass


# Stop acquisition and output
def stopRP(redpitaya,avg_loop_time):
	redpitaya.stopAcquisition()
	redpitaya.disableOutput(redpitaya.feedback_channel)