''' Setup flying. '''

from omega import *
from euclid import *
from math import *

cameraPosition = Vector3(0,0,0)
cameraOrientation = Quaternion()
pivotRayOrigin = Vector3(0, 0, 0)
pivotRayDirection = Vector3(0,0,-1)
pivotDistance = -62
pivotDistanceIncrement = 2
    
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
    global panVector
    global panSpeed
    
    e = getEvent()
    portholeS = porthole.getService()
    
    # Mouse wheel = move the center of rotation along the pointer view ray
    if(e.getType() == EventType.Zoom):
        # print " Before: ", pivotPosition
        pivotDistance += e.getExtraDataInt(0) * pivotDistanceIncrement * panSpeedMultiplier
        # print e.getExtraDataInt(0), " : ", pivotDistance, " PivRayDir: ", pivotRayDirection, " Orig: ", pivotRayOrigin
        pivotPosition = pivotRayOrigin + pivotRayDirection * pivotDistance 
        # pivotPosition[0] = 47.0
        # pivotPosition[1] = 17.0
        # print "PivPos: ",pivotPosition, " CamPos: " , cameraPosition
        portholeS.broadcastjs('updateCenterOfRotation('+str(pivotPosition[0])+','+str(pivotPosition[1])+','+str(pivotPosition[2])+')','')
        return
    
    if(e.isButtonDown(EventFlags.Left)):
        # ctrl + mouse click: go to pivot selection mode
        if(e.isFlagSet(EventFlags.Ctrl)):
            res = getRayFromEvent(e)
            if(res[0] == True):
                pivotRayOrigin = res[1]
                pivotRayDirection = res[2]
                pivotDistance = abs(pivotPosition - pivotRayOrigin)
                pivotPosition = pivotRayOrigin + pivotRayDirection * pivotDistance 
                portholeS.broadcastjs('updateCenterOfRotation('+str(pivotPosition[0])+','+str(pivotPosition[1])+','+str(pivotPosition[2])+')','')
        
        # start rotating the model
        startPos = e.getPosition()
        rotating = True
        cameraOrientation = camera.getOrientation()
        cameraPosition = camera.getPosition()
        
    elif(e.isButtonUp(EventFlags.Left)):
        # mouse button released. end rotation
        rotating = False
        cameraOrientation = camera.getOrientation()
        cameraPosition = camera.getPosition()
        
    elif(rotating == True and e.getServiceType() == ServiceType.Pointer 
        and e.getType() == EventType.Move):
        
        # if the mouse is moving and we are rotating the model, compute the new
        # camera position and orientation. The camera rotates around the pivot point,
        # based on mouse movement
        dx = startPos.x - e.getPosition().x
        dy = startPos.y - e.getPosition().y
        
        # compute the rotation basis and the new rotation
        left = cameraOrientation * Vector3(1,0,0)
        up = cameraOrientation * Vector3(0,1,0)
        rot = Quaternion.new_rotate_axis(radians(dy / 10), left)
        rot = rot * Quaternion.new_rotate_axis(radians(dx / 10), up)
        
        # Rotate the camera around the pivot
        newPosition = rot * (cameraPosition - pivotPosition) + pivotPosition
        camera.setOrientation(rot * cameraOrientation)
        camera.setPosition(newPosition)
        redraw()

    # Panning control
    ps = panSpeed
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
    
    # if we are moving, update the camera position based on movement vector and
    # speed, then redraw.
    if(panVector.magnitude() > 0): 
        redraw()
        cameraPosition += cameraOrientation * panVector * dt * panSpeedMultiplier
        camera.setPosition(cameraPosition)

        # cange the pan speed multiplier depending on how far
    # we are from the object, so panning speed looks constant
    l = (cameraPosition - pivotPosition).magnitude()
    panSpeedMultiplier = 0.1 + abs(l / 100)

setEventFunction(onEvent)
setUpdateFunction(onUpdate)

def enablePivotSelectorMode(enabled):
    global pivotSelectionMode
    pivotSelectionMode = enabled
    if(enabled):
        for p in parts:
            p.setData(None)
            p.setProgram(prog_df)
            p.setPointScale(scale)
        pcw.enableColormapper(False)
        for p in parts: p.setDecimation(dqDec)
        camera.setSceneEnabled(True)
    else:
        # Reset previous view mode
        setDataMode(dataMode)
        setPointScale(pointScale)
        enableColormapper(colormapperEnabled)
        updateColormapBounds(colormapMin, colormapMax)
        redraw()

def resetPivot():
    global pivotPosition
    pivotPosition = sn.getBoundCenter()
    print("Pivot position: " + str(pivotPosition))
 
def setCamPos(x,y,z):
    global camera, cameraPosition
    oldPos = camera.getPosition()
    cameraPosition = Vector3(float(x),float(y),float(z))
    print "camera position set to:" , cameraPosition
    camera.setPosition(cameraPosition)
    redraw()
    #camera.setPosition(Vector3(float(x),float(y),float(z)))

def setCamOrientation(w,ix,iy,iz):
    global cameraOrientation
    newQuat = Quaternion.new_rotate_axis(w,ix,iy,iz)
    # print "Setting New Camera Orientation" ,newQuat
    cameraOrientation = newQuat
    camera.setOrientation(cameraOrientation)

def setCamNearFar(nearPlane, farPlane):
    camera.setCamNearFarZ(nearPlane,farPlane)

def setPivotPoint(x,y,z):
    global pivotPosition
    print "setting pivot point to to x:" , x ," y: ", y , " z: ", z
    pivotPosition = Vector3(float(x),float(y),float(z))

def lookAtPivot():
    print "looking at pivot point"
    global camera, pivotPosition
    camera.lookAt(pivotPosition,Vector3(0,1,0))
    redraw()

def requestUpdatePos():
    global cameraPosition
    ps.broadcastjs('updateCameraPos('+str(cameraPosition[0])+','+str(cameraPosition[1])+','+str(cameraPosition[2])+')','')

print 'flyControl.py done'
print ''
