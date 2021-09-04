import numpy as np
import matplotlib.pyplot as plt

#Setup
Vc, XNt, Y, Vm, HEDEG, TF, XNP = 4000, 0, 0, 3000, -20, 10, 4
#Closing Velocity, Target Maneuver, Vertical Separation, Heading angle (Degrees), Flight Time, Maneuvering constant
YD = -Vm*HEDEG/57.3
T=0;S=0
H=.01

#Data
Time, Ydata, YDdata, XNcdata = [],[],[],[]


#Loop
while T < TF-.0001:
    #Block 10
    YOLD = Y
    YDOLD = YD
    #Block 200
    Tgo = TF - T + .00001
    LambdaD = (Y + YD * Tgo)/(Vc*Tgo**2)
    XNc = XNP * Vc * LambdaD
    YDD = XNt - XNc
    #Block 66
    Y = Y + H*YD
    YD = YD + H*YDD
    T = T + H
    #Block 200
    Tgo = TF - T + .00001
    LambdaD = (Y + YD * Tgo)/(Vc*Tgo**2)
    XNc = XNP * Vc * LambdaD
    YDD = XNt - XNc
    #Block 55
    Y = .5 * (YOLD+Y+H*YD)
    YD= .5 * (YDOLD+YD+H*YDD)
    S = S + H
    if S < .09999:
        continue
    S=0
    Time.append(T)
    Ydata.append(Y)
    YDdata.append(YD)
    XNcdata.append(XNc/32.2)
print(Y)
plt.plot(Time,XNcdata, 'k-', label='Linearized Model')
plt.title('Linearized 2D Engagement Model')
plt.xlabel('Time (S)')
plt.ylabel('Acceleration (G)')
plt.xlim(0,11)
plt.ylim(0,11)
#plt.xticks(np.arange(0,11,.5),minor=True)
plt.xticks(np.linspace(0,10,6))
#plt.yticks(np.arange(0,11,.5),minor=True)
plt.yticks(np.linspace(0,10,6))
plt.grid('both')
plt.show()
