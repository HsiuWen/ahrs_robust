import numpy as np
import glob
import os
import ahrs
import matplotlib.pyplot as plt
# Please pay attention to your path naming system
print(os.getcwd())
file_root = '../../data/20220414_NCKU_GYM/Data'
files_sequence = os.listdir(file_root)
#P1211: right wrist, 4 imu array
#P1213: left wrist,  1 imu array
#P1214: left wrist, 4 imu array
print(files_sequence)

seq = files_path = glob.glob(os.path.join(file_root,files_sequence[0],'*.txt'))
imu = np.genfromtxt(seq[0], skip_header=3)

def draw_raw_data(imu):
    fig, axs = plt.subplots(3, 1, sharex=True)
    axs[0].set(ylabel='accel (m/s/s)', title='MIMU reading')
    axs[1].set(ylabel='gyro (rad/s)')
    axs[2].set(xlabel='$t$ (s)', ylabel='mag (microtesla)')

    for i in range(3):
        axs[i].plot(imu[:,1], imu[:,2+i*3], label='x')
        axs[i].plot(imu[:,1], imu[:,3+i*3], label='y')
        axs[i].plot(imu[:,1], imu[:,4+i*3], label='z')
        axs[i].grid()
        axs[i].legend()

    plt.show()
    
def draw_attitude(ahrs):
    fig, axs = plt.subplot(3,1,sharex=True)
    axs[0].plot(ahrs[:,0], ahrs[:,1],ylabel='roll (deg)',title='Attitude')
    axs[1].plot(ahrs[:,0], ahrs[:,2],ylabel='pitch (deg)')
    axs[2].plot(ahrs[:,0], ahrs[:,3],ylabel='yaw (deg)')
    for i in range(3):
        axs[i].grid()
    plt.show()

#draw_raw_data(imu)

# cut data
time_start = 72.5
time_end = 253.5
imu2 = imu[(imu[:,1]>time_start) & (imu[:,1]<time_end),:]
print('Remove samples:', imu.shape[0]-imu2.shape[0])
#draw_raw_data(imu2)
plt.plot(imu[:,1])
attitude = ahrs.filters.Madgwick(frequency=62,acc=imu2[:,2:5], gyr=imu2[:,5:8])
