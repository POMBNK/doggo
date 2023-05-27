import matplotlib.pyplot as plt

# full_hip = []
# full_knee = []
# with open("hip_full_n.txt", 'r') as hip:
#     for line in hip:
#         # remove linebreak from a current name
#         # linebreak is the last character of each line
#         x = line[:-1]

#         # add current item to the list
#         full_hip.append(float(x))

# with open("knee_full_n.txt", 'r') as knee:
#     for line in knee:
#         # remove linebreak from a current name
#         # linebreak is the last character of each line
#         y = line[:-1]

#         # add current item to the list
#         full_knee.append(float(y))

# plt.plot(full_hip)
# plt.plot(full_knee)

# full_hip = []
# full_knee = []
# with open("hip_fulFL.txt", 'r') as hip:
#     for line in hip:
#         # remove linebreak from a current name
#         # linebreak is the last character of each line
#         x = line[:-1]

#         # add current item to the list
#         full_hip.append(float(x))

# with open("knee_fulFL.txt", 'r') as knee:
#     for line in knee:
#         # remove linebreak from a current name
#         # linebreak is the last character of each line
#         y = line[:-1]

#         # add current item to the list
#         full_knee.append(float(y))

# plt.plot(full_hip)
# plt.plot(full_knee)

full_hip = []
full_knee = []
with open("h_step_FL.txt", 'r') as hip:
    for line in hip:
        # remove linebreak from a current name
        # linebreak is the last character of each line
        x = line[:-1]

        # add current item to the list
        full_hip.append(float(x))

with open("h_skip_FL.txt", 'r') as knee:
    for line in knee:
        # remove linebreak from a current name
        # linebreak is the last character of each line
        y = line[:-1]

        # add current item to the list
        full_knee.append(float(y))

plt.plot(full_hip)
#plt.plot(full_knee)


plt.show()