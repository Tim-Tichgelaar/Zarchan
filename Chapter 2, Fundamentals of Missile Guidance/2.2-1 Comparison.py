import numpy as np
import matplotlib.pyplot as plt

def Engagement(Missile_Velocity, Target_Velocity, Target_Maneuver, Heading_Error, N_Prime, Missile_Location, Target_Location, Overload, Target_Angle):
    #Setup
    Vm, Vt, XNt, HEDEG, XNP = Missile_Velocity, Target_Velocity, Target_Maneuver * 32.2, Heading_Error, N_Prime
    Rm1, Rm2, Rt1, Rt2 = Missile_Location[0], Missile_Location[1], Target_Location[0], Target_Location[1]
    XNclim = Overload * 32.2
    Beta = Target_Angle/57.3
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
    #def XNt(T,G,P):
    #return 32.2*G*(np.cos(np.pi/P * T)**3)
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
        BetaD = XNt/Vt

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
        BetaD = XNt/Vt

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
        if S < .09999:
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
    #XNcData.append(XNc/32.2)
    Nonlinear_Miss_Distance = RtmP
    Final_Time = Time[-1]
    return [Nonlinear_Miss_Distance, Final_Time, Time, XNcData]

def  Linearized(Missile_Velocity, Target_Velocity, Target_Maneuver, Heading_Error, N_Prime, Missile_Location, Target_Location, Target_Angle, Overload, Final_Time):
    #Setup
    XNt, Y, Vm, HEDEG, TF, XNP = Target_Maneuver * 32.2, Target_Location[1]-Missile_Location[1], Missile_Velocity, Heading_Error, Final_Time, N_Prime
    if Target_Angle < 90: Vc = Missile_Velocity + Target_Velocity
    elif Target_Angle < 270:
        if Target_Angle >= 90: Vc = Missile_Velocity - Target_Velocity
    else: Vc = Missile_Velocity + Target_Velocity
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
        if XNc > (Overload*32.2): XNc = (Overload*32)
        if XNc < -(Overload*32.2): XNc = -(Overload*32)
        YDD = XNt - XNc
        #Block 66
        Y = Y + H*YD
        YD = YD + H*YDD
        T = T + H
        #Block 200
        Tgo = TF - T + .00001
        LambdaD = (Y + YD * Tgo)/(Vc*Tgo**2)
        XNc = XNP * Vc * LambdaD
        if XNc > (Overload*32.2): XNc = (Overload*32)
        if XNc < -(Overload*32.2): XNc = -(Overload*32)
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
    Linearized_Miss_Distance = Y
    return [Linearized_Miss_Distance, Time, XNcdata]

def Compare(Missile_Velocity, Target_Velocity, Target_Maneuver, Heading_Error, N_Prime, Missile_Location, Target_Location, Overload, Target_Angle):
    Nonlinear_Data = Engagement(Missile_Velocity, Target_Velocity, Target_Maneuver, Heading_Error, N_Prime, Missile_Location, Target_Location, Overload, Target_Angle)
    Final_Time = Nonlinear_Data[1]
    Linear_Data = Linearized(Missile_Velocity, Target_Velocity, Target_Maneuver, Heading_Error, N_Prime, Missile_Location, Target_Location, Target_Angle, Overload, Final_Time)

    print('Nonlinear Miss = ', Nonlinear_Data[0])
    print('Linear Miss = ', Linear_Data[0])

    plt.plot(Nonlinear_Data[2],Nonlinear_Data[3],'k:',label='Nonlinear')
    plt.plot(Linear_Data[1],Linear_Data[2],'k-',label='Linearized')
    plt.ylim(0,11)
    plt.xlim(0,11)
    plt.xlabel('Time (S)')
    plt.ylabel('''Acceleration (G's)''')
    plt.title('Linear vs Nonlinear acceleration')
    plt.grid('both')
    plt.legend()
    plt.show()

Compare(3000,1000,0,-20,4,(0,10000),(40000,10000),30,0)


