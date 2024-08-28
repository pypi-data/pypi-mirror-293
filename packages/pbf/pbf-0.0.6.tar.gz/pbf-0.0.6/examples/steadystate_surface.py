import pbf, numpy as np, matplotlib.pyplot as plt
units = pbf.units

IN625 = pbf.makeMaterial("IN625")
#IN625 = pbf.readMaterialFile("materials/IN625.json")

laserD4Sigma = 170 * units.um
laserSpeed = 800 * units.mm / units.s
laserPower = 180 * units.W
absorptivity = 0.32
layerHeight = 0.0 * units.um

x0 = 0.25 * units.mm;
x1 = 0.75 * units.mm;
dur = ( x1 - x0 ) / laserSpeed

elementSize = 16 * units.um;
        
laserTrack = [pbf.LaserPosition(xyz=[x0, 0.0 * units.mm, layerHeight], time=0.0 * units.s, power=laserPower),
              pbf.LaserPosition(xyz=[x1, 0.0 * units.mm, layerHeight], time=dur, power=laserPower)]

# Setup beam shape
pixelsize = 8 * units.um

X, Y = np.mgrid[-20:20, -20:20]
pixels = np.exp(-(X**2 + Y**2) / (2 * (laserD4Sigma/4)**2 / pixelsize**2))
pixels = pixels / (np.sum(pixels) * pixelsize**2)
laserBeam = pbf.beamShapeFromPixelMatrix(absorptivity * pixels, pixelsize)

#plt.contourf(pixels)
#plt.colorbar()
#plt.show()

#heatSource = pbf.volumeSource(laserTrack, laserBeam, depthSigma=0.045)
heatSource = pbf.surfaceSource(laserTrack, laserBeam)

# Setup problem
domainMin = [0.0 * units.mm, -0.3 * units.mm, -0.2 * units.mm]
domainMax = [1.0 * units.mm,  0.3 * units.mm, layerHeight]

filebase = "outputs/steadystate_surface"
grid = pbf.createMesh(domainMin, domainMax, elementSize, layerHeight, zfactor=0.5)

tsetup = pbf.ThermalProblem( )
tsetup.addPostprocessor(pbf.thermalVtuOutput(filebase))
#tsetup.addPostprocessor(pbf.meltPoolContourOutput(filebase))
tsetup.addPostprocessor(pbf.meltPoolBoundsPrinter())
tsetup.setMaterials({"powder" : IN625, "structure" : IN625, "baseplate" : IN625, "air" : IN625})
tsetup.addDirichletBC(pbf.temperatureBC(1, tsetup.ambientTemperature))
tsetup.addSource(heatSource) 

tstate = pbf.makeThermalState(tsetup, grid, time=dur)

pbf.computeSteadyStateThermal(tsetup, tstate, [laserSpeed, 0, 0])
