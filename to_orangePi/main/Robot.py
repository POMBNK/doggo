
    #COMMENT THIS IN REAL ORANGE PI ENV 
# import sys
# import fake_rpi

# fake_rpi.toggle_print(False)
# sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi
# sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake GPIO
# sys.modules['smbus'] = fake_rpi.smbus # Fake smbus (I2C)

    #COMMENT THIS IN REAL ORANGE PI ENV 

import math
import time
import numpy as np
import json
import os
import smbus
import PCA9685
import ServoPCA9685
import mpu6050
from ServoPCA9685 import map
import socket


X_RANGE_STEP_F_B = np.arange(50,-50,-10)
X_RANGE_SKIP_F_B = np.arange(-50,50,10)
MIN_DELTA_F_B = X_RANGE_SKIP_F_B[0]
DROP_F_B = 150
R_F_B = 125


X_RANGE_STEP_L_R = np.arange(50,-50,-10)
X_RANGE_SKIP_L_R = np.arange(-50,50,10)
MIN_DELTA_L_R = X_RANGE_SKIP_L_R[0]
DROP_R_L = 150
R_L_R = 125

def saveList(values,filename):
    with open(filename+".txt","w") as file:
        for item in values:
            file.write("%s\n" % item)
        print("Done")

def kalman(value, last_estimate, err_estimate): 
    err_measure = 0.09342
    spd = 0.1 # скорость измения значений 
    kalman_gain = err_estimate / (err_estimate + err_measure) 
    current_estimate = last_estimate + kalman_gain * (value - last_estimate) 
    err_estimate =  (1.0 - kalman_gain)*err_estimate + abs(last_estimate-current_estimate)*spd 
    return current_estimate, err_estimate


