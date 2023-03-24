import matplotlib.pyplot as plt
import numpy as np

# Getting angles for servo and
# Compare figures resulting trajectory with original trajectory

r = 60 
drop = 105 # height from zero to upper servo
x= np.arange(-40,40,0.1)
y=np.zeros(np.size(x))
def xy(r,phi):
	return r*np.cos(phi), r*np.sin(phi) - drop

phis=np.arange(0,6.28,0.01)

for i in range(len(x)):
	yy = np.sqrt((r**2) - (x[i]**2)) - drop
	y[i]=yy
	#y[i]=round(-yy,1)


print(f"x={x}")
print(f"y={y}")

fig, ax = plt.subplots()
ax.plot(*xy(r,phis),c='r',ls='-')
ax.plot(x, y,c='b',ls='--')
plt.show()