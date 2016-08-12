from omega import *
from euclid import *
from math import *

cameraPosition = Vector3(0,0,0)
cameraOrientation = Quaternion()
snapbackCameraPosition = Vector3(0,0,0)
snapbackcameraOrientation = Quaternion()
snapback = False
pivotPosition = Vector3(4, 5, 6)
pivotRayOrigin = Vector3(0, 0, 0)
pivotRayDirection = Vector3(0,0,-1)
pivotDistance = 1
pivotDistanceIncrement = 1
    
# node around which the camera rotates.
camera = getDefaultCamera()
camera.setControllerEnabled(False)

startPos = None
rotating = False

# panning speed and vector
panSpeed = 50
panSpeedMultiplier = 1
panVector = Vector3(0,0,0)

def focus():
    global pivotPosition
    global cameraOrientation
    camera.lookAt(pivotPosition, Vector3(0,1,0))
    cameraOrientation = camera.getOrientation()

def onEvent():
    global startPos
    global rotating
    global pivotPosition
    global pivotRayOrigin
    global pivotRayDirection
    global pivotDistance
    global cameraPosition
    global cameraOrientation
    global snapbackCameraPosition
    global snapbackCameraOrientation
    global snapback
    global panVector
    global panSpeed
    
    e = getEvent()
    if(e.getType() == EventType.Zoom):
        pivotDistance += e.getExtraDataInt(0) * pivotDistanceIncrement
        pivotPosition = pivotRayOrigin + pivotRayDirection * pivotDistance 
        return
    
    if(e.isButtonDown(EventFlags.Left)):
        if(e.isFlagSet(EventFlags.Shift)):
            res = getRayFromEvent(e)
            if(res[0] == True):
                pivotRayOrigin = res[1]
                pivotRayDirection = res[2]
                pivotDistance = abs(pivotPosition - pivotRayOrigin)
                pivotPosition = pivotRayOrigin + pivotRayDirection * pivotDistance 
                snapback = True
                snapbackCameraPosition = camera.getPosition()
                snapbackCameraOrientation = camera.getOrientation()
        startPos = e.getPosition()
        rotating = True
    elif(e.isButtonUp(EventFlags.Left)):
        rotating = False
        if(snapback):
            camera.setPosition(snapbackCameraPosition)
            camera.setOrientation(snapbackCameraOrientation)
            cameraPosition = snapbackCameraPosition
            cameraOrientation = snapbackCameraOrientation
        snapback = False
    elif(rotating == True and e.getServiceType() == ServiceType.Pointer 
        and e.getType() == EventType.Move):
        dx = e.getPosition().x - startPos.x
        dy = e.getPosition().y - startPos.y
        rot = Quaternion.new_rotate_euler(radians(dx / 10), radians(dy / 10), 0)
        cameraPosition = rot * (cameraPosition - pivotPosition) + pivotPosition
        cameraOrientation = rot * cameraOrientation
        camera.setOrientation(cameraOrientation)
        camera.setPosition(cameraPosition)
        if(not snapback): dqon()
        startPos = e.getPosition()

    # Panning control
    ps = panSpeed
    #print "Source is: ", e.getSourceId()
    #print "Keyboard A : " , int(Keyboard.KEY_A)
    if(e.isKeyDown(Keyboard.KEY_A)): panVector.x -= ps
    elif(e.isKeyUp(Keyboard.KEY_A)): panVector.x = 0
    if(e.isKeyDown(Keyboard.KEY_D)): panVector.x += ps
    elif(e.isKeyUp(Keyboard.KEY_D)): panVector.x = 0
    if(e.isKeyDown(Keyboard.KEY_S)): panVector.z += ps
    elif(e.isKeyUp(Keyboard.KEY_S)): panVector.z = 0
    if(e.isKeyDown(Keyboard.KEY_W)): panVector.z -= ps
    elif(e.isKeyUp(Keyboard.KEY_W)): panVector.z = 0
    if(e.isKeyDown(Keyboard.KEY_R)): panVector.y += ps
    elif(e.isKeyUp(Keyboard.KEY_R)): panVector.y = 0
    if(e.isKeyDown(Keyboard.KEY_F)): panVector.y -= ps
    elif(e.isKeyUp(Keyboard.KEY_F)): panVector.y = 0


def onUpdate(frame, time, dt):
    global pivotPosition
    global cameraPosition
    global cameraOrientation
    global panSpeedMultiplier
    
    if(panVector.magnitude() > 0): 
        dqon()
        cameraPosition += cameraOrientation * panVector * dt * panSpeedMultiplier
        camera.setPosition(cameraPosition)
    #camera.lookAt(pivot.getPosition(), Vector3(0,1,0))
    # cange the pan speed multiplier depending on how far
    # we are from the object, so panning speed looks constant
    l = (cameraPosition - pivotPosition).magnitude()
    panSpeedMultiplier = 0.1 + abs(l / 100)
    
    # update info ui
    #cameraInfo.setText(str(getDefaultCamera().getPosition()))
    #pivotInfo.setText(str(pivotPosition) + ' d=' + str(pivotDistance))

setEventFunction(onEvent)
setUpdateFunction(onUpdate)