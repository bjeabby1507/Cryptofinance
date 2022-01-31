# double spending

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

# input parameters
# z : confirmations needed 
# q: hashrate
# A: seuil de tolerance
# v: montant de la double depesnse
# N : nb de cycle d'attaque
# k : nb of premined block

#output 
# rendement par unité de temps : revenue total gagané / tps
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
    etat = np.random.choice((True, False),p=[proba,1-proba])
    return(etat)

def Sim(q,z,A,k,v):
    H=0 # official chain
    AliceChain=k # number selfish block mined
    succesAttempt =0
    progress =0
    # seuil de tolérence respecté et seuil de confirmation : sécurité respecté
    while(H - AliceChain)< A and H<z and AliceChain<z:
        piece=profil(q)
        if piece:
            # selfish miner found a block and don't publish it.
            succesAttempt +=1 
            AliceChain+=1
        else:
            # honest miners found a block
            H+=1
            
    if AliceChain> H:
        succesAttempt += v
        H = AliceChain
    else : 
        succesAttempt = 0
    #print(succesAttempt, H)       
    return [succesAttempt, H]

def simulate(N,q,z,A,k,v):
    Rn=0
    Hn=0
    for i in range(N):
        RH = Sim(q,z,A,k,v) 
        #print(RH)
        # experimental rendement
        Rn+=RH[0]
        Hn+=RH[1]
    #print("Rn",Rn)
    #print("Hn",Hn)
    Rend = Rn/Hn
    #print("rendement : ", Rend)
    return Rend 
root = tkinter.Tk()
root.wm_title("Double spending")
fig = Figure(figsize=(5, 4), dpi=100)

# To create a canvas for the figure
canvas = FigureCanvasTkAgg(fig, master=root) 
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

# To create a toolbar under the figure
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

def Graph(event):
    k=0
    v= 1
    # liste de hashrate, de 0.01 à 0.5
    Hashrate = [0] * 50
    # lsite des esperances de gains
    EsperanceGains = [0] * 50
    EsperanceGains10 = [0] * 50
    EsperanceGains6 = [0] * 50
    for p in range(1,50):
        #l'attaque est générée pour chaque q représentant q, le hashrate
        EsperanceGains[p] = simulate(N.get(),p/100,6,3,k,v)
        EsperanceGains6[p] = simulate(N.get(),p/100,6,10,k,v)
        EsperanceGains10[p] = simulate(N.get(),p/100,10,3,k,v)
        Hashrate[p] = p/100
    fig.clear()
    #Espérance de gains en fonction du hashrate
    ax1=fig.add_subplot(111)
    ax1.grid(linestyle='dotted')
    ax1.plot(Hashrate, EsperanceGains, label='sim, confirmations=6 , A=3')
    ax1.legend() # add a legend
    ax1.plot(Hashrate, EsperanceGains6, label='sim, confirmations=6 , A=10')
    ax1.legend() # add a legend
    ax1.plot(Hashrate, EsperanceGains10, label='sim, confirmations=10 , A=3')
    ax1.legend() # add a legend
    ax1.plot(Hashrate, Hashrate, label='Honest')
    ax1.legend() # add a legend
    #idx = np.argwhere(np.diff(np.sign(np.array(Hashrate) - np.array(EsperanceGains)))).flatten()
    #idx6 = np.argwhere(np.diff(np.sign(np.array(Hashrate) - np.array(EsperanceGains6)))).flatten()
    #idx10 = np.argwhere(np.diff(np.sign(np.array(Hashrate) - np.array(EsperanceGains10)))).flatten()
    #print(idx)
    #print('Experimental : minimum Esperance de gain z=6 , A=3, Hashrate[idx[1]] =' ,Hashrate[idx[1]])
    #print('Experimental : minimum Esperance de gain z=6 , A=10, Hashrate[idx[1]] =' ,Hashrate[idx6[1]])
    #print('Experimental : minimum Esperance de gain  z=10 , A=3, Hashrate[idx[1]] =' ,Hashrate[#idx10[1]])
    ax1.set_xlabel('Hashrate')
    ax1.set_ylabel('Esperance de gain')
    ax1.set_title('Double spending')
    canvas.draw()

N = tkinter.Scale(master=root, from_=1, to=2000, orient=tkinter.HORIZONTAL, length=200,label="N : nbr d'attaquees", command=Graph)
N.pack(side=tkinter.BOTTOM)
tkinter.mainloop()
if __name__ == "__main__":
    q=0.44
    z=6
    N=10**5
    A=3
    k=0
    v= 1
    #print ("Simulated probability :",simulate(N,q,z,A,k,v))