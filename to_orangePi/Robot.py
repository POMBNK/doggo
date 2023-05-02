
    #COMMENT THIS IN REAL ORANGE PI ENV 
import sys
import fake_rpi
import json

sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi
sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake GPIO
sys.modules['smbus'] = fake_rpi.smbus # Fake smbus (I2C)

    #COMMENT THIS IN REAL ORANGE PI ENV 

# Robot Class with PCA9685 integration
# mpu6050 soon

import numpy as np
import smbus
import PCA9685
import ServoPCA9685

"""
@TODO:
    1) Scan from mpu pitch and roll and give it to calculate func in step_skip(), than skip_step()
    2) Implement smooth_start with pca9685 servo lib
"""

class Robot(object):
    def __init__(self,r,drop):
        self.i2cBus = smbus.SMBus(0)
        self.pca9685 = PCA9685.PCA9685(self.i2cBus)
        #self.mpu = mpu6050.mpu6050(self.i2cBus)
        self.r = r
        self.drop = drop
        self.l1=100
        self.l2=100
        #servos init once
        srv_data = json.load('servo_pwm_dgr.json')
        self.servo_knee_r_f = ServoPCA9685.ServoPCA9685(self.pca9685, PCA9685.CHANNEL10, srv_data['krf']['pwm'], srv_data['krf']['dgr'])
        self.servo_hip_r_f = ServoPCA9685.ServoPCA9685 (self.pca9685, PCA9685.CHANNEL11, srv_data['hrf']['pwm'], srv_data['hrf']['dgr'])
        self.servo_knee_l_b = ServoPCA9685.ServoPCA9685 (self.pca9685, PCA9685.CHANNEL06, srv_data['klb']['pwm'], srv_data['klb']['dgr'])
        self.servo_hip_l_b = ServoPCA9685.ServoPCA9685 (self.pca9685, PCA9685.CHANNEL07, srv_data['hlb']['pwm'], srv_data['hlb']['dgr'])
        self.servo_knee_l_f = ServoPCA9685.ServoPCA9685 (self.pca9685, PCA9685.CHANNEL14, srv_data['klf']['pwm'], srv_data['klf']['dgr'])
        self.servo_hip_l_f = ServoPCA9685.ServoPCA9685 (self.pca9685, PCA9685.CHANNEL15, srv_data['hlf']['pwm'], srv_data['hlf']['dgr'])
        self.servo_knee_r_b = ServoPCA9685.ServoPCA9685 (self.pca9685, PCA9685.CHANNEL02, srv_data['krb']['pwm'], srv_data['krb']['dgr'])
        self.servo_hip_r_b = ServoPCA9685.ServoPCA9685 (self.pca9685, PCA9685.CHANNEL03, srv_data['hrb']['pwm'], srv_data['hrb']['dgr'])

    # callculate_step return a servos angle to hip and knee from IK step pos
    def callculate_step(self,x_range_step):
        elev = np.random.uniform(low=0, high=2, size=1,) # NOISE TEST
        roll = np.random.uniform(low=0, high=2, size=1,) # NOISE TEST
        # elev = 0
        # roll = 0
        
        y_step=0
        height = self.drop + elev
        hip_offset = np.arcsin(elev / 105) #MagicNumber is 0.5*length longerone
        height_slew = np.sqrt(x_range_step**2+(height-y_step)**2)+roll
        hip_step = 0.5*np.pi - np.arccos(height_slew/(2*self.l1))+np.arctan(x_range_step/(height-y_step)) + hip_offset
        knee_step = 2*np.arcsin(height_slew/(2*self.l1))

        return np.rad2deg(hip_step), np.rad2deg(knee_step)
    

    # callculate_skip return a servos angle to hip and knee from IK skip pos
    def callculate_skip(self,x_range_skip,min_delta):
        elev = np.random.uniform(low=0, high=2, size=1,) # NOISE TEST
        roll = np.random.uniform(low=0, high=2, size=1,) # NOISE TEST
        # elev = 0
        # roll = 0

        delta = np.sqrt(self.r**2-min_delta**2) ## ERROR MAGIC -70
        y_skip = np.sqrt((self.r**2) - (x_range_skip**2)) - delta
        height = self.drop + elev
        hip_offset = np.arcsin(elev / 105)
        height_slew = np.sqrt(x_range_skip**2+(height-y_skip)**2)+roll
        hip_skip = 0.5*np.pi - np.arccos(height_slew/(2*self.l1))+np.arctan(x_range_skip/(height-y_skip)) + hip_offset
        knee_skip = 2*np.arcsin(height_slew/(2*self.l1))

        return np.rad2deg(hip_skip),np.rad2deg(knee_skip)
    
    # start smooth_start in initial position. Should keep your servos save.
    def start(self,x_range_step,x_range_skip):
        hip_step,knee_step=self.callculate_step(x_range_step[0])
        hip_skip,knee_skip = self.callculate_skip(x_range_skip[0],min_delta=x_range_skip[0])

        #@TODO:(2)
        #change set angle to smooth start. Calc koef before
        self.servo_knee_r_f.set_angle(knee_step)
        self.servo_hip_r_f.set_angle(hip_step)
        self.servo_knee_l_b.set_angle(knee_step)
        self.servo_hip_l_b.set_angle(hip_step)

        self.servo_knee_l_f.set_angle(knee_skip)
        self.servo_hip_l_f.set_angle(hip_skip)
        self.servo_knee_r_b.set_angle(knee_skip)
        self.servo_hip_r_b.set_angle(hip_skip)

    # rf_knee->rf_hip->lb_knee->lb_hip
    # map angles to pwm and controll servos initialy to step_skip movement
    def move_step_skip(self,x_range_step,x_range_skip,min_delta):
        #@TODO:(1)
        #elev,roll = self.get_elev_roll()
        hip_step,knee_step=self.callculate_step(x_range_step)
        hip_skip,knee_skip = self.callculate_skip(x_range_skip,min_delta)

        self.servo_knee_r_f.set_angle(knee_step)
        self.servo_hip_r_f.set_angle(hip_step)
        self.servo_knee_l_b.set_angle(knee_step)
        self.servo_hip_l_b.set_angle(hip_step)

        self.servo_knee_l_f.set_angle(knee_skip)
        self.servo_hip_l_f.set_angle(hip_skip)
        self.servo_knee_r_b.set_angle(knee_skip)
        self.servo_hip_r_b.set_angle(hip_skip)

    #lf_knee->lf_hip->rb_knee->rb_hip
    # map angles to pwm and controll servos initialy to skip_step movement
    def move_skip_step(self,x_range_step,x_range_skip,min_delta):
        hip_step,knee_step=self.callculate_step(x_range_step)
        hip_skip,knee_skip = self.callculate_skip(x_range_skip,min_delta)

        self.servo_knee_r_f.set_angle(knee_skip)
        self.servo_hip_r_f.set_angle(hip_skip)
        self.servo_knee_l_b.set_angle(knee_skip)
        self.servo_hip_l_b.set_angle(hip_skip)

        self.servo_knee_l_f.set_angle(knee_step)
        self.servo_hip_l_f.set_angle(hip_step)
        self.servo_knee_r_b.set_angle(knee_step)
        self.servo_hip_r_b.set_angle(hip_step)

    def get_elev_roll(self):
        #self.mpu6050.read()
        pass
