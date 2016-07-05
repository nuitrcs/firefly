from omega import *
from euclid import *

def setViewport(id):
    print("setting viewport " + str(id))

def saveViewport(id):
    print("saving viewport " + str(id))


def onEvent():
    e = getEvent()
    
    if(e.isKeyDown(ord("1"))): 
        if(e.isFlagSet(EventFlags.Shift)): saveViewport(1)
        else: setViewport(1)
    if(e.isKeyDown(ord("2"))): 
        if(e.isFlagSet(EventFlags.Shift)): saveViewport(2)
        else: setViewport(2)
    if(e.isKeyDown(ord("3"))): 
        if(e.isFlagSet(EventFlags.Shift)): saveViewport(3)
        else: setViewport(3)
    if(e.isKeyDown(ord("4"))): 
        if(e.isFlagSet(EventFlags.Shift)): saveViewport(4)
        else: setViewport(4)
    

setEventFunction(onEvent)