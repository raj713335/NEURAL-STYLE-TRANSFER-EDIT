# USAGE
# python neural_style_transfer_video.py --models models


from imutils.video import VideoStream
from imutils import paths
import itertools
import argparse
import imutils
import time
import cv2


ap = argparse.ArgumentParser()
ap.add_argument("-m", "--models", required=True,
	help="path to directory containing neural style transfer models")
args = vars(ap.parse_args())


modelPaths = paths.list_files(args["models"], validExts=(".t7",))
modelPaths = sorted(list(modelPaths))


models = list(zip(range(0, len(modelPaths)), (modelPaths)))


modelIter = itertools.cycle(models)
(modelID, modelPath) = next(modelIter)


print("[INFO] loading style transfer model...")
net = cv2.dnn.readNetFromTorch(modelPath)


print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
print("[INFO] {}. {}".format(modelID + 1, modelPath))


while True:

	frame = vs.read()


	frame = imutils.resize(frame, width=600)
	orig = frame.copy()
	(h, w) = frame.shape[:2]


	blob = cv2.dnn.blobFromImage(frame, 1.0, (w, h),
		(103.939, 116.779, 123.680), swapRB=False, crop=False)
	net.setInput(blob)
	output = net.forward()


	output = output.reshape((3, output.shape[2], output.shape[3]))
	output[0] += 103.939
	output[1] += 116.779
	output[2] += 123.680
	output /= 255.0
	output = output.transpose(1, 2, 0)


	#cv2.imshow("Input", frame)
	cv2.imshow("Output",  cv2.resize(output, (1920,1060)))
	key = cv2.waitKey(1) & 0xFF


	if key == ord("n"):

		(modelID, modelPath) = next(modelIter)
		print("[INFO] {}. {}".format(modelID + 1, modelPath))
		net = cv2.dnn.readNetFromTorch(modelPath)


	elif key == ord("q"):
		break


cv2.destroyAllWindows()
vs.stop()