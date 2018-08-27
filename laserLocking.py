# Initialize and lock laser

import time
import Controller
from ipywidgets import interact, interactive, fixed, interact_manual
from IPython.display import display
import ipywidgets as widgets
import threading

def main(ip, param_file='laser_locking_parameters.txt'):
	# Start/open communitation channel to Red Pitaya
	# Set parameters
	#redpitaya = initializeRP.main(ip, param_file)

	controller = Controller.getParams(ip, param_file)

	set_point_slider = widgets.FloatSlider(
		value=controller.pid.set_point,
		min=-1.0,
		max=1.0,
		step=0.01,
		description='Set Point:',
		disabled=False,
		continuous_update=False,
		orientation='horizontal',
		readout=True,
		readout_format='.2f')

	set_point_text = widgets.FloatText(
		value=controller.pid.set_point,
		description='Any:',
		disabled=False)

	display(set_point_text, set_point_slider)
	mylink = widgets.jslink((set_point_text, 'value'), (set_point_slider, 'value'))

	loopThread = threading.Thread(target=controller.controlLoop,args=(set_point_text,),daemon=True)

	loopThread.start()
	# Initialize plotting
	#figure = updateDisplay.initialize3Plots(redpitaya)

	# Start output at some value (usually 0).
	#redpitaya.enableOutput(redpitaya.feedback_channel)

	# Initialize PID
	#pid = PID.PID()

	# Timing
	#i=0
	#avg_loop_time = 0
	#loop_begin = time.time()
	# Lock the laser in a loop. Exit loop with CTRL+C
	# try:
	# 	while(True):
	# 		loop_start = time.time()
	# 		# Take data
	# 		acquisition_successful = takeData.main(redpitaya)

	# 		# Trigger received
	# 		if acquisition_successful:
	# 			# Analyze data
	# 			analyzeData.main(redpitaya, loop_begin)

	# 			# Update feedback
	# 			updateFeedback.main(redpitaya,self.pidON)

	# 			# Update display
	# 			updateDisplay.main(redpitaya, figure)

	# 			# Timing
	# 			i+=1
	# 			loop_end = time.time()
	# 			loop_time = loop_end - loop_start
	# 			avg_loop_time+=loop_time
	# 		# No trigger
	# 		else:
	# 			stopRP(redpitaya)
	# 			redpitaya.closeConnection()
	# 			updateDisplay.closeAll()
	# 			print('No trigger was detected so acquisition was stopped, the program was aborted, and the connection was closed.')
	# 			break

# 	# Escape loop with interrupt
# 	except KeyboardInterrupt:
# 		stopRP(redpitaya,avg_loop_time)
# 		redpitaya.closeConnection()
# 		updateDisplay.closeAll()
# 		print('Program stopped.')
# 		print('Average loop time was {} seconds.'.format(avg_loop_time/i))
# 		pass


# # Stop acquisition and output
# def stopRP(redpitaya,avg_loop_time):
# 	redpitaya.stopAcquisition()
# 	redpitaya.disableOutput(redpitaya.feedback_channel)
# 	name = 'Error_signal_'+datetime.datetime.today().strftime('%I%M%p_%Y%m%d')+'.csv'
# 	title = 'Error Value'
# 	with open(name,'w',newline='') as f:
# 		w = csv.writer(f)
# 		w.writerow([title,"Time (s)"])
# 		w.writerows(zip(redpitaya.error,redpitaya.error_time))
# 	name = 'Stable_Mean_'+datetime.datetime.today().strftime('%I%M%p_%Y%m%d')+'.csv'
# 	title = 'Mean Value'
# 	with open(name,'w',newline='') as f:
# 		w = csv.writer(f)
# 		w.writerow([title,"Time (s)"])
# 		w.writerows(zip(redpitaya.means[0]), redpitaya.error_time)