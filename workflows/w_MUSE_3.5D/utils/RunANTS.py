#!/usr/bin/env python

import os, sys, getopt, signal

EXEC_NAME = "RunANTS.py"

# Usage info
def usage():
    """usage information"""
    print(r"""
  %(EXEC)s--
    A wrapper to run ANTS on a given source and target image and generate the warped output
    image as well as the warped label image

  Usage: %(EXEC)s [OPTIONS]

  Options:
    [-s --source]	Source image file to be warped (in .nii.gz format)
    [-t --target]       Target image file to warp the source image to (in .nii.gz format)
    [-o --output]       Warped output image file (in .nii.gz format)
    [-p --syn]		Symmetric Norm value
    [-l --label]	Label image file in the source image space (in .nii.gz format) (optional)
    [-w --warpedlabel]  Warped label image file in the target image space (in .nii.gz format) (optional)
    [-d --keepwarp]	Keep warps (default: no)
    [-r --rigid]	Rigid alignment only (default: false)
    [-a --affine]	Affine transformation only (default: false)

  """ % {'EXEC':EXEC_NAME})

# Catch error and trap signals
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

# Check the number of arguments
if len(sys.argv) < 8:
	usage()
	sys.exit(0)

# Default parameters
labelImg = None
warpedlabelImg = None
keepwarps = int(0)
rigid = False
affine = False

print("\nParsing args   : %s\n" % (sys.argv[ 1: ]) )
sys.stdout.flush()

# Read command line args
try:
	opts, files = getopt.getopt(sys.argv[1:], "s:t:o:l:w:p:dra",
	  ["source=", "target=","output=","label=","warpedlabel=", "syn=", \
	  "keepwarp","rigid","affine"])

except getopt.GetoptError as err:
	usage()
	print("ERROR!", err)
	sys.stdout.flush()

for o, a in opts:
	if o in ["-s", "--source"]:
		sourceImg = a
	elif o in ["-t", "--target"]:
		targetImg = a
	elif o in ["-o", "--output"]:
		warpedImg = a
	elif o in ["-l", "--label"]:
		labelImg = a
	elif o in ["-w", "--warpedlabel"]:
		warpedlabelImg = a
	elif o in ["-p", "--syn"]:
		syn = a
	elif o in ["-d", "--keepwarp"]:
		keepwarps = int(1)
	elif o in ["-r", "--rigid"]:
		rigid = int(1)
	elif o in ["-a", "--affine"]:
		affine = int(1)
	else:
		usage()
		sys.exit(0)

if rigid==1 and affine==1:
	print("\nERROR! You want both affine and rigid alignment! Please check your options!")
	sys.exit(0)
	
for f in sourceImg, targetImg, labelImg:
	if f and not os.path.exists(f):
		print("\nERROR! %s does not exist! Please check" % f)
		sys.exit(0)

if rigid == 1:
	cmd = 'ANTS '\
		'3 '\
		'-m MI[' + targetImg + ',' + sourceImg + ',1,32] '\
		'-o ' + warpedImg + ' '\
		'-i 0 '\
		'--use-Histogram-Matching '\
		'--number-of-affine-iterations 1000x1000x1000x1000x1000 '\
		'--rigid-affine true '\
		'--affine-gradient-descent-option 0.5x0.95x1.e-4x1.e-4'
elif affine == 1:
	cmd = 'ANTS '\
		'3 '\
		'-m MI[' + targetImg + ',' + sourceImg + ',1,32] '\
		'-o ' + warpedImg + ' '\
		'-i 0 '\
		'--use-Histogram-Matching '\
		'--number-of-affine-iterations 1000x1000x1000x1000x1000 '\
		'--rigid-affine false '\
		'--affine-gradient-descent-option 0.5x0.95x1.e-4x1.e-4'
else:
	cmd = 'ANTS '\
		 '3 '\
		 '-m PR[' + targetImg + ',' + sourceImg + ',1,2] '\
		 '-i 10x50x50x10 '\
		 '-o ' + warpedImg + ' '\
		 '-t SyN[' + syn + '] '\
		 '-r Gauss[2,0]'
		 
try:
	print("\nExecuting : %s \n" % cmd)
	sys.stdout.flush()
	os.system(cmd)
except:
	print("\nERROR! Execution of this command failed: \n", cmd)
	sys.stdout.flush()

if rigid==1 or affine==1:
	cmd = 'WarpImageMultiTransform '\
		 '3 '\
		 + sourceImg + ' '\
		 + warpedImg + ' '\
		 '-R ' + targetImg + ' '\
		 + warpedImg[:-7] + 'Affine.txt'
else:
	cmd = 'WarpImageMultiTransform '\
		 '3 '\
		 + sourceImg + ' '\
		 + warpedImg + ' '\
		 '-R ' + targetImg + ' '\
		 + warpedImg[:-7] + 'Warp.nii.gz ' \
		 + warpedImg[:-7] + 'Affine.txt'
		 
try:
	print("\nExecuting : %s \n" % cmd)
	sys.stdout.flush()
	os.system(cmd)
except:
	print("\nERROR! Execution of this command failed: \n", cmd)
	sys.stdout.flush()

if warpedlabelImg:
	if rigid==1 or affine==1:
		cmd = 'WarpImageMultiTransform '\
			 '3 '\
			 + labelImg + ' '\
			 + warpedlabelImg + ' '\
			 '--use-NN '\
			 '-R ' + targetImg + ' '\
			 + warpedImg[:-7] + 'Affine.txt'	
	else:
		cmd = 'WarpImageMultiTransform '\
			 '3 '\
			 + labelImg + ' '\
			 + warpedlabelImg + ' '\
			 '--use-NN '\
			 '-R ' + targetImg + ' '\
			 + warpedImg[:-7] + 'Warp.nii.gz ' \
			 + warpedImg[:-7] + 'Affine.txt'
			 
	try:
		print("\nExecuting : %s \n" % cmd)
		sys.stdout.flush()
		os.system(cmd)
	except:
		print("\nERROR! Execution of this command failed: \n", cmd)
		sys.stdout.flush()

if keepwarps == 0:
	cmd = 'rm '\
		 '-fv '\
		 + warpedImg[:-7] + 'Warp.nii.gz '\
		 + warpedImg[:-7] + 'InverseWarp.nii.gz '\
		 + warpedImg[:-7] + 'Affine.txt'
			 
	try:
		print("\nExecuting : %s \n" % cmd)
		sys.stdout.flush()
		os.system(cmd)
	except:
		print("\nERROR! Execution of this command failed: \n", cmd)
		sys.stdout.flush()
