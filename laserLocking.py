'''
This is the main function for locking a laser using a Red Pitaya (RP).
To run the program, execute laserLocking.main(ip). This will initialize
the RP using the file "laser_locking_parameters.txt". Use that text file
to control the lock by modifying and saving the text fileself.

To work with Jupyter notebook, this code uses tkinter to display
plots in a separate window.

Work in progress by Arian Jadbabaie. arianjad@gmail.com
'''

import time
from Controller import ControllerClass

'''Initialize RP, run control loop'''
def main(ip, param_file='laser_locking_parameters.txt'):

	# Initialize controller class instance used to handle parameters and run loop
	controller = ControllerClass.getParams(ip, param_file)

	# Run control loop indefinitely until the kernel is stopped
	controller.controlLoop()
