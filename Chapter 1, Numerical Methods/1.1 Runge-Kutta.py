#This is a series of functions based on the first listing in the book, exploring
#Runge-Kutta integration techniques and comparing them to a euler integration
import numpy as np
import matplotlib.pyplot as plt
#y'' = wx - w**2y
#y=1/w(1-cos(wt))
'''
def RungeKutta(W,T,Tf,Sc,Y,YD,X,H):
    t = []
    YRK = []
    YT = []
    E = []
    S=0
    while T < Tf:
        S+=H
        Yold=Y
        YDold=YD
        YDD = W*X - W*W*Y
        Y  += H * YD
        YD += H * YDD
        T  += H
        YDD = W*X - W*W*Y
        YD = .5 * (YDold + YD + H*YDD)
        Y  = .5 * (Yold + Y + H* YD)
        if S >= Sc:
            continue
        S = 0
        YTHEORY = (1 - np.cos(W*T))/W
        ERROR = YTHEORY - Y
        t.append(T)
        YRK.append(Y)
        YT.append(YTHEORY)
        E.append(ERROR)
    plt.plot(t,YT,'k:', Label='THEORY')
    plt.plot(t,YRK,'b-',Label='RUNGE-KUTTA')
    plt.plot(t,E,'r-',Label='ERROR')
    plt.legend(loc='upper right')
    plt.show()

def Euler(W,T,Tf,S,Y,YD,X,H):
    t = []
    YRK = []
    YT = []
    E = []
    while T < Tf:
        S+=H
        Yold=Y
        YDold=YD
        YDD = W*X - W*W*Y
        Y  += H * YD
        YD += H * YDD
        T  += H
        if S >= .01:
            continue
        S = 0
        YTHEORY = (1 - np.cos(W*T))/W
        ERROR = YTHEORY - Y
        t.append(T)
        YRK.append(Y)
        YT.append(YTHEORY)
        E.append(ERROR)
    plt.plot(t,YT,'k:', Label='THEORY')
    plt.plot(t,YRK,'b-',Label='EULER')
    plt.plot(t,E,'r-',Label='ERROR')
    plt.legend(loc='upper right')
    plt.show()


'''
def RungeKutta(W,T,Tf,Sc,Y,YD,X,H):
    t = []
    YRK = []
    YT = []
    E = []
    S=0
    while T < Tf:
        S+=H
        Yold=Y
        YDold=YD
        YDD = W*X - W*W*Y
        Y  += H * YD
        YD += H * YDD
        T  += H
        YDD = W*X - W*W*Y
        YD = .5 * (YDold + YD + H*YDD)
        Y  = .5 * (Yold + Y + H* YD)
        if S >= Sc:
            continue
        S = 0
        YTHEORY = (1 - np.cos(W*T))/W
        ERROR = YTHEORY - Y
        t.append(T)
        YRK.append(Y)
        YT.append(YTHEORY)
        E.append(ERROR)
    return t,YRK,YT,E

def Euler(W,T,Tf,Sc,Y,YD,X,H):
    t = []
    YRK = []
    YT = []
    E = []
    S=0
    while T < Tf:
        S+=H
        Yold=Y
        YDold=YD
        YDD = W*X - W*W*Y
        Y  += H * YD
        YD += H * YDD
        T  += H
        if S >= Sc:
            continue
        S = 0
        YTHEORY = (1 - np.cos(W*T))/W
        ERROR = YTHEORY - Y
        t.append(T)
        YRK.append(Y)
        YT.append(YTHEORY)
        E.append(ERROR)
    return t,YRK,YT,E
def plot(H1,H2,H3):
    t,YRK,YT,E=Euler(20,0,1,.1,0,0,1,H1)
    plt.plot(t,YT,'k:', Label='THEORY')
    plt.plot(t,YRK,'b-',Label=('EULER'+str(H1)))
    t,YRK,YT,E=Euler(20,0,1,.1,0,0,1,H2)
    plt.plot(t,YRK,Label=('EULER'+str(H2)))
    #t,YRK,YT,E=Euler(20,0,1,.11,0,0,1,H3)
    #plt.plot(t,YRK,Label=('EULER'+str(H3)))
    #t,YRK,YT,E=RungeKutta(20,0,1,.1,0,0,1,H1)
    #plt.plot(t,YRK,Label=('RK'+str(H1)))
    t,YRK,YT,E=RungeKutta(20,0,1,.1,0,0,1,H2)
    plt.plot(t,YRK,Label=('RK'+str(H2)))
    t,YRK,YT,E=RungeKutta(20,0,1,.1,0,0,1,H3)
    plt.plot(t,YRK,Label=('RK'+str(H3)))
    plt.legend(loc='best')
    plt.show()
def error(H1,H2,H3):
    t,YRK,YT,E=Euler(20,0,1,.1,0,0,1,H1)
    plt.plot([0,1],[0,0],'k:', Label='Zero')
    plt.plot(t,(np.array(E)/.05*100),'b-',Label=('EULER'+str(H1)))
    t,YRK,YT,E=Euler(20,0,1,.1,0,0,1,H2)
    plt.plot(t,(np.array(E)/.05*100),Label=('EULER'+str(H2)))
    #t,YRK,YT,E=Euler(20,0,1,.11,0,0,1,H3)
    #plt.plot(t,YRK,Label=('EULER'+str(H3)))
    #t,YRK,YT,E=RungeKutta(20,0,1,.1,0,0,1,H1)
    #plt.plot(t,YRK,Label=('RK'+str(H1)))
    t,YRK,YT,E=RungeKutta(20,0,1,.1,0,0,1,H2)
    plt.plot(t,(np.array(E)/.05*100),Label=('RK'+str(H2)))
    t,YRK,YT,E=RungeKutta(20,0,1,.11,0,0,1,H3)
    plt.plot(t,(np.array(E)/.05*100),Label=('RK'+str(H3)))
    plt.legend(loc='best')
    plt.show()
error(.001,.01,.001)

#RungeKutta(20,0,1,.1,0,0,1,.01)
