# strategy : "1+2"
#import random 
from random import random
#  graphique
import tkinter
import numpy as np
import matplotlib.pyplot as plt
# To display curves in the GUI
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings
from matplotlib.figure import Figure

# random choice of Alice (Pile) or Bob (Face)
def profil(proba):
    etat = False #pile
    piece=random()
    """if piece <= proba: 
        #print("pile")
        etat = False
    else:
        #print("face")
        etat = True"""
    etat = np.random.choice((False, True),p=[proba,1-proba])
    return(etat)

#1+2 simulation
def sim(p):
    piece = profil(p)
    P=0 #alice block (selfish miner)
    F=0 # bob block
    R=0 #reward
    H=0 # hauteur : valid block
    # max 3 rounds
    if not piece:
        # selfish miner (Alice) found a block and don't publish it
        P+=1
        H+=1
        piece2= profil(p) # round 2
        piece3 = profil(p) # round 3
        if piece2 :
            # honest miner found a block
            F+=1
            H+=1
        else :
            # selfish miner found a 2nd block
            P+=1
            H+=1
        if piece3 :
            # honest minner found a 2nd block
            F+=1
            H+=1
        else :
            # selfish miner found a 3rd block
            P+=1
            H+=1
    else :
        # honest miner (Bob) found a block , and it's finished 
        F+=1
        H+=1
    #rend =P-F+1
    if P>F :
        R=P # Number of selfish mined block
        H=R # Longest chain block
    else :
        R=0 # Number of selfish mined block
        H=F # Longest chain block
    #print ("H (hauteur):", H,"\nR (récompense de Alice) :", R,"\nP (Alice finds) : ", P,"\nF(Bob finds) :", F, "\nrend :", rend)
    return [R,H]

#1+2 simulation , N times
def simulate(N,p):
    #piece =profil(p)
    #print ("piece :", piece)
    Rn=0
    Hn=0
    for i in range(N):
        RH = sim(p) 
        #print(RH)
        # experimental rendement
        Rn+=RH[0]
        Hn+=RH[1]
    #print("Rn",Rn)
    #print("Hn",Hn)
    Rend = Rn/Hn
    threndement = (3*p**3 + 4*(1-p)*p**2) / ((1-p) + 3*p**3 + 4*(1-p)*p**2 + 2*(1-p)**2*p)
    #print("rendement : ", Rend)
    return Rend , threndement

root = tkinter.Tk()
root.wm_title("1+2")
fig = Figure(figsize=(5, 4), dpi=100)

# To create a canvas for the figure
canvas = FigureCanvasTkAgg(fig, master=root) 
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

# To create a toolbar under the figure
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

def Graph(event):
    # liste de hashrate, de 0.01 à 1
    Hashrate = [0] * 100
    # lsite des esperances de gains
    EsperanceGains = [0] * 100
    EsperanceGainsTH = [0] * 100
    for p in range(1,100):
        #l'attaque est générée pour chaque q représentant q, le hashrate
        EsperanceGains[p] = simulate(N.get(),p/100)[0]
        EsperanceGainsTH[p]=simulate(N.get(),p/100)[1]
        Hashrate[p] = p/100
    fig.clear()
    #Espérance de gains en fonction du hashrate
    ax1=fig.add_subplot(111)
    ax1.grid(linestyle='dotted')
    ax1.plot(Hashrate, EsperanceGains, label='sim')
    ax1.legend() # add a legend
    ax1.plot(Hashrate, EsperanceGainsTH, label='theoretical')
    ax1.legend() # add a legend
    ax1.plot(Hashrate, Hashrate, label='Honest')
    ax1.legend() # add a legend
    idx = np.argwhere(np.diff(np.sign(np.array(Hashrate) - np.array(EsperanceGains)))).flatten()
    idTH = np.argwhere(np.diff(np.sign(np.array(Hashrate) - np.array(EsperanceGainsTH)))).flatten()
    #print(idx)
    #print(idTH)
    print('Experimental : minimum Esperance de gain, Hashrate[idx[1]] =' ,Hashrate[idx[1]])
    #ax1.scatter(Hashrate[elm], EsperanceGains[elm], label='indice',c='red')
    ax1.set_xlabel('Hashrate')
    ax1.set_ylabel('Esperance de gain')
    ax1.set_title('1+2')
    canvas.draw()

N = tkinter.Scale(master=root, from_=1, to=6000, orient=tkinter.HORIZONTAL, length=200,label="N : nbr d'attaquees", command=Graph)
N.pack(side=tkinter.BOTTOM)

tkinter.mainloop()
if __name__ == "__main__":
    N=10**4
    p=0.414  #41,4%
    q=1-p
    rendement=simulate(N,p)[0]
    threndement = (3*p**3 + 4*q*p**2) / (q + 3*p**3 + 4*q*p**2 + 2*q**2*p)
    print("N =",N,"p =",p*100,"% ","rendement exp =",rendement)
    print("N =",N,"p =",p*100,"% ","rendement th =",threndement)
    #piece=profil(p)
    #sim(piece,p)
    