import laserLocking
import argparse

parser = argparse.ArgumentParser(description='Laser locking test')
parser.add_argument('-ip',           		type=str, default='169.254.174.98', 				help='provide IP address for RedPitaya')
parser.add_argument('-p', '--port', 		type=int, default=5000,        						help='specify SCPI port (default is 5000)')
parser.add_argument('-f', '--file', 	type=str, default='laser_locking_parameters.txt', 	help='specify name of txt file with locking parameters')
#parser.add_argument('-b', '--bin',  action="store_true",         		help='use binary data transfer instead of the default ASCII')
#parser.add_argument('--py',         action="store_true",        		help='use PyVISA-py (by default the system visa library is used)')
args = parser.parse_args()

if __name__ == '__main__':
	laserLocking.main(args.ip,args.file)