class Robot(object):
    def __init__(self):
        self.i2cBus = smbus.SMBus(2)
        self.pca9685 = PCA9685.PCA9685(self.i2cBus)
        self.mpu = mpu6050.MPU6050()
        self.l1=100
        self.l2=100
        #servos init once
        srv_data = json.load(open(os.path.dirname(__file__)+'/servo_pwm_dgr.json'))

        self.pitch_estimate = 0
        self.pitch_err = 1
        self.roll_estimate = 0
        self.roll_err = 1

        self.old_pitch = 0
        self.old_roll = 0
        
        #MPU angles metrics
        # self.roll_arr = []
        # self.pitch_arr = []
        
        # Servo angles metrics
        self.hip_fulFL = []
        self.knee_fulFL = []
        self.hip_fulFR = []
        self.knee_fulFR = []
        self.hip_fulBL = []
        self.knee_fulBL = []
        self.hip_fulBR = []
        self.knee_fulBR = []

        #Height metrics
        self.h_step_FL=[]
        self.h_skip_FL=[]

        self.servo_knee_r_f = ServoPCA9685.ServoPCA9685(self.pca9685, PCA9685.CHANNEL10, srv_data['krf']['pwm'], srv_data['krf']['dgr'])
        self.servo_hip_r_f = ServoPCA9685.ServoPCA9685 (self.pca9685, PCA9685.CHANNEL11, srv_data['hrf']['pwm'], srv_data['hrf']['dgr'])
        self.servo_knee_l_b = ServoPCA9685.ServoPCA9685 (self.pca9685, PCA9685.CHANNEL06, srv_data['klb']['pwm'], srv_data['klb']['dgr'])
        self.servo_hip_l_b = ServoPCA9685.ServoPCA9685 (self.pca9685, PCA9685.CHANNEL07, srv_data['hlb']['pwm'], srv_data['hlb']['dgr'])
        self.servo_knee_l_f = ServoPCA9685.ServoPCA9685 (self.pca9685, PCA9685.CHANNEL14, srv_data['klf']['pwm'], srv_data['klf']['dgr'])
        self.servo_hip_l_f = ServoPCA9685.ServoPCA9685 (self.pca9685, PCA9685.CHANNEL15, srv_data['hlf']['pwm'], srv_data['hlf']['dgr'])
        self.servo_knee_r_b = ServoPCA9685.ServoPCA9685 (self.pca9685, PCA9685.CHANNEL02, srv_data['krb']['pwm'], srv_data['krb']['dgr'])
        self.servo_hip_r_b = ServoPCA9685.ServoPCA9685 (self.pca9685, PCA9685.CHANNEL03, srv_data['hrb']['pwm'], srv_data['hrb']['dgr'])
        #self.start()
        time.sleep(3)
        self.mpu.dmpInitialize()
        self.mpu.setDMPEnabled(True)
        time.sleep(20)
        self.packetSize = self.mpu.dmpGetFIFOPacketSize() 

    # callculate_step return a servos angle to hip and knee from IK step pos
    def callculate_step_8L(self,x_range_step,drop):
        roll_ang,elev_ang = self.get_pitch_roll()
        # self.roll_arr.append(roll_ang)
        # self.pitch_arr.append(elev_ang)

        elev = 0.5*np.sin(elev_ang)*105
        roll = 0.5*np.sin(roll_ang)*83


        F_height = drop - elev
        B_height = drop + elev
        hip_offset = np.arcsin(elev / 105) #MagicNumber is 0.5*length longerone

        y_step=0
        F_height_slew = np.sqrt(x_range_step**2+(F_height-y_step)**2)
        B_height_slew = np.sqrt(x_range_step**2+(B_height-y_step)**2)
        
        FL_height = F_height_slew + roll
        FR_height = F_height_slew - roll
        BL_height = B_height_slew + roll
        BR_height = B_height_slew - roll

        FL_hip_step = 0.5*np.pi - np.arccos(FL_height/(2*self.l1))+np.arctan(x_range_step/(F_height-y_step)) + hip_offset
        FL_knee_step = 2*np.arcsin(FL_height/(2*self.l1))
        
        FR_hip_step = 0.5*np.pi - np.arccos(FR_height/(2*self.l1))+np.arctan(x_range_step/(F_height-y_step)) + hip_offset
        FR_knee_step = 2*np.arcsin(FR_height/(2*self.l1))
        
        BL_hip_step = 0.5*np.pi - np.arccos(BL_height/(2*self.l1))+np.arctan(x_range_step/(B_height-y_step)) + hip_offset
        BL_knee_step = 2*np.arcsin(BL_height/(2*self.l1))
        
        BR_hip_step = 0.5*np.pi - np.arccos(BR_height/(2*self.l1))+np.arctan(x_range_step/(B_height-y_step)) + hip_offset
        BR_knee_step = 2*np.arcsin(BR_height/(2*self.l1))

        hFL1 = self.l1*np.cos(0.5*np.pi-FL_hip_step)
        hFL2 = self.l2*np.sin(FL_knee_step-FL_hip_step)
        self.h_step_FL.append(hFL1+hFL2)

        return np.rad2deg(FL_hip_step),np.rad2deg(FL_knee_step),np.rad2deg(FR_hip_step),np.rad2deg(FR_knee_step),np.rad2deg(BL_hip_step),np.rad2deg(BL_knee_step),np.rad2deg(BR_hip_step),np.rad2deg(BR_knee_step)
    
        
    def callculate_skip_8L(self,x_range_skip,min_delta,drop,r):

        roll_ang,elev_ang = self.get_pitch_roll()
        # self.roll_arr.append(roll_ang)
        # self.pitch_arr.append(elev_ang)

        elev = 0.5*np.sin(elev_ang)*105
        roll = 0.5*np.sin(roll_ang)*83

    
        F_height = drop - elev
        B_height = drop + elev
        hip_offset = np.arcsin(elev / 105)

        delta = np.sqrt(r**2-min_delta**2) ## ERROR MAGIC -70
        y_skip = np.sqrt((r**2) - (x_range_skip**2)) - delta
        F_height_slew = np.sqrt(x_range_skip**2+(F_height-y_skip)**2)
        B_height_slew = np.sqrt(x_range_skip**2+(B_height-y_skip)**2)
        
        FL_height = F_height_slew + roll
        FR_height = F_height_slew - roll
        BL_height = B_height_slew + roll
        BR_height = B_height_slew - roll

        FL_hip_skip = 0.5*np.pi - np.arccos(FL_height/(2*self.l1))+np.arctan(x_range_skip/(F_height-y_skip)) + hip_offset #FL_height
        FL_knee_skip = 2*np.arcsin(FL_height/(2*self.l1))
        
        FR_hip_skip = 0.5*np.pi - np.arccos(FR_height/(2*self.l1))+np.arctan(x_range_skip/(F_height-y_skip)) + hip_offset
        FR_knee_skip = 2*np.arcsin(FR_height/(2*self.l1))

        BL_hip_skip = 0.5*np.pi - np.arccos(BL_height/(2*self.l1))+np.arctan(x_range_skip/(B_height-y_skip)) + hip_offset
        BL_knee_skip = 2*np.arcsin(BL_height/(2*self.l1))
        
        BR_hip_skip = 0.5*np.pi - np.arccos(BR_height/(2*self.l1))+np.arctan(x_range_skip/(B_height-y_skip)) + hip_offset
        BR_knee_skip = 2*np.arcsin(BR_height/(2*self.l1))

        hFL1 = self.l1*np.cos(0.5*np.pi-FL_hip_skip)
        hFL2 = self.l2*np.sin(FL_knee_skip-FL_hip_skip)
        self.h_skip_FL.append(hFL1+hFL2)
        #return FL_hip_skip,FL_knee_skip,FR_hip_skip,FR_knee_skip,BL_hip_skip,BL_knee_skip,BR_hip_skip,BR_knee_skip
        return np.rad2deg(FL_hip_skip),np.rad2deg(FL_knee_skip),np.rad2deg(FR_hip_skip),np.rad2deg(FR_knee_skip),np.rad2deg(BL_hip_skip),np.rad2deg(BL_knee_skip),np.rad2deg(BR_hip_skip),np.rad2deg(BR_knee_skip)


    # start smooth_start in initial position. Should keep your servos save.
    def start(self):
        FL_hip_step,FL_knee_step,FR_hip_step,FR_knee_step,BL_hip_step,BL_knee_step,BR_hip_step,BR_knee_step=self.callculate_step_8L(X_RANGE_STEP_F_B[0], DROP_F_B)
        FL_hip_skip,FL_knee_skip,FR_hip_skip,FR_knee_skip,BL_hip_skip,BL_knee_skip,BR_hip_skip,BR_knee_skip = self.callculate_skip_8L(X_RANGE_SKIP_F_B[0],MIN_DELTA_F_B,DROP_F_B, R_F_B)

        self.servo_knee_r_f.smooth_start(FR_knee_step)
        self.servo_hip_r_f.smooth_start(FR_hip_step)
        self.servo_knee_l_b.smooth_start(BL_knee_step)
        self.servo_hip_l_b.smooth_start(BL_hip_step)

        self.servo_knee_l_f.smooth_start(FL_knee_skip)
        self.servo_hip_l_f.smooth_start(FL_hip_skip)
        self.servo_knee_r_b.smooth_start(BR_knee_skip)
        self.servo_hip_r_b.smooth_start(BR_hip_skip)


