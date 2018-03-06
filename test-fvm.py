from fipy import *
import numpy as np
import skimage.io as io
from skimage.util import invert


test_stack = io.imread('/Volumes/HD_1/LeafAir-WorkDir/Helwingia-test-stack.tif')
test_stack_flat = test_stack.flatten()

dx = 1.277 #um


# 2D example
# Get first slice
test_2D = test_stack[1]
io.imshow(test_2D)
#subset first slice
test_2D = invert(test_2D[75:150,])
io.imshow(test_2D)

test_2D_flat = test_2D.flatten(order='F')
set(test_2D_flat) # get unique values

nx, ny = test_2D.shape
print(nx, ny)
L = dx * nx

mesh_2D = Grid2D(dx=dx, dy=dx, nx=nx, ny=ny)
mesh_2D

X, Y = mesh_2D.faceCenters

air = CellVariable(mesh_2D, name='air', value=test_2D_flat == 0)
cells = CellVariable(mesh_2D, name='cells', value=test_2D_flat == 255)

air

# Setup a viewer to check if grid is OK
# The mesh is currently rotated, but I'll keep it as is for now
# and set the boundary conditions at the right place
if __name__ == '__main__':
    viewer = Viewer(vars=air, datamin=0., datamax=1.)
    viewer.plotMesh()

# Create the diffusion equation
D = 1.

eq = TransientTerm() == DiffusionTerm(coeff=D)

#Set the Drichlet boundary conditions
valueRight = 0
valueLeft = 1

faces_Right = (mesh_2D.facesRight & (Y > L / 2))
faces_Left = (mesh_2D.facesLeft & (Y > L / 2))

init.constrain(valueLeft, faces_Left)
init.constrain(valueRight, faces_Right)


if __name__ == '__main__':
    viewer = Viewer(vars=air, datamin=0., datamax=1.)
    viewer.plot()


timeStepDuration = 10 * 0.9 * dx**2 / (2 * D)
steps = 10
for step in range(steps):
    eq.solve(var=cells, dt=timeStepDuration)
    if __name__ == '__main__':
        viewer.plot()

print numerix.allclose(cells(((L,), (0,))), valueLeft, atol = 1e-2)

DiffusionTerm().solve(var=cells)
if __name__ == '__main__':
    viewer.plot()



## 3D EXAMPLE
nx = test_stack.shape[0]
ny = test_stack.shape[1]
nz = test_stack.shape[2]

mesh = Grid3D(dx=dx, dy=dx, dz=dx, nx=nx, ny=ny, nz=nz)
X, Y, Z = mesh.cellCenters

air = CellVariable(mesh=mesh, value=test_stack_flat)

D = 1.
eq = TransientTerm() == DiffusionTerm(coeff=D)




for x in range(0, size[0]):
	for y in range(0, size[1]):
		for y in range(0, size[2]):
			source.setValue(test_stack.getGrid()[x][y][z], where=(X < x + 1) & (X > x) & (Y > y) & (Y < y + 1) & (Z > z) & (Z < z + 1))
                