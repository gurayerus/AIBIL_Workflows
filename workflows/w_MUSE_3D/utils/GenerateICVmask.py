#!/usr/bin/env python

################################################ FUNCTIONS ################################################
import os, sys, time
EXEC_NAME = "SkullStrip_IC.py"

# Usage info
def usage():
    """usage information"""
    print(r"""
  %(EXEC)s--
    Generate approximate ICV mask from a given brain mask

  USAGE: %(EXEC)s [OPTIONS]

  OPTIONS:
  Reqd:
    [-i --T1input   ]	< file	>	Input T1 image
    [-r --T2input   ]	< file	>	Input T2 image
    [-j --jacrank   ]	< file	>	Input Jacobian Rank Mask
    [-o --out	    ]	< file  >	Output file name
  
  Optional:
    [-a --affine    ]			Flag indicating the input files are already co-registered (default: None)
    [-s --str       ]	< file  >	Output filename for the skull-stripped image (default: None)
    [-p --prob      ]	< file  >	Output filename for the tissue probabilities (default: None)
    [-n --iter      ]	< int	>	Number of iterations of dilations (default: 50)
    [-l --minsd     ]	< float >	Minimum std dev to accept during conditional dilation (default: -1)
    [-h --maxsd     ]	< float >	Maximum std dev to accept during conditional dilation (default: 3)
    [-t --tolerance ]	< float	>	Minimum tolerance level (default: 0.01)
    [-v --verbose   ] 			Verbose output (default: no)


  """) #% {'EXEC':EXEC_NAME}

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        pool.terminate()
        sys.exit(0)

################################################ END OF FUNCTIONS ################################################

################################################ MAIN BODY ################################################


# Check the number of arguments
if len(sys.argv) < 8:
	usage()
	sys.exit(0)

### Timestamps
startTime = time.asctime()
startTimeStamp = time.time()

### Import some more modules
import getopt
import pythonUtilities
from pythonUtilities import *

# Setting environ variable for fsl
os.environ['FSLOUTPUTTYPE'] = 'NIFTI_GZ'

### Default parameters
numiter     = int(50)
minsd       = float(-0.5)
maxsd       = float(3)
tolerance   = float(0.01)
verbose     = int(0)
affine      = int(0)
tmpDirToUse = None
stripped    = None
costfuncs   = [ 'mutualinfo', 'normmi' ]
probJR      = None

### Read command line args
print("\nParsing args: ", sys.argv[ 1: ], "\n")

try:
	opts, files = getopt.getopt( sys.argv[1:], "i:r:j:o:n:l:h:t:s:ap:v",
	  [ "T1input", "T2input", "jacrank", "out", "iter","minsd","maxsd", "tolerance", "str", "affine", "prob", "verbose" ] )

except getopt.GetoptError as err:
	usage()
	print("ERROR!", err)

for o, a in opts:
	if o in [ "-i", "--T1input" ]:
		T1  = a

		checkFile( T1 )
		T1inputdName, T1inputbName, T1inputExt = FileAtt( T1 )

	if o in [ "-r", "--T2input" ]:
		T2  = a

		checkFile( T2 )
		T2inputdName, T2inputbName, T2inputExt = FileAtt( T2 )

	elif o in [ "-j", "--jacrank" ]:
		JR   = a

		checkFile(JR)
		JRdName, JRbName, JRExt = FileAtt( JR )

	elif o in [ "-o", "--out" ]:
		out   = a

		outdName, outbName, outExt = FileAtt(out)

	elif o in [ "-s", "--str" ]:
		stripped   = a

		strippeddName, strippedbName, strippedExt = FileAtt( stripped )

	elif o in [ "-p", "--prob" ]:
		probJR = a

	elif o in [ "-a", "--affine" ]:
		affine   = int(1)
	elif o in [ "-n", "--iter" ]:
		numiter   = int( a )
	elif o in [ "-l", "--minsd" ]:
		minsd     = float(a)
	elif o in [ "-h", "--maxsd" ]:
		maxsd     = float(a)
	elif o in [ "-t", "--tolerance" ]:
		tolerance = float(a)
	elif o in [ "-v", "--verbose" ]:
		verbose   = int(1)
#	else:
#		print "\nERROR! Option %s does not exist! \n" % (o)
#		usage()
#		sys.exit(0)

### Import some more modules
import nibabel as nib
import numpy as np
import scipy as sp
import signal
from scipy import ndimage
import scipy.stats as st
import subprocess

### Read the input images
print("----->	Reading the input images ...")
T1_img 	= nib.load( os.path.join( T1 ) )
JR_img 	= nib.load( os.path.join( JR ) )