#-----------FSM------------------------------


    def check_state(self):
        try:
            msg = self.conn.recv(4096)
            msg = msg.decode('UTF-8')
            if msg[:7] == "state: ":
                self.state = msg[7:]
                print(self.state)
            else: 
                self.state = msg[7:] #TODO
        except socket.error as e:
            pass


    def fsm_process(self, conn):
        self.conn = conn
        self.state = 'idle'
        print('idle') #TODO del print



        while True:
            self.check_state()
            roll_ang,elev_ang = self.get_pitch_roll()
            if self.state == "forward":
                self.move_forward(X_RANGE_STEP_F_B, X_RANGE_SKIP_F_B,MIN_DELTA_F_B)
                print('idle') #TODO del print
            elif self.state == "backward":
                self.move_backward(X_RANGE_STEP_F_B, X_RANGE_SKIP_F_B,MIN_DELTA_F_B)
                print('idle') #TODO del print
            elif self.state == "left":
                self.rotate_left(X_RANGE_STEP_L_R, X_RANGE_SKIP_L_R,MIN_DELTA_L_R)
                print('idle') #TODO del print
            elif self.state == "right":
                self.rotate_right(X_RANGE_STEP_L_R, X_RANGE_SKIP_L_R,MIN_DELTA_L_R)
                print('idle') #TODO del print


