from omega import *
from euclid import *
from math import *

# Set this variable to the object that you want to rotate/scale.
root = None

# Disable the default camera controller since we do our own thing here.
camera = getDefaultCamera()
camera.setControllerEnabled(False)

startPos = None
rotating = False

# panning speed and vector
panSpeed = 50
panSpeedMultiplier = 1
panVector = Vector3(0,0,0)

def onEvent():
    global startPos
    global rotating
    global root
    global panVector
    global panSpeed
    
    e = getEvent()
    if(e.isButtonDown(EventFlags.Left)):
        startPos = e.getPosition()
        rotating = True
    elif(e.isButtonUp(EventFlags.Left)):
        rotating = False
    
    if(rotating == True and e.getServiceType() == ServiceType.Pointer 
    and e.getType() == EventType.Move):
        dx = e.getPosition().x - startPos.x
        dy = e.getPosition().y - startPos.y
        startPos = e.getPosition()
        root.rotate(Vector3(0, 1, 0), radians(dx), Space.World)
        root.rotate(Vector3(1, 0, 0), radians(dy), Space.World)

    # Panning control
    ps = panSpeed
    if(e.isKeyDown(ord('a'))): panVector.x -= ps
    elif(e.isKeyUp(ord('a'))): panVector.x = 0
    if(e.isKeyDown(ord('d'))): panVector.x += ps
    elif(e.isKeyUp(ord('d'))): panVector.x = 0
    if(e.isKeyDown(ord('s'))): panVector.z -= ps
    elif(e.isKeyUp(ord('s'))): panVector.z = 0
    if(e.isKeyDown(ord('w'))): panVector.z += ps
    elif(e.isKeyUp(ord('w'))): panVector.z = 0
    if(e.isKeyDown(ord('r'))): panVector.y -= ps
    elif(e.isKeyUp(ord('r'))): panVector.y = 0
    if(e.isKeyDown(ord('f'))): panVector.y += ps
    elif(e.isKeyUp(ord('f'))): panVector.y = 0



def onUpdate(frame, time, dt):
    camera.translate(panVector * dt * panSpeedMultiplier, Space.World)
    # cange the pan speed multiplier depending on how far
    # we are from the object, so panning speed looks constant
    global panSpeedMultiplier
    panSpeedMultiplier = 0.1 + abs(camera.getPosition().z / 100)

setEventFunction(onEvent)
setUpdateFunction(onUpdate)