T1_dat 	= T1_img.get_data()
T1_hdr 	= T1_img.get_header()

JR_dat 	= JR_img.get_data()
JR_hdr 	= JR_img.get_header()

JR_dat 	= JR_dat / JR_dat.max() 	# scaling the jacrank to [0,1]

if affine == int(1):
	T2_img 	= nib.load( os.path.join( T2 ) )
	T2_dat 	= T2_img.get_data()
	T2_hdr 	= T2_img.get_header()

### Create temporary directory
TMP = createTempDir('SkullStrip_IC-', tmpDirToUse)

### Co-register T1 and T2 images if required
if affine == int(0):
	
	print("----->	Co-registering T1 and T2 images ...")
	
	T2_dat = np.zeros_like( T1_dat )
	
	for cost in costfuncs:
		cmd = 'flirt ' \
			'-in ' + T2 + ' ' \
			'-ref ' + T1 + ' ' \
			'-out ' + TMP + '/' + T2inputbName + '_rT1_' + cost + '.nii.gz' + ' ' \
			'-cost ' + cost + ' ' \
			'-searchcost ' + cost + ' ' \
			'-interp trilinear ' \
			'-dof 12 ' \
			'-v'				 
			
		try:
			if verbose == 1:
				print("\t-->	Executing : %s \n" % cmd)
	
			proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
			(out, err) = proc.communicate()

			if verbose == 1:
				print(out)
		       
		except:
			print("\nERROR! Execution of this command failed: \n", cmd)
			sys.exit(0)

		# Read co-registered T2 images and average them
		T2_img 	= nib.load( TMP + '/' + T2inputbName + '_rT1_' + cost + '.nii.gz' )
		T2_dat	= T2_dat + T2_img.get_data()
		T2_hdr	= T2_img.get_header()

		# Remove temporary files
		os.remove( TMP + '/' + T2inputbName + '_rT1_' + cost + '.nii.gz' )
	
	# Average the T2 images
	T2_dat = T2_dat / len( costfuncs )

### Threshold the input image at threshold mask and segment it
print("----->	Thresholding the input T1 and T2 images at the 50% agreement mask and segmenting them ...")

T1_dat_thresh 		= sp.where( JR_dat > 0.5, T1_dat, 0 )
T1_dat_thresh_res 	= sp.ndimage.zoom( T1_dat_thresh, 0.5, order=1 )

T2_dat_thresh 		= sp.where( JR_dat > 0.5, T2_dat, 0 )
T2_dat_thresh_res 	= sp.ndimage.zoom( T2_dat_thresh, 0.5, order=1 )

T1_dat_thresh_resimg = nib.Nifti1Image( T1_dat_thresh_res, None, T1_hdr )
T1_dat_thresh_resimg.to_filename( os.path.join( TMP + '/' + T1inputbName + '_thresh_res.nii.gz' ) )

T2_dat_thresh_resimg = nib.Nifti1Image( T2_dat_thresh_res, None, T2_hdr )
T2_dat_thresh_resimg.to_filename( os.path.join( TMP + '/' + T2inputbName + '_thresh_res.nii.gz' ) )

# Segment T1 image
cmd = 'fast ' \
	'-n 3 ' \
	'-t 1 ' \
	'-N ' \
	'-o ' + TMP + '/' + T1inputbName + '_thresh_res_fast.nii.gz ' \
	'-v ' \
	'--nopve ' \
	+ TMP + '/' + T1inputbName + '_thresh_res.nii.gz'
		 
try:
	if verbose == 1:
		print("\t-->	Executing : %s \n" % cmd)
	
	proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()

	if verbose == 1:
		print(out)
       
except:
	print("\nERROR! Execution of this command failed: \n", cmd)
	sys.exit(0)

# Segment T2 image
cmd = 'fast ' \
	'-n 3 ' \
	'-t 2 ' \
	'-N ' \
	'-o ' + TMP + '/' + T2inputbName + '_thresh_res_fast.nii.gz ' \
	'-v ' \
	'--nopve ' \
	+ TMP + '/' + T2inputbName + '_thresh_res.nii.gz'
		 
try:
	if verbose == 1:
		print("\t-->	Executing : %s \n" % cmd)
	
	proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()

	if verbose == 1:
		print(out)
       
except:
	print("\nERROR! Execution of this command failed: \n", cmd)
	sys.exit(0)

# Read segmented image and then delete the temporary directory
T1segimg = nib.load( TMP + '/' + T1inputbName + '_thresh_res_fast_seg.nii.gz' ).get_data()
T2segimg = nib.load( TMP + '/' + T2inputbName + '_thresh_res_fast_seg.nii.gz' ).get_data()

