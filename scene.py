# create a point cloud view. This object takes care of rendering and generates
# an image we can place on screen or save to disk. 
pcw = PointCloudView()
pcw.setColormapper(prog_mapper)

# we assume parts is a list containing all the point clouds we want to render
# (parts is populated by loader.py)
for p in parts: pcw.addPointCloud(p)

# create a 2D overlay to display the image rendered by the point cloud view
mainView = Overlay()
mainView.setAutosize(True)
mainView.setTexture(pcw.getOutput())

# create a scene node to handle the 3D scene, attach all the point cloud objects
# to it. 
sn = SceneNode.create('galaxy')
sn.setScale(scale, scale, scale)
for p in parts: 
    sn.addComponent(p)
    p.setPointScale(scale)
