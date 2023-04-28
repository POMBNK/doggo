import numpy as np
import Robot 
import matplotlib.pyplot as plt

r=120
drop=150
doggo = Robot.Robot(r,drop)
x_range_step = np.arange(70,-70,-5)
x_range_skip = np.arange(-70,70,5)
min_delta = x_range_skip[0]
#doggo.start(x_range_step,x_range_skip)

# to collect data
x_full = np.concatenate((x_range_step,x_range_skip))
t_full = np.arange(0,np.size(x_full))
hip_step = np.zeros(np.size(x_range_step))
knee_step = np.zeros(np.size(x_range_step))
hip_skip = np.zeros(np.size(x_range_skip))
knee_skip = np.zeros(np.size(x_range_skip))

flag = True
while flag:
    for i in range(len(x_range_step)):
        hip,knee=doggo.callculate_step(x_range_step[i])
        #doggo.move_step_skip(x_range_step[i],x_range_skip[i],min_delta)
        # collecting data
        hip_step[i] = hip
        knee_step[i] = knee

    for i in range(len(x_range_skip)):
        hip,knee=doggo.callculate_skip(x_range_skip[i],min_delta)
        #doggo.move_skip_step(x_range_step[i],x_range_skip[i])
        #collecting data
        hip_skip[i] = hip
        knee_skip[i] = knee

    flag = False

hip_ful = np.concatenate((hip_step,hip_skip))
knee_ful = np.concatenate((knee_step,knee_skip))

fig, ax = plt.subplots()
ax.plot(t_full,hip_ful)
ax.plot(t_full,knee_ful)
ax.legend(["hip","knee"])
plt.show()