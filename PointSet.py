from cyclops import *
from pointCloud import *
#from sceneTools import spin_navigation
from math import *
import sys


scene = getSceneManager()
scene.addLoader(BinaryPointsLoader())

starProgram = ProgramAsset()
starProgram.name = "star"
starProgram.vertexShaderName = "star.vert"
starProgram.fragmentShaderName = "star.frag"
scene.addProgram(starProgram)

gasProgram = ProgramAsset()
gasProgram.name = "gas"
gasProgram.vertexShaderName = "gas.vert"
gasProgram.fragmentShaderName = "gas.frag"
scene.addProgram(gasProgram)


class PointSet:
    def __init__(self, file, color, pointScale):
        self.pointScale = Uniform.create('pointScale', UniformType.Float, 1)
        self.pointScale.setFloat(pointScale)
        
        self.color = Uniform.create('color', UniformType.Color, 1)
        self.color.setColor(color)
        
        self.model = ModelInfo()
        self.model.name = file
        self.model.path = file
        self.model.options = "200000 500:1000000:20 200:500:8 50:200:4 0:50:1"
        scene.loadModel(self.model)

        self.object = StaticObject.create(self.model.name)
        # attach shader uniforms
        self.material = self.object.getMaterial()
        self.material.setProgram(starProgram.name)
        self.material.attachUniform(self.pointScale)
        self.material.attachUniform(self.color)
        self.material.setTransparent(True, True)
        self.material.setAdditive(True)
        self.material.setDepthTestEnabled(False)
        
        self.material.setDiffuseTexture('star1.png')
        self.material.setPointSprite(True)
