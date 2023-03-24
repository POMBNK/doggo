import matplotlib.pyplot as plt
import numpy as np

# Trajectory for test Inverse kinematick and forward kinematic results.
r = 60
drop = 105
def xy(r,phi):
        return r*np.cos(phi), r*np.sin(phi) - drop

fig = plt.figure()
ax = fig.add_subplot(111,aspect='equal')

phis=np.arange(0,6.28,0.01)

for x in range(-40, 41, 1):
        y = np.sqrt((r**2) - (x**2)) - drop
        print(x,round(-y, 1))

ax.plot( *xy(r,phis), c='r',ls='-' )
plt.show()