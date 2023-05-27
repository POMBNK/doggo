import time
# Servo with PCA9685 implementation

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min + 1) / (in_max - in_min + 1) + out_min

def map_k(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class ServoPCA9685(object):
    def __init__(self, pca9685, channel, servo_pwm = [103,512], servo_dgr = [0,180]):
        self.pca9685 = pca9685
        self.channel = channel
        self.servo_min_pwm = servo_pwm[0]
        self.servo_max_pwm = servo_pwm[1]
        self.servo_min_dgr = servo_dgr[0]
        self.servo_max_dgr = servo_dgr[1]
        self.set_pwm_freq(50)
        self.set_pulse(300)

    def set_pwm_freq(self, freq=50):
        self.pca9685.set_pwm_freq(freq)
        time.sleep(0.005)

    def set_angle(self, angle):
        self.set_pulse(map(angle, self.servo_min_dgr, self.servo_max_dgr, self.servo_min_pwm, self.servo_max_pwm))

    def set_pulse(self, pulse):
        if pulse >= 103 and pulse <= 512:
            self.pca9685.set_pwm(self.channel, 0, int(pulse)) # not working if pulse not int
            time.sleep(0.005)

    #own_coef get by: own_coef = (y2-y1)/(x2-x1); Y->{servo_min,servo_max},X->{0,180}
    # def smooth_start(self,angle,own_coef):
    #     duty_cycle = 103 + (angle/own_coef)
    #     for i in range(100):
    #         self.set_pulse(i/100 * duty_cycle)
    #         time.sleep(0.05)
    #     self.set_pulse(duty_cycle)
    #     time.sleep(0.5)

    def smooth_start(self,angle):

        for i in range(angle//100,angle):
            self.set_angle(i)
            time.sleep(0.05)
        self.set_angle(angle)
        time.sleep(0.5)

    def disable(self):
        self.pca9685.set_pwm(self.channel, 0, 0)
        time.sleep(0.005)