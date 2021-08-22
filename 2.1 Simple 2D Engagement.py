import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

#Setup
Vm, Vt, XNt, HEDEG, XNP, Tau = 1500, 1000, 96.6, -0, 4, 1
Rm1, Rm2, Rt1, Rt2 = 0, 8500,10000,10000
XNclim = 966
Beta = 1 * np.pi
Vt1 = Vt* np.cos(np.pi - Beta); Vt2 = Vt * np.sin(Beta)
HE = HEDEG / 57.3
T = 0; S = 0
Rtm1 = Rt1 - Rm1; Rtm2 = Rt2 - Rm2
Rtm = np.sqrt(Rtm1**2 + Rtm2**2)
Lambda = np.arctan2(Rtm2, Rtm1)
Lead = np.arcsin(Vt/Vm * np.sin(Beta + Lambda))
Theta = Lambda + Lead
Vm1 = Vm * np.cos(Theta + HE); Vm2 = Vm * np.sin(Theta + HE)
Vtm1 = Vt1 - Vm1; Vtm2 = Vt2 - Vm2
Vc = -(Rtm1*Vtm1 + Rtm2*Vtm2)/Rtm

#additional maneuver
def XNt(T,G,P):
    return 32.2*G*(np.cos(np.pi/P * T)**1)
    #if (T//(2*P)) > (P/2): return G*32.2
    #else: return -G*32.2
#Data
Time = []; Velocity = []
Rt1K = []; Rt2K = []
Rm1K = []; Rm2K = []
RtmK = []; VcK = []
XNcData = []

#Loop
    #Block 10
while Vc > 0:
    if Rtm < 1000:
        H = 0.0002
    else:
        H = 0.01
    BetaOLD = Beta
    Rt1OLD  = Rt1
    Rt2OLD  = Rt2
    Rm1OLD  = Rm1
    Rm2OLD  = Rm2
    Vm1OLD  = Vm1
    Vm2OLD  = Vm2

    #Block 200
    Rtm1 = Rt1 - Rm1
    Rtm2 = Rt2 - Rm2
    Rtm = np.sqrt(Rtm1**2 + Rtm2**2)
        #Over/Under shoot
    if Rtm2 >= 0:
        RtmP = Rtm
    else:
        RtmP = -Rtm
    Vtm1 = Vt1 - Vm1
    Vtm2 = Vt2 - Vm2
    Vc = -(Rtm1*Vtm1 + Rtm2*Vtm2)/Rtm
    Lambda = np.arctan2(Rtm2, Rtm1)
    LambdaD= (Rtm1*Vtm2 - Rtm2*Vtm1)/(Rtm**2)
        #Prop-Nav
    XNc = XNP * Vc * LambdaD
    if XNc >  XNclim: XNc =  XNclim
    if XNc < -XNclim: XNc = -XNclim
    Am1 = -XNc * np.sin(Lambda)
    Am2 =  XNc * np.cos(Lambda)
        #Target Maneuver
    Vt1 = Vt* np.cos(np.pi - Beta)
    Vt2 = Vt * np.sin(Beta)
    BetaD = XNt(T,8,2) / Vt
    #BetaD = XNt / Vt

    #Block 66
        #Updating differentials
    Beta+= H * BetaD
    Rt1 += H * Vt1
    Rt2 += H * Vt2
    Rm1 += H * Vm1
    Rm2 += H * Vm2
    Vm1 += H * Am1
    Vm2 += H * Am2
    T += H

    #Block 200
    Rtm1 = Rt1 - Rm1
    Rtm2 = Rt2 - Rm2
    Rtm = np.sqrt(Rtm1**2 + Rtm2**2)
        #Over/Under shoot
    if Rtm2 >= 0:
        RtmP = Rtm
    else:
        RtmP = -Rtm
    Vtm1 = Vt1 - Vm1
    Vtm2 = Vt2 - Vm2
    Vc = -(Rtm1*Vtm1 + Rtm2*Vtm2)/Rtm
    Lambda = np.arctan2(Rtm2, Rtm1)
    LambdaD= (Rtm1*Vtm2 - Rtm2*Vtm1)/(Rtm**2)
        #Prop-Nav
    XNc = XNP * Vc * LambdaD
    if XNc >  XNclim: XNc =  XNclim
    if XNc < -XNclim: XNc = -XNclim
    Am1 = -XNc * np.sin(Lambda)
    Am2 =  XNc * np.cos(Lambda)
        #Target Maneuver
    Vt1 = Vt* np.cos(np.pi - Beta)
    Vt2 = Vt * np.sin(Beta)
    BetaD = XNt(T,8,2) / Vt
    #BetaD = XNt / Vt

    #Block 55
        #Runge kutta
    Beta= .5 * (BetaOLD+ Beta+ H*BetaD)
    Rt1 = .5 * (Rt1OLD + Rt1 + H*Vt1)
    Rt2 = .5 * (Rt2OLD + Rt2 + H*Vt2)
    Rm1 = .5 * (Rm1OLD + Rm1 + H*Vm1)
    Rm2 = .5 * (Rm2OLD + Rm2 + H*Vm2)
    Vm1 = .5 * (Vm1OLD + Vm1 + H*Am1)
    Vm2 = .5 * (Vm2OLD + Vm2 + H*Am2)
        #recording
    S += H
    if S < .01999:
        continue
    S = 0
    Time.append(T)
    Velocity.append(np.sqrt(Vm1**2 + Vm2**2))
    Rt1K.append(Rt1/1000); Rt2K.append(Rt2/1000)
    Rm1K.append(Rm1/1000); Rm2K.append(Rm2/1000)
    XNcData.append(XNc/32.2)
    RtmK.append(Rtm/1000); VcK.append(Vc/1000)

#Time.append(T)
#Velocity.append(np.sqrt(Vm1**2 + Vm2**2))
Rt1K.append(Rt1/1000); Rt2K.append(Rt2/1000)
Rm1K.append(Rm1/1000); Rm2K.append(Rm2/1000)
Time.append(T)
XNcData.append(XNc/32.2)
#XNcData.append(XNc/32.2)
Miss_Distance = RtmP
print(Miss_Distance)
tF = Time[-1]
'''
plt.plot(Rm1K,Rm2K,'b-', label='Missile')
plt.plot(Rt1K,Rt2K,color='orange',linestyle='dotted', label='Target')
plt.xlabel('DownRange (Kft)')
plt.ylabel('Crossrange (Kft)')
plt.title('2D Pure Prop-Nav Engagement')
plt.gca().set_aspect('equal', adjustable='box')
plt.tight_layout()
plt.show()
'''
'''
plt.plot(Time,XNcData)
plt.show()
'''
fig, (ax1, ax2)= plt.subplots(2)
ax1.scatter(Rt1K,Rt2K, c=cm.rainbow(np.array(Time[::-1])/tF),marker='.')
ax1.scatter(Rm1K,Rm2K, c=cm.rainbow(np.array(Time[::-1])/tF),marker='o', s=(72./fig.dpi)**2)
ax1.set(xlabel=('DownRange (Kft)'),ylabel=('Crossrange (Kft)'))
ax1.set_aspect('equal', adjustable='box')

ax2.plot(Time,XNcData,'k-')
ax2.set(xlabel=('Time (S)'),ylabel=('''Acceleration (G's)'''))

fig.tight_layout()
fig.suptitle('''Pure Prop-Nav Simulation''')
plt.show()