os.remove( TMP + '/' + T1inputbName + '_thresh_res.nii.gz' )
os.remove( TMP + '/' + T1inputbName + '_thresh_res_fast_seg.nii.gz' )
os.remove( TMP + '/' + T2inputbName + '_thresh_res.nii.gz' )
os.remove( TMP + '/' + T2inputbName + '_thresh_res_fast_seg.nii.gz' )

os.removedirs(TMP)

### Generate probability maps for GM and WM and add them to the jacrank
print("----->	Generating tissue probabilities for WM, GM and CSF and adding them to the input JacRank probabilities ...")

T1_dat_prob = np.zeros_like( T1_dat )
T2_dat_prob = np.zeros_like( T2_dat )
prob_map    = np.zeros( (T1_dat.shape[0], T1_dat.shape[1], T1_dat.shape[2], 5) )

for tissue in 1, 2, 3:
	print("\t-->	Generating tissue probabilities for tissue ", tissue)

	# CSF
	if tissue in [ 1 ]:
		# Calculate non-zero mean, stdev and the z-score for this tissue type
		T1_dat_zscore 	= ( T1_dat - T1_dat_thresh_res[ T1segimg == int(tissue) ].mean() ) / T1_dat_thresh_res[ T1segimg == int(tissue) ].std()
		T1_dat_prob 	= st.norm.sf( T1_dat_zscore )

		T2_dat_zscore 	= ( T2_dat - T2_dat_thresh_res[ T2segimg == int(tissue) ].mean() ) / T2_dat_thresh_res[ T2segimg == int(tissue) ].std()
		T2_dat_prob 	= 1 - st.norm.sf( T2_dat_zscore )
		
		prob_final = T1_dat_prob * T2_dat_prob
	# GM
	elif tissue in [ 2 ]:
		# Calculate non-zero mean, stdev and the z-score for this tissue type
		T1_dat_zscore 	= np.abs( ( T1_dat - T1_dat_thresh_res[ T1segimg == int(tissue) ].mean() ) / T1_dat_thresh_res[ T1segimg == int(tissue) ].std() )
		T1_dat_prob 	= st.norm.sf( T1_dat_zscore ) * 8 #4
		
		prob_final = T1_dat_prob
	# WM
	elif tissue in [ 3 ]:
		# Calculate non-zero mean, stdev and the z-score for this tissue type
		T1_dat_zscore 	= ( T1_dat - T1_dat_thresh_res[ T1segimg == int(tissue) ].mean() ) / T1_dat_thresh_res[ T1segimg == int(tissue) ].std()
		T1_dat_prob 	= 1 - st.norm.sf( T1_dat_zscore )
		
		prob_final = T1_dat_prob

	prob_map[ :,:,:,tissue-1 ] = prob_final

### Generate probability maps for brain and non-brain
print("----->	Generating tissue probabilities for brain tissue ...")

prob_map[ :,:,:,3 ] = ( JR_dat + prob_map[ :,:,:,1 ] + prob_map[ :,:,:,2 ] ) * ( 1-prob_map[ :,:,:,0 ] )
prob_map[ :,:,:,4 ] = ( prob_map[ :,:,:,3 ]/prob_map[ :,:,:,3 ].max()*2 + 4*prob_map[ :,:,:,0 ] )
#prob_map[ :,:,:,4 ] = ( prob_map[ :,:,:,3 ] + 4*prob_map[ :,:,:,0 ] )

### Smooth all probabilities
print("----->	Smoothing all probabilities ...")
for i in range(5):
	prob_map[ :,:,:,i ] = sp.ndimage.gaussian_filter( prob_map[ :,:,:,i ], 1 / np.sqrt(8*np.log(2)) )

### Get the initial brain mask from the input jacobian rank map
print("----->	Generating the initial brain mask from the input Jacobian Rank Mask ...")

# Getting the initial brain mask
#data_maskimg 		= sp.where( prob_map[ :,:,:,3 ] > 1.1, 1, 0 )
data_maskimg 		= sp.where( prob_map[ :,:,:,3 ] > 1.25, 1, 0 )
data_maskimg_updated 	= sp.ndimage.binary_opening( data_maskimg, iterations=4 ).astype(np.int)

# Removing small clusters smaller than 100 voxels in size
label_im, nb_labels 	= sp.ndimage.label( data_maskimg_updated )
sizes 			= sp.ndimage.sum( data_maskimg_updated, label_im, list(range(nb_labels + 1)))
vol			= data_maskimg_updated.sum() / 2
mask_size 		= sizes < vol
remove_pixel 		= mask_size[label_im]

