dqTimeout = 0.1
dqTimer = 0
dqDec = 10
progressiveRender = True
dqCurDec = 1

# prog_default is used to display points directly, mapping one data dimension to
# point colors
prog_default = sig.addProgram('default')
prog_default.setVertexShader('shaders/point.vert')
prog_default.setGeometryShader('shaders/point.geom')
prog_default.setFragmentShader('shaders/point.frag')

# prog vector is used to display a line for each point (ie velocity vectors)
prog_vector = sig.addProgram('vector')
prog_vector.setVertexShader('shaders/vector.vert')
prog_vector.setGeometryShader('shaders/vector.geom')
prog_vector.setFragmentShader('shaders/vector.frag')

# prog_default is used to display points directly, using a fixed color for each
# point cloud
prog_fixedColor = sig.addProgram('fixedColor')
prog_fixedColor.setVertexShader('shaders/point.vert')
prog_fixedColor.setGeometryShader('shaders/point.geom')
prog_fixedColor.setFragmentShader('shaders/point-fixedColor.frag')

# prog_df is used to draw in pivot selection mode
prog_df = sig.addProgram('depthFilter')
prog_df.setVertexShader('shaders/point-depthFilter.vert')
prog_df.setGeometryShader('shaders/point-depthFilter.geom')
prog_df.setFragmentShader('shaders/point-depthFilter.frag')

# prog_channel is used for colormapped rendering: it draws points accumulating the
# data dimension values to the output, without performing a color mapping
prog_channel = sig.addProgram('channel')
prog_channel.setVertexShader('shaders/point.vert')
prog_channel.setGeometryShader('shaders/point.geom')
prog_channel.setFragmentShader('shaders/point-channel.frag')

# prog_mapper is the color mapping program used in conjunction with prog_channel
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

for p in programs:
    p.define('KERNEL_MODE', '0')
    p.define('RENDER_MODE', '0')
    p.define('LOG_MODE', '0')
    p.define('FILTER_MODE', '0')
    p.define('DATA_MODE', '0')
    p.define('SIZE_MODE', '0')
    
# Load colormaps 
colormaps = []
for cn in colorMapNames:
    colormaps.append(loadImage(cn))
for i in colormaps: i.setTextureFlags(TextureFlags.WrapClamp)

# When the program window resizes, notify all rendering components
getDisplayConfig().canvasChangedCommand = 'onResize()'
def onResize():
    r = getDisplayConfig().getCanvasRect()
    o.resize(r[2], r[3])
    pcw.resize(r[2], r[3])

# Start redrawing the 3D view 
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
    
    # Progressive rendering mode: increase the rendering quality each frame
    # (descreasing the decimation value passed to the point clouds) until the
    # decimation is back to one. At that point, render one last frame then disable
    # 3D scene rendering to save CPU/GPU resources, until the redraw() function is
    # called again
    if progressiveRender:
        if(dqTimer > 0):
            dqTimer -= dt
        elif(dqCurDec >= dqDec):
                print "Reset atnwitn---"
                dqCurDec = int(dqCurDec / 2)
                if(dqCurDec == 0): dqCurDec = 1
                for p in parts: p.setDecimation(dqCurDec)
                if(dqCurDec == 1):
                    # draw one high quality frame, then stop.
                    queueCommand('camera.setSceneEnabled(False)')
    else:
        if (dqCurDec != dqDec):
            print "Resetting-----"
            dqCurDec = int(dqDec)
            for p in parts: p.setDecimation(dqCurDec)

setUpdateFunction(onUpdate)