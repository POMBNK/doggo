import numpy as np
import matplotlib.pyplot as plt

"""
Last well working robot config
r = 120
drop = 130
x = {70, step:1}
"""

def saveFile(values,fileName:str):
    with open(fileName+".txt", 'w') as file:
        for row in values:
            file.write(str(row)+'\n')

r = 120 # max height of step
drop = 130 # height from zero to upper servo
l1 = l2 = 100 # legth of legs
x_step = np.arange(70,-70,-1) # range of step
x_skip = np.arange(-70,70,1) 
x_full = np.concatenate((x_step,x_skip))
y_step=np.zeros(np.size(x_step))
y_skip=np.zeros(np.size(x_skip))
h_step=np.zeros(np.size(x_step))
h_skip=np.zeros(np.size(x_skip))
delta = np.sqrt(r**2-x_skip[0]**2)

for i in range(len(x_step)):
	y = 0
	y_step[i]=y

for i in range(len(x_skip)):
	y = np.sqrt((r**2) - (x_skip[i]**2)) - delta
	y_skip[i]=y

hip_step = np.zeros(np.size(x_step))
knee_step = np.zeros(np.size(x_step))

hip_skip = np.zeros(np.size(x_skip))
knee_skip = np.zeros(np.size(x_skip))
t= np.arange(0,np.size(x_skip),1)
t_full = np.arange(0,np.size(x_full))
for i in range(len(x_step)):
   
    # walk with R    

    #pitch = MPU6050.Scan()...
    # elev = l/2 *sin(pitch)
    # offset = np.asin(elev/105) 105 = 211/2 - половина длины корпуса
    #F_knee_step = 2*np.arcsin(np.sqrt(x_step[i]**2+(drop_f-y_step[i])**2)/(2*l1))+hip_offset
    # может тут учитывать отклонение по гироскопу drop +- elev и +-offset в углах в конце 

    hip_step[i] = 0.5*np.pi - np.arccos(np.sqrt(x_step[i]**2+(drop-y_step[i])**2)/(2*l1))+np.arctan(x_step[i]/(drop-y_step[i]))
    knee_step[i] = 2*np.arcsin(np.sqrt(x_step[i]**2+(drop-y_step[i])**2)/(2*l1))
    
    h1 = l1*np.cos(0.5*np.pi-hip_step[i])
    h2 = l2*np.sin(knee_step[i]-hip_step[i])
    h_step[i]=h1+h2

for i in range(len(x_skip)):
   
    # walk with R    
    hip_skip[i] = 0.5*np.pi - np.arccos(np.sqrt(x_skip[i]**2+(drop-y_skip[i])**2)/(2*l1))+np.arctan(x_skip[i]/(drop-y_skip[i]))
    knee_skip[i] = 2*np.arcsin(np.sqrt(x_skip[i]**2+(drop-y_skip[i])**2)/(2*l1))
    
    h1 = l1*np.cos(0.5*np.pi-hip_skip[i])
    h2 = l2*np.sin(knee_skip[i]-hip_skip[i])
    h_skip[i]=h1+h2


# saveFile(np.rad2deg(hip_skip),"hip_skip_degree")
# saveFile(np.rad2deg(knee_skip),"knee_skip_degree")
# saveFile(np.rad2deg(hip_step),"hip_step_degree")
# saveFile(np.rad2deg(knee_step),"knee_skip_degree")

# # make together
# hip_ful = np.zeros(np.size(hip_step)+np.size(hip_skip))
# knee_ful = np.zeros(np.size(knee_step)+np.size(knee_skip))

hip_step_skip = np.concatenate((hip_step,hip_skip))
hip_skip_step = np.concatenate((hip_skip,hip_step))
knee_step_skip = np.concatenate((knee_step,knee_skip))
knee_skip_step = np.concatenate((knee_skip,knee_step))

saveFile(np.rad2deg(hip_step_skip),"hip_step_skip_degree")
saveFile(np.rad2deg(hip_skip_step),"hip_skip_step_degree")

saveFile(np.rad2deg(knee_step_skip),"knee_step_skip_degree")
saveFile(np.rad2deg(knee_skip_step),"knee_skip_step_degree")


hip_ful = np.concatenate((hip_step,hip_skip))
knee_ful = np.concatenate((knee_step,knee_skip))

fig, ax = plt.subplots()
fig2, ax2 = plt.subplots()
ax.plot(t_full,np.rad2deg(hip_ful))
ax.plot(t_full,np.rad2deg(knee_ful))

# ax.plot(t,np.rad2deg(hip_skip))
# ax.plot(t,np.rad2deg(hip_skip))
# ax.plot(t,np.rad2deg(knee_step))
# ax.plot(t,np.rad2deg(knee_skip))
ax.legend(["hip","knee"])
t_phis = np.arange(0,6.28,0.1)
#ax2.plot( *xy(r,phis), c='r',ls='-' )
#ax2.plot(x,y)
ax2.plot(x_step,h_step)
ax2.plot(x_skip,h_skip)




# ax.plot(t,np.rad2deg(hip_step))
# ax.plot(t,np.rad2deg(knee_step))
# ax2.plot(t,hip_step)
plt.show()