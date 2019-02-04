Written by Arian Jadbabaie
02/02/2019

This python3 code is used to implement a tunable, slow transfer cavity lock for
a laser's frequency, using a Red Pitaya. You can run this code by importing
laserLocking.py and running laserLocking.main(ip), where ip is the IP address
of the RedPitaya.
NOTE: You must have a "laser_locking_parameters.txt" file and a "pid_parameters.txt" file in the same directory for this to work.
By modifying and saving the pid_parameters.txt file, the lock can be updated.

This code is a work in progress. Thanks for being understanding.
Contact arianjad@gmail.com with bugs.
