from omega import *
from cyclops import *

l1 = Light.create()
l1.setPosition(0, 0, 0)
# l1.setColor(Color(1, 1, 0.8, 1))
# l1.setAmbient(Color(0.1,0.1,0.1,1))
# l1.setLightType(LightType.Spot)
# l1.setLightDirection(Vector3(0, 0, -1))

cam = getDefaultCamera()
# cam.setPosition( 0, 0, 0)
box = BoxShape.create(0.8, 0.8, 0.8)
box.setPosition( 0, 0, -10)

# Format: camPx, camPy, camPz, viewPx, viewPy, viewPz, timeGap (distance between this frame and the last frame)

currentAnimation = []
maxAnimPoint = 0
currentFrame = [0,0,0,0,0,0,0]
currCamPoint = [0,0,0]
nextCamPoint = [0,0,0] # camera position
posChangePerSecond = [0,0,0]

currOrientation = [0,0,0]
nextOrientation = [0,0,0] # PitchYawRoll of the camera at the next orientation.
orientationChangePerSecond = [0,0,0]

timeSinceLast = 0 #current time since last 
nextGoalTime = 0
currGoalTime = 0
currentAnimPoint = 0
playing = False

def onUpdate(frame, t, dt):
	global timeSinceLast
	if playing:
		timeSinceLast = timeSinceLast + dt
		animate(dt)
	
def animate(dt):
	global currentAnimPoint, timeSinceLast, nextGoalTime,maxAnimPoint
	currCamPoint[0] = currCamPoint[0] + (dt * posChangePerSecond[0])
	currCamPoint[1] = currCamPoint[1] + (dt * posChangePerSecond[1])
	currCamPoint[2] = currCamPoint[2] + (dt * posChangePerSecond[2])
	cam.setPosition(currCamPoint[0],currCamPoint[1],currCamPoint[2])

	currOrientation[0] = currOrientation[0] + (dt * orientationChangePerSecond[0])
	currOrientation[1] = currOrientation[1] + (dt * orientationChangePerSecond[1])
	currOrientation[2] = currOrientation[2] + (dt * orientationChangePerSecond[2])
	cam.setPitchYawRoll(Vector3(currOrientation[0],currOrientation[1],currOrientation[2]))

	# print "Dt: " , dt, " TimeSinceLast: ", timeSinceLast, " nextGoalTime: ", nextGoalTime
	if timeSinceLast >= nextGoalTime:
		print "-----Printing Animation Point: ", currentAnimPoint , "--------"
		if currentAnimPoint < (maxAnimPoint - 1):
			timeSinceLast = 0
			print "advancing point. Current: ", currentAnimPoint, " Max: ", maxAnimPoint
	 		currentAnimPoint = currentAnimPoint + 1
			setPointTo(currentAnimPoint)
			calculateInterpolationTo(currentAnimPoint + 1)
		else:
			print "Finished"
			currentAnimPoint = 0
			print "finished animation"
			setPlaying(False)

def setPlaying(play):
	global playing
	if play:
		playing = True
	else:
		playing = False

def calculateInterpolationTo(point):
	global nextFrame, nextCamPoint, nextGoalTime , nextOrientation, posChangePerSecond, orientationChangePerSecond
	nextFrame = currentAnimation[point]
	nextFrame[3] = nextFrame[3] - 2

	nextCamPoint[0] = nextFrame[0]
	nextCamPoint[1] = nextFrame[1]
	nextCamPoint[2] = nextFrame[2]
	nextGoalTime = nextFrame[6]

	yDiff = (1.0*nextFrame[4]) - (1.0*nextFrame[1])
	xDiff = (1.0*nextFrame[3]) - (1.0*nextFrame[0])
	zDiff = (1.0*nextFrame[5]) - (1.0*nextFrame[2])

	print " xDiff: ", xDiff, " yDiff: " , yDiff, " zDiff: ", zDiff
	rotx = math.atan2(yDiff,zDiff)
	roty = math.atan2(xDiff * math.cos(rotx),zDiff)
	rotz = math.atan2(math.cos(rotx),math.sin(rotx) * math.sin(roty))
	rotz = rotz * -1.0
	print "rotX: " , rotx , " rotY: " , roty, " rotZ: " , rotz

	nextOrientation[0] = rotx
	nextOrientation[1] = roty
	nextOrientation[2] = rotz

	posChangePerSecond[0] = (nextCamPoint[0] - currCamPoint[0])/nextGoalTime
	posChangePerSecond[1] = (nextCamPoint[1] - currCamPoint[1])/nextGoalTime
	posChangePerSecond[2] = (nextCamPoint[2] - currCamPoint[2])/nextGoalTime

	orientationChangePerSecond[0] = (nextOrientation[0] - currOrientation[0])/nextGoalTime
	orientationChangePerSecond[1] = (nextOrientation[1] - currOrientation[1])/nextGoalTime
	orientationChangePerSecond[2] = (nextOrientation[2] - currOrientation[2])/nextGoalTime



def setPointTo(currentPoint):
	global currentAnimation,currentFrame,currCamPoint,currGoalTime,currOrientation, currGoalTime
	currentFrame = currentAnimation[currentPoint]
	currentFrame[3] = currentFrame[3] - 2

	currCamPoint[0] = currentFrame[0]
	currCamPoint[1] = currentFrame[1]
	currCamPoint[2] = currentFrame[2]

	currGoalTime = currentFrame[6]

	yDiff = (1.0*currentFrame[4]) - (1.0*currentFrame[1])
	xDiff = (1.0*currentFrame[3]) - (1.0*currentFrame[0])
	zDiff = (1.0*currentFrame[5]) - (1.0*currentFrame[2])

	rotx = math.atan2(yDiff,zDiff)
	roty = math.atan2(xDiff * math.cos(rotx),zDiff)
	rotz = math.atan2(math.cos(rotx),math.sin(rotx) * math.sin(roty))
	currOrientation[0] = rotx
	currOrientation[1] = roty
	currOrientation[2] = rotz

#http://stackoverflow.com/questions/1251828/calculate-rotations-to-look-at-a-3d-point
def resetAnimation():
	global timeSinceLast, cam
	print "resetting Animation"
	timeSinceLast = 0
	currentAnimPoint = 0
	setPointTo(0)
	calculateInterpolationTo(1)
	cam.setPosition(currCamPoint[0],currCamPoint[1],currCamPoint[2])
	print "Position set to: " , nextCamPoint
	cam.setPitchYawRoll(Vector3(currOrientation[0],currOrientation[1],currOrientation[2]))
	print "Current Orientation: ", currOrientation

def loadAnimation(animationTable):
	global currentAnimation, maxAnimPoint
	currentAnimation = animationTable
	maxAnimPoint = len(currentAnimation) - 1
	print "Max Anim point is: " ,  maxAnimPoint
	resetAnimation()

setUpdateFunction(onUpdate)

test = [[0,0,0,0,0,-10,0],[0,0,6,0,0,-10,3],[0,6,6,0,0,-10,10]]
loadAnimation(test)
setPlaying(True)