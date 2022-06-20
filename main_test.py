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
    
def draw_attitude(ahrs,**kw):
    fig, axs = plt.subplots(3,1,sharex=True)
    axs[0].set(ylabel='roll (deg)',title='Attitude')
    axs[1].set(ylabel='pitch (deg)')
    axs[2].set(ylabel='yaw (deg)')
  
    label_text = kw.get('label_text','None')
    for i in range((ahrs.shape[1]-1)//3):
        if label_text == "None":
            axs[0].plot(ahrs[:,0], ahrs[:,1+i*3]/np.pi*180, label=f"roll_{i}")
            axs[1].plot(ahrs[:,0], ahrs[:,2+i*3]/np.pi*180, label=f"pitch_{i}")
            axs[2].plot(ahrs[:,0], ahrs[:,3+i*3]/np.pi*180, label=f"yaw_{i}")
        else:
            axs[0].plot(ahrs[:,0], ahrs[:,1+i*3]/np.pi*180, label = f"roll_{label_text[i]}")
            axs[1].plot(ahrs[:,0], ahrs[:,2+i*3]/np.pi*180, label=f"pitch_{label_text[i]}")
            axs[2].plot(ahrs[:,0], ahrs[:,3+i*3]/np.pi*180, label=f"yaw_{label_text[i]}")
          
    for i in range(3):
        axs[i].grid()
        axs[i].legend()
    
    plt.show()

#draw_raw_data(imu)

# cut data
time_start = 2 #72.5
time_end = 253.5
imu2 = imu[(imu[:,1]>time_start) & (imu[:,1]<time_end),:]
print('Remove samples:', imu.shape[0]-imu2.shape[0])
#draw_raw_data(imu2)
#plt.plot(imu[:,1])

#attitude_marg = ahrs.filters.Madgwick(acc=imu2[:,2:5], gyr=imu2[:,5:8],mag=imu2[:,8:11],frequency=62)
#attitude = ahrs.filters.Madgwick(acc=imu2[:,2:5], gyr=imu2[:,5:8],q0 = attitude_magwick_marg.Q[0],frequency=62)

attitude_marg = ahrs.filters.aqua.AQUA(acc=imu2[:,2:5], gyr=imu2[:,5:8], mag=imu2[:,8:11],frequency=62,adaptive = True)
attitude = ahrs.filters.aqua.AQUA(acc=imu2[:,2:5], gyr=imu2[:,5:8],q0 = attitude_aqua_marg.Q[0],frequency=62)

euler_angles_aqua = np.asarray([ahrs.common.orientation.q2euler(s) for s in attitude.Q]) #this formula is different to wiki
rpy_angles_aqua = np.asarray([ahrs.common.orientation.q2rpy(s) for s in attitud.Q])

euler_angles_marg_aqua = np.asarray([ahrs.common.orientation.q2euler(s) for s in attitude_marg.Q]) #this formula is different to wiki
rpy_angles_marg_aqua = np.asarray([ahrs.common.orientation.q2rpy(s) for s in attitude_marg.Q])

orientations = np.hstack((imu2[:,1].reshape(-1,1),euler_angles_aqua,euler_angles_marg_aqua))
orientations2 = np.hstack((imu2[:,1].reshape(-1,1),rpy_angles_aqua, rpy_angles_marg_aqua))

#draw_attitude(orientations, label_text = ['imu','marg'])
draw_attitude(orientations2)