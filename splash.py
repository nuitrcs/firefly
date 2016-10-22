# Omium is the web renderer. we use it to render the user interface
o = Omium.getInstance()

# start up the web server that will serve the user interface.
porthole.initialize(4080, './splash.html')
ps = porthole.getService()
ps.setServerStartedCommand('loadUi()')

getDefaultCamera().setBackgroundColor(Color('white'))

# called when the user interface is ready. Create an overlay to display it.
def loadUi():
    global gui
    global p
    gui = Overlay()
    p = o.getPixels()
    guifx = OverlayEffect()
    guifx.setShaders('overlay/overlay.vert', 'overlay/overlay-flipy.frag')
    gui.setTexture(p)
    gui.setAutosize(True)
    gui.setEffect(guifx)
    o.open('http://localhost:4080')
    onResize()

getDisplayConfig().canvasChangedCommand = 'onResize()'
def onResize():
    r = getDisplayConfig().getCanvasRect()
    o.resize(r[2], r[3])
