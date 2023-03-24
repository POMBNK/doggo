import numpy as np
import matplotlib.pyplot as plt

# drop = 45
# slew = 0

#delete this later. Testing forward and inverse Kinematic
#-----------------------------------------------
def xy(r,phi):
	return r*np.cos(phi), r*np.sin(phi) - drop
phis=np.arange(0,6.28,0.01)
#-----------------------------------------------
def saveFile(values,fileName:str):
    with open(fileName+".txt", 'w') as file:
        for row in values:
            file.write(str(row)+'\n')

r = 60 # max height of step?
drop = 105 # height from zero to upper servo
x= np.arange(-40,40,0.01)
y=np.zeros(np.size(x))

for i in range(len(x)):
	yy = np.sqrt((r**2) - (x[i]**2)) - drop
	y[i]=yy

hip = np.zeros(np.size(x))
knee = np.zeros(np.size(x))
t= np.arange(0,80,0.01)
for i in range(len(x)):
    hypotenuse = np.sqrt(y[i]**2+x[i]**2)
    phi_1 = np.arccos((hypotenuse**2)/(100*hypotenuse))
    phi_2 = np.arctan(x[i]/y[i])
    hip[i] = 90+(np.rad2deg(phi_2-phi_1))
    knee[i] = np.rad2deg(np.arccos(1-((hypotenuse**2)/5000)))
    #print('hip: ', hip, ' knee: ', knee)
#print('hip: ', np.deg2rad(hip[0]), ' knee: ', np.deg2rad(knee[0]))
#print('hip: ', np.deg2rad(hip[len(hip)-1]), ' knee: ', np.deg2rad(knee[len(knee)-1]))


saveFile(hip,"hip_degree")
saveFile(knee,"knee_degree")


fig, ax = plt.subplots()
fig2, ax2 = plt.subplots()
ax.plot(t,hip)
ax.plot(t,knee)
ax.legend(["hip","knee"])
t_phis = np.arange(0,6.28,0.01)
ax2.plot( *xy(r,phis), c='r',ls='-' )
ax2.plot(x,y)
plt.show()