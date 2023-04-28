import numpy as np
import Robot 
import datetime as dt
import time as t
import matplotlib.pyplot as plt
import matplotlib.animation as animation

r=120
drop=150
doggo = Robot.Robot(r,drop)
# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []
ys2 = []
x_range_step = np.arange(70,-70,-1)


# This function is called periodically from FuncAnimation
def animate(i, xs, ys2,ys):

    hip,knee=doggo.callculate_step(x_range_step[i])

    # Add x and y to lists
    #xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    xs.append(i)

    # xs.append(i)
    ys2.append(hip)
    ys.append(knee)

    # Draw x and y lists
    ax.clear()
    ax.plot(xs,ys2,ys)
    ax.legend(["hip","knee"])

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Hip and knee angles')
    plt.ylabel('Angles (deg)')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys2,ys), interval=1)
plt.show()