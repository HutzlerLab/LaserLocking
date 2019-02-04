'''
This is the main function for locking a laser using a Red Pitaya (RP).
To run the program, execute laserLocking.main(ip). This will initialize
the RP using the file "laser_locking_parameters.txt". Use that text file
to control the lock by modifying and saving the text fileself.

To work with Jupyter notebook, this code uses tkinter to display
plots in a separate window.

Work in progress by Arian Jadbabaie
'''

import time
from Controller import ControllerClass

'''Initialize RP, run control loop'''
def main(ip, param_file='laser_locking_parameters.txt'):

	# Initialize controller class instance used to handle parameters and run loop
	controller = ControllerClass.getParams(ip, param_file)

<<<<<<< HEAD
# Stop acquisition and output
def stopRP(redpitaya,avg_loop_time):
	redpitaya.stopAcquisition()
	redpitaya.disableOutput(redpitaya.feedback_channel)
	name = 'Error_signal_'+datetime.datetime.today().strftime('%I%M%p_%Y%m%d')+'.csv'
	title = 'Error Value'
	with open(name,'w',newline='') as f:
		w = csv.writer(f)
		w.writerow([title,"Time (s)"])
		w.writerows(zip(redpitaya.error,redpitaya.error_time))
	name = 'Stable_Mean_'+datetime.datetime.today().strftime('%I%M%p_%Y%m%d')+'.csv'
	title = 'Mean Value'
	with open(name,'w',newline='') as f:
		w = csv.writer(f)
		w.writerow([title,"Time (s)"])
		w.writerows(zip(redpitaya.means[0], redpitaya.error_time))
=======
	# Run control loop indefinitely until the kernel is stopped
	controller.controlLoop()
>>>>>>> dev
