import time
# Servo with PCA9685 implementation

# Configure min and max servo pulse lengths

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min + 1) / (in_max - in_min + 1) + out_min

class ServoPCA9685(object):
    def __init__(self, pca9685, channel,servo_min=103,servo_max=512):
        self.pca9685 = pca9685
        self.channel = channel
        self.servo_min = servo_min
        self.servo_max = servo_max
        self.set_pwm_freq(50)
        self.set_pulse(300)

    def set_pwm_freq(self, freq=50):
        self.pca9685.set_pwm_freq(freq)
        time.sleep(0.005)

    def set_angle(self, angle):
        self.set_pulse(map(angle, 0, 180, self.servo_min, self.servo_max))

    def set_pulse(self, pulse):
        if pulse >= self.servo_min and pulse <= self.servo_max:
            self.pca9685.set_pwm(self.channel, 0, int(pulse)) # not working if pulse not int
            time.sleep(0.005)

    #own_coef get by: own_coef = (y2-y1)/(x2-x1); Y->{servo_min,servo_max},X->{0,180}
    def smooth_start(self,angle,own_coef):
        duty_cycle = self.servo_min + (angle/own_coef)
        for i in range(100):
            self.set_pulse(i/100 * duty_cycle)
            time.sleep(0.02)
        self.set_pulse(duty_cycle)
        time.sleep(0.5)

    def disable(self):
        self.pca9685.set_pwm(self.channel, 0, 0)
        time.sleep(0.005)
