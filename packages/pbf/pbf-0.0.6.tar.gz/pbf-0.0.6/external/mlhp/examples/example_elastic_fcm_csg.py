import mlhp

D = 3

print("1. Setting up mesh and basis", flush=True)

origin, max = [-0.78] * D, [0.78] * D

sphere = mlhp.implicitSphere( [0.0, 0.0, 0.0], 1.0 )
cube = mlhp.implicitCube(origin, max)
intersection = mlhp.implicitIntersection([sphere, cube])

circle = mlhp.implicitSphere([0, 0], 0.4)

cylinder1 = mlhp.extrude(circle, -1.0, 1.0, 0)
cylinder2 = mlhp.extrude(circle, -1.0, 1.0, 1)
cylinder3 = mlhp.extrude(circle, -1.0, 1.0, 2)

cylinders = mlhp.implicitUnion([cylinder1, cylinder2, cylinder3])
domain = mlhp.implicitSubtraction([intersection, cylinders])

scaling = 2 * 2.5 / 0.78

domain = mlhp.implicitTransformation(domain, mlhp.scaling([scaling] * D))

# Setup discretization
youngsModulus = 200 * 1e9
poissonsRatio = 0.3

polynomialDegree = 1
nelements = [50] * D
alphaFCM = 1e-8
penalty = 1e5 * youngsModulus

# ##################### FIX ####################
origin = [scaling * o - 1e-10 for o in origin]
max = [scaling * m + 1e-10 for m in max]

lengths = [m - o for o, m in zip(origin, max)]

grid = mlhp.makeGrid(nelements, lengths, origin)
print(grid)

grid = mlhp.makeRefinedGrid(mlhp.filterCells(grid, domain, nseedpoints=polynomialDegree + 2))
basis = mlhp.makeHpTrunkSpace(grid, degrees=polynomialDegree, nfields=D)

print(grid)
print(basis)

resolution = [polynomialDegree + 3] * D
triangulation, celldata = mlhp.marchingCubesBoundary(grid, domain, resolution)

print(basis)

print("2. Allocating linear system", flush=True)

matrix = mlhp.allocateUnsymmetricSparseMatrix(basis)
vector = mlhp.allocateVectorWithSameSize(matrix)

print("3. Computing weak boundary integrals", flush=True)

def createBoundaryQuadrature(func):
    filteredTriangulation, filteredCelldata = mlhp.filterTriangulation(triangulation, celldata, mlhp.implicitFunction(D, func))
    quadrature = mlhp.triangulationQuadrature(filteredTriangulation, filteredCelldata, polynomialDegree + 1)
    
    return filteredTriangulation, filteredCelldata, quadrature
    
intersected0, celldata0, quadrature0 = createBoundaryQuadrature(f"x < {origin[0] + 1e-3}")
intersected1, celldata1, quadrature1 = createBoundaryQuadrature(f"x > {origin[0] + lengths[0] - 1e-3}")

integrand0 = mlhp.l2BoundaryIntegrand(mlhp.vectorField(D, [penalty] * D),
                                      mlhp.vectorField(D, [0.0] * D))

integrand1 = mlhp.neumannIntegrand(mlhp.vectorField(D, [1e3, 0.0, 0.0]))

mlhp.integrateOnSurface(basis, integrand0, [matrix, vector], quadrature0)
mlhp.integrateOnSurface(basis, integrand1, [vector], quadrature1)

print("4. Computing domain integral", flush=True)

E = mlhp.scalarField(D, 200 * 1e9)
nu = mlhp.scalarField(D, 0.3)
rhs = mlhp.vectorField(D, [0.0, 0.0, 0.0])

kinematics = mlhp.smallStrainKinematics(D) 
constitutive = mlhp.isotropicElasticMaterial(E, nu)
integrand = mlhp.staticDomainIntegrand(kinematics, constitutive, rhs)

quadrature = mlhp.spaceTreeQuadrature(domain, 
    depth=polynomialDegree + 1, epsilon=alphaFCM)

#quadrature = mlhp.momentFittingQuadrature(domain, 
#    depth=polynomialDegree + 3, epsilon=alphaFCM)

mlhp.integrateOnDomain(basis, integrand, [matrix, vector], quadrature=quadrature)

print("6. Solving linear system", flush=True)

#P = mlhp.additiveSchwarzPreconditioner(matrix, basis, dirichlet[0])
P = mlhp.diagonalPreconditioner(matrix)

dofs, norms = mlhp.cg(matrix, vector, tolerance=1e-12, preconditioner=P, maxit=2000, residualNorms=True)

#print(f"cond K after domain integral: {numpy.linalg.cond(matrix.todense())}")
#import matplotlib.pyplot as plt
#plt.loglog(norms)
#plt.show()

print("7. Postprocessing solution", flush=True)

# Output solution on FCM mesh and boundary surface
gradient = mlhp.projectGradient(basis, dofs, quadrature)

processors = [mlhp.solutionProcessor(D, dofs, "Displacement"),
              mlhp.stressProcessor(gradient, kinematics, constitutive),
              mlhp.vonMisesProcessor(dofs, kinematics, constitutive, "VonMises1"),
              mlhp.vonMisesProcessor(gradient, kinematics, constitutive, "VonMises2"),
              mlhp.strainEnergyProcessor(gradient, kinematics, constitutive)]

surfmesh = mlhp.associatedTrianglesCellMesh(triangulation, celldata)

writer0 = mlhp.PVtuOutput(filename="outputs/linear_elasticity_fcm_stl_boundary")
writer1 = mlhp.PVtuOutput(filename="outputs/linear_elasticity_fcm_stl_fcmmesh")

mlhp.writeBasisOutput(basis, surfmesh, writer0, processors)
mlhp.writeBasisOutput(basis, writer=writer1, processors=processors)
#mlhp.writeBasisOutput(basis, mlhp.quadraturePointCellMesh(quadrature, basis), writer=mlhp.PVtuOutput(filename="outputs/linear_elasticity_fcm_stl_quadraturepoints"), processors=[])

# Output boundary surfaces
surfmesh0 = mlhp.associatedTrianglesCellMesh(intersected0, celldata0)
surfmesh1 = mlhp.associatedTrianglesCellMesh(intersected1, celldata1)

surfwriter0 = mlhp.VtuOutput(filename="outputs/linear_elasticity_fcm_stl_boundary0")
surfwriter1 = mlhp.VtuOutput(filename="outputs/linear_elasticity_fcm_stl_boundary1")
            
mlhp.writeBasisOutput(basis, surfmesh0, surfwriter0, processors)
mlhp.writeBasisOutput(basis, surfmesh1, surfwriter1, processors)
