import os, sys, string, time
from classlist import *

def main():
	"""Main program"""
	
	# Read input file
	try:
		f = sys.stdin
	except IOError as e:
		sys.exit("{}".format(e))
	rawinput = []
	for line in f:
		if line.startswith("%") or not line.strip():
			continue
		rawinput.append(line[:-1].lower()) # ditch trailing newline
	
	# Remove non-data lines & format
	rawdata = rawinput[rawinput.index("@data")+1:]
	data = []
	for line in rawdata:
		data.append(line.split(','))
	
	# Process input
	start = time.time()
	CL = classlist(data)
	end = time.time()
	#print CL.leaves
	print(CL.displayTree())
	print("SLIQ took " + str(end - start) + " seconds")

if __name__ == '__main__':
	main()