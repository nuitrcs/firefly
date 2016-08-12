dqTimeout = 0.1
dqTimer = 0
dqDec = 4
dqCurDec = 1

# Enable dynamic quality
def dqon():
    # enable continuous drawing
    camera.setSceneEnabled(True)
    global dqTimer
    global dqCurDec
    dqTimer = dqTimeout
    for p in parts:
        p.setDecimation(dqDec)
        dqCurDec = dqDec

def dqupdate(frame, time, dt):
    global dqTimer
    global dqCurDec
    if(dqTimer > 0):
        dqTimer -= dt
    elif(dqCurDec > 1):
            dqCurDec = int(dqCurDec / 2)
            for p in parts: p.setDecimation(dqCurDec)
            if(dqCurDec == 1):
                # draw one high quality frame, then stop.
                queueCommand('camera.setSceneEnabled(False)')

setUpdateFunction(dqupdate)