data_maskimg_updated[remove_pixel] = 0

for tissue in 3, 4:
	
	if tissue == 3:
		print("\t-->	Performing conditional expansion in brain tissue ")
	else:
		print("\t-->	Performing conditional expansion in non-brain tissue ")

	### Conditionally dilating the brain mask
	prevCount 	= currentCount = data_maskimg_updated.sum()
	diffCount 	= 0
	i 		= 1
	volRat 		= 100.000
	mean 		= 2 
	stdev 		= 0

	data_maskimg_prev = data_maskimg_updated.copy()
	
#	while ( i <= numiter ) and ( volRat >= tolerance ) and ( mean >= 2*stdev ) :
	while ( i <= numiter ) and ( volRat >= tolerance ) and ( mean >= stdev ) :

		# Calculate non-zero mean, stdev and the z-score for this tissue type
		mean 				= prob_map[ :,:,:,tissue ][ data_maskimg_updated > 0 ].mean()
		stdev 				= prob_map[ :,:,:,tissue ][ data_maskimg_updated > 0 ].std()

		prob_zscore 	= ( prob_map[ :,:,:,tissue ] - mean ) / stdev

		# Binarizing the z-score mask between intervals [minsd, maxsd] and dilating it
		data_maskimg_updated 		= data_maskimg_prev + \
						(sp.ndimage.morphology.binary_dilation(data_maskimg_prev) - data_maskimg_prev) * \
						sp.where( (prob_zscore > minsd) & (prob_zscore < maxsd), 1, 0)

		# Binary opening
		data_maskimg_updated 		= sp.ndimage.binary_opening( data_maskimg_updated ).astype(np.int)

		# Removing small clusters smaller than 10 voxels in size
		label_im, nb_labels 		= sp.ndimage.label(data_maskimg_updated)
		sizes 				= sp.ndimage.sum(data_maskimg_updated, label_im, list(range(nb_labels + 1)))
		mask_size 			= sizes < 100
		remove_pixel 			= mask_size[label_im]
		data_maskimg_updated[remove_pixel] = 0

		# Binary closing
		data_maskimg_updated 		= sp.ndimage.binary_closing( data_maskimg_updated ).astype(np.int)

		# Gaussian smoothing
		data_maskimg_updated 		= sp.where( sp.ndimage.gaussian_filter( data_maskimg_updated*1000, 2 / np.sqrt(8*np.log(2)) ) > 500, 1, 0)

		# Calculating stats again
		prevCount 			= float(data_maskimg_prev.sum())
		currentCount 			= float(data_maskimg_updated.sum())
		volRat 				= float(100*((currentCount - prevCount) / prevCount))
		diffCount 			= (currentCount - prevCount)

		data_maskimg_prev 		= data_maskimg_updated.copy()

		print("\t\t-->	Iteration: %s. percent change: %f. Mean: %f. StDev: %f" % (i, volRat, mean, stdev))
		i = i + 1

# Gaussian smoothing
data_maskimg_updated = sp.where( sp.ndimage.gaussian_filter( data_maskimg_updated*1000, 2 / np.sqrt(8*np.log(2)) ) > 500, 1, 0)


# Save output files
if probJR:
	JR_dat_updated_final_img = nib.Nifti1Image( prob_map[ :,:,:,3 ], None, JR_hdr)
	JR_dat_updated_final_img.to_filename(os.path.join( probJR + '_Brain.nii.gz' ))

	JR_dat_updated_final_img = nib.Nifti1Image( prob_map[ :,:,:,4 ], None, JR_hdr)
	JR_dat_updated_final_img.to_filename(os.path.join( probJR + '_Brain+CSF.nii.gz' ))

if stripped:
	T1inputdName, T1inputbName, T1inputExt
	data_inputimg_thresh = sp.where( data_maskimg_updated > 0, T1_dat, 0 )
	
	data_inputimg_thresh = nib.Nifti1Image( data_inputimg_thresh, None, T1_hdr )
	data_inputimg_thresh.to_filename(os.path.join( strippeddName + '/' + strippedbName + strippedExt ))

data_maskimg_updated = nib.Nifti1Image( data_maskimg_updated, None, T1_hdr)
data_maskimg_updated.set_data_dtype( 'uint8' )
data_maskimg_updated.to_filename(os.path.join( outdName + '/' + outbName + outExt ))



### Execution Time
executionTime(startTimeStamp)

################################################ END ################################################	
