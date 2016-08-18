dqTimeout = 0.1
dqTimer = 0
dqDec = 1
dqCurDec = 1

prog_default = sig.addProgram('default')
prog_default.setVertexShader('shaders/point.vert')
prog_default.setGeometryShader('shaders/point.geom')
prog_default.setFragmentShader('shaders/point.frag')

prog_vector = sig.addProgram('vector')
prog_vector.setVertexShader('shaders/vector.vert')
prog_vector.setGeometryShader('shaders/vector.geom')
prog_vector.setFragmentShader('shaders/vector.frag')

prog_fixedColor = sig.addProgram('fixedColor')
prog_fixedColor.setVertexShader('shaders/point.vert')
prog_fixedColor.setGeometryShader('shaders/point.geom')
prog_fixedColor.setFragmentShader('shaders/point-fixedColor.frag')

prog_df = sig.addProgram('depthFilter')
prog_df.setVertexShader('shaders/point-depthFilter.vert')
prog_df.setGeometryShader('shaders/point-depthFilter.geom')
prog_df.setFragmentShader('shaders/point-depthFilter.frag')

prog_channel = sig.addProgram('channel')
prog_channel.setVertexShader('shaders/point.vert')
prog_channel.setGeometryShader('shaders/point.geom')
prog_channel.setFragmentShader('shaders/point-channel.frag')

prog_mapper = sig.addProgram('colormapper')
prog_mapper.setVertexShader('shaders/colormapper.vert')
prog_mapper.setFragmentShader('shaders/colormapper.frag')


programs = [
    prog_default, 
    prog_vector, 
    prog_fixedColor, 
    prog_df, 
    prog_channel, 
    prog_mapper]

# Load colormaps 
colormaps = []
for cn in colorMapNames:
    colormaps.append(loadImage(cn))
for i in colormaps: i.setTextureFlags(TextureFlags.WrapClamp)

getDisplayConfig().canvasChangedCommand = 'onResize()'
def onResize():
    r = getDisplayConfig().getCanvasRect()
    o.resize(r[2], r[3])
    pcw.resize(r[2], r[3])

def redraw():
    # enable continuous drawing
    camera.setSceneEnabled(True)
    global dqTimer
    global dqCurDec
    dqTimer = dqTimeout
    for p in parts:
        p.setDecimation(dqDec)
        dqCurDec = dqDec

timeSinceUpdate = 0
def onUpdate(frame, time, dt):
    global dqTimer
    global dqCurDec
    global timeSinceUpdate

    timeSinceUpdate = timeSinceUpdate + dt
    if timeSinceUpdate > 2:
        timeSinceUpdate = 0
        #global cameraPosition,pivotPosition
        #print "Updating, setting cameraPos: ", cameraPosition
        #ps.broadcastjs('updateCameraPos('+str(cameraPosition[0])+','+str(cameraPosition[1])+','+str(cameraPosition[2])+')','')
        #ps.broadcastjs()

    if(pivotSelectionMode): 
        for p in parts: p.setFocusPosition(pivotPosition)
        return
        
    if(dqTimer > 0):
        dqTimer -= dt
    elif(dqCurDec >= 1):
            dqCurDec = int(dqCurDec / 2)
            if(dqCurDec == 0): dqCurDec = 1
            for p in parts: p.setDecimation(dqCurDec)
            if(dqCurDec == 1):
                # draw one high quality frame, then stop.
                queueCommand('camera.setSceneEnabled(False)')

setUpdateFunction(onUpdate)