#-----------forward/backward------------------------------


    def move_step_skip(self,x_range_step,x_range_skip,min_delta):
        FL_hip_step,FL_knee_step,FR_hip_step,FR_knee_step,BL_hip_step,BL_knee_step,BR_hip_step,BR_knee_step=self.callculate_step_8L(x_range_step, DROP_F_B)
        FL_hip_skip,FL_knee_skip,FR_hip_skip,FR_knee_skip,BL_hip_skip,BL_knee_skip,BR_hip_skip,BR_knee_skip = self.callculate_skip_8L(x_range_skip,min_delta,DROP_F_B, R_F_B)

        self.hip_fulFL.append(FL_hip_skip)
        self.knee_fulFL.append(FL_knee_skip)
        self.hip_fulFR.append(FR_hip_step)
        self.knee_fulFR.append(FR_knee_step)
        self.hip_fulBL.append(BL_hip_step)
        self.knee_fulBL.append(BL_knee_step)
        self.hip_fulBR.append(BR_hip_skip)
        self.knee_fulBR.append(BR_knee_skip)

        self.servo_knee_r_f.set_angle(FR_knee_step)
        self.servo_hip_r_f.set_angle(FR_hip_step)
        self.servo_knee_l_b.set_angle(BL_knee_step)
        self.servo_hip_l_b.set_angle(BL_hip_step)

        self.servo_knee_l_f.set_angle(FL_knee_skip)
        self.servo_hip_l_f.set_angle(FL_hip_skip)
        self.servo_knee_r_b.set_angle(BR_knee_skip)
        self.servo_hip_r_b.set_angle(BR_hip_skip)


    def move_skip_step(self,x_range_step,x_range_skip,min_delta):
        FL_hip_step,FL_knee_step,FR_hip_step,FR_knee_step,BL_hip_step,BL_knee_step,BR_hip_step,BR_knee_step=self.callculate_step_8L(x_range_step, DROP_F_B)
        FL_hip_skip,FL_knee_skip,FR_hip_skip,FR_knee_skip,BL_hip_skip,BL_knee_skip,BR_hip_skip,BR_knee_skip= self.callculate_skip_8L(x_range_skip,min_delta, DROP_F_B, R_F_B)

        self.hip_fulFL.append(FL_hip_step)
        self.knee_fulFL.append(FL_knee_step)
        self.hip_fulFR.append(FR_hip_skip)
        self.knee_fulFR.append(FR_knee_skip)
        self.hip_fulBL.append(BL_hip_skip)
        self.knee_fulBL.append(BL_knee_skip)
        self.hip_fulBR.append(BR_hip_step)
        self.knee_fulBR.append(BR_knee_step)

        self.servo_knee_r_f.set_angle(FR_knee_skip)
        self.servo_hip_r_f.set_angle(FR_hip_skip)
        self.servo_knee_l_b.set_angle(BL_knee_skip)
        self.servo_hip_l_b.set_angle(BL_hip_skip)

        self.servo_knee_l_f.set_angle(FL_knee_step)
        self.servo_hip_l_f.set_angle(FL_hip_step)
        self.servo_knee_r_b.set_angle(BR_knee_step)
        self.servo_hip_r_b.set_angle(BR_hip_step)


    def move_forward(self,x_range_step,x_range_skip,min_delta):
        print('enter forward') #TODO del print
        steps = 0
        while self.state == 'forward' and steps<4:
            for i in range(len(x_range_step)):
                self.move_step_skip(x_range_step[i],x_range_skip[i],min_delta)
                self.check_state()
            for i in range(len(x_range_skip)):    
                self.move_skip_step(x_range_step[i],x_range_skip[i],min_delta)
                self.check_state()
            steps+=1
        self.state = 'idle'
        #saveList(self.hip_fulFL,"hip_fulFL")
        #saveList(self.knee_fulFL,"knee_fulFL")
        saveList(self.h_step_FL,"h_step_FL")
        saveList(self.h_skip_FL,"h_skip_FL")
        print('exit forward') #TODO del print


    def move_backward(self,x_range_step,x_range_skip,min_delta):
        print('enter backward') #TODO del print
        steps = 0
        while self.state == 'backward':
            for i in range(len(x_range_step) - 1,-1,-1):
                self.move_step_skip(x_range_step[i],x_range_skip[i],min_delta)
                self.check_state()
            for i in range(len(x_range_skip)-1,-1,-1):
                self.move_skip_step(x_range_step[i],x_range_skip[i],min_delta)
                self.check_state()
            steps+=1
        print('exit backward') #TODO del print


# ------------------------------------------rotate----------------------------------------------------- 


    def move_step_left(self,x_range_step,x_range_skip,min_delta):
        hip_step,knee_step=self.callculate_step(x_range_step)

        self.servo_knee_l_f.set_angle(knee_step)
        self.servo_hip_l_f.set_angle(hip_step)
        self.servo_knee_l_b.set_angle(knee_step)
        self.servo_hip_l_b.set_angle(hip_step)


    def move_skip_left(self,x_range_step,x_range_skip,min_delta):
        hip_skip,knee_skip = self.callculate_skip(x_range_skip,min_delta)

        self.servo_knee_l_f.set_angle(knee_skip)
        self.servo_hip_l_f.set_angle(hip_skip)
        self.servo_knee_l_b.set_angle(knee_skip)
        self.servo_hip_l_b.set_angle(hip_skip)


    def move_step_right(self,x_range_step,x_range_skip,min_delta):
        hip_step,knee_step=self.callculate_step(x_range_step)

        self.servo_knee_r_f.set_angle(knee_step)
        self.servo_hip_r_f.set_angle(hip_step)
        self.servo_knee_r_b.set_angle(knee_step)
        self.servo_hip_r_b.set_angle(hip_step)


    def move_skip_right(self,x_range_step,x_range_skip,min_delta):
        hip_skip,knee_skip = self.callculate_skip(x_range_skip,min_delta)

        self.servo_knee_r_f.set_angle(knee_skip)
        self.servo_hip_r_f.set_angle(hip_skip)
        self.servo_knee_r_b.set_angle(knee_skip)
        self.servo_hip_r_b.set_angle(hip_skip)


    def rotate_right(self,x_range_step,x_range_skip,min_delta,count_steps=0):
        print('enter rotate (right)') #TODO del print
        while self.state == 'right':    
            roll_ang,elev_ang = self.get_pitch_roll()
            self.check_state()

            # for i in range(len(x_range_step)):
            #     self.move_step_left(x_range_step[i],x_range_skip[i],min_delta)
            #     self.move_skip_right(x_range_step[i],x_range_skip[i],min_delta)
            #     self.check_state()
            # for i in range(len(x_range_skip)-1,-1,-1):    
            #     self.move_skip_left(x_range_step[i],x_range_skip[i],min_delta)
            #     self.check_state()
        print('exit rotate (right)') #TODO del print


    def rotate_left(self,x_range_step,x_range_skip,min_delta,count_steps=0):
        print('enter rotate (left)') #TODO del print
        while self.state == 'left':    
            roll_ang,elev_ang = self.get_pitch_roll()
            self.check_state()

            # for i in range(len(x_range_step)):
            #     self.move_step_right(x_range_step[i],x_range_skip[i],min_delta)
            #     self.move_skip_left(x_range_step[i],x_range_skip[i],min_delta)
            #     self.check_state()
            # for i in range(len(x_range_skip)-1,-1,-1):    
            #     self.move_skip_right(x_range_step[i],x_range_skip[i],min_delta)
            #     self.check_state()
        print('enter rotate (left)') #TODO del print


#-----------gyro------------------------------


    def get_pitch_roll(self):
         # Get INT_STATUS byte
        while True:

            mpuIntStatus = self.mpu.getIntStatus()
        
            if mpuIntStatus >= 2: # check for DMP data ready interrupt (this should happen frequently) 
                # get current FIFO count
                fifoCount = self.mpu.getFIFOCount()
                
                # check for overflow (this should never happen unless our code is too inefficient)
                if fifoCount == 1024:
                    # reset so we can continue cleanly
                    self.mpu.resetFIFO()
                    print('FIFO overflow!')
                    return self.old_roll, self.old_pitch
                    
                # wait for correct available data length, should be a VERY short wait
                fifoCount = self.mpu.getFIFOCount()
                while fifoCount < self.packetSize:
                    fifoCount = self.mpu.getFIFOCount()
                
                result = self.mpu.getFIFOBytes(self.packetSize)
                q = self.mpu.dmpGetQuaternion(result)
                g = self.mpu.dmpGetGravity(q)
                ypr = self.mpu.dmpGetYawPitchRoll(q, g)
                #fifoCount -= self.packetSize
                self.pitch_estimate, self.pitch_err = kalman(ypr['roll'], self.pitch_estimate, self.pitch_err)
                self.roll_estimate, self.roll_err = kalman(ypr['pitch'], self.roll_estimate, self.roll_err)
                # print(f"pitch= {ypr['pitch'] * 180 / math.pi}")
                # print(f"roll= {ypr['roll'] * 180 / math.pi}")
                return self.roll_estimate,self.pitch_estimate