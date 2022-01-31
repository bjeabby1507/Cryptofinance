#Selfish mining

#rentable tout le temps si gamma = 1 ?
# rentable si alpha > 33% ?
from random import random
#  graphique
import tkinter
import numpy as np
import matplotlib.pyplot as plt
# To display curves in the GUI
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings
from matplotlib.figure import Figure

def Sim(alpha,gamma,N):
    state=0
    H=0 #LongestChainLength
    AliceBlock=0 # number selfish block mined

    #round begin state=0 , finish when state=0 again
    for i in range(N):
        piece=random()
    
        if state==0:
            #Initial State, the selfish miners have 0 hidden block.
            if piece<=alpha:
                # selfish miner found a block and don't publish it. 
                state=1
                # n=1 , hidden block
            else:
                # honest miners found a block,the round is finished
                H+=1 #reveal
                state=0
    
        elif state==1:
            #There is one hidden block
            if piece<=alpha:
                # selfish miners found a new block, => total of two blocks ahead and hidden.
                state=2
                n=2
            else:
                state=-1

        elif state==-1:
            # honest miners found a block.
            #the selfish miners publish their hidden block.
            # blockchain is forked with one block in each fork.
            if piece<=alpha:
                # selfish miners found a block in their fork.
                # Selfish miners won 2 blocks and the honest miners 0.
                AliceBlock+=2
                H+=2 #reveal
                state=0
            elif piece<=(1-alpha)*(1-gamma):
                # honest miners found a block in the fork of the selfish miners.
                # Selfish miners won 1 blocks and the honest miners 1.
                AliceBlock+=1
                H+=2 #reveal
                state=0
            else:
                # honest miners found a block in their fork.
                # Selfish miners won 0 blocks and the honest miners 2.
                AliceBlock+=0
                H+=2 #reveal
                state=0
                
        elif state==2:
            # selfish miners have 2 hidden blocks
            if piece<=alpha:
                # selfish miners found a new hidden block
                n+=1
                state=3
            else:
                # honest miners found a block.
                # selfish miners are only one block ahead of the honest miners,
                # they publish their hidden chain which is of length n.
                # round finished : Selfish miners won n blocks
                H+=n #reveal
                AliceBlock+=n
                state=0
        elif state>2:
            if piece<=alpha:
                # selfish miners found a new hidden block
                n+=1
                state+=1
            else:
                # honest miners found a block the network is catching up
                # selfish miners loose 1 block of lead
                state-=1
    #print(AliceBlock , H)
    if H!=0 :       
        return float(AliceBlock)/H  #, state


root = tkinter.Tk()
root.wm_title("Selfish mining")
fig = Figure(figsize=(5, 4), dpi=100)

# To create a canvas for the figure
canvas = FigureCanvasTkAgg(fig, master=root) 
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

# To create a toolbar under the figure
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

def Graph(event):
    gamma=0.5
    # liste de hashrate, de 0.01 à 1
    Hashrate = [0] * 50
    # lsite des esperances de gains
    EsperanceGains = [0] * (50)
    for p in range(1,50):
        #l'attaque est générée pour chaque q représentant q, le hashrate
        EsperanceGains[p] = Sim(p/100,gamma,N.get())
        Hashrate[p] = p/100
    fig.clear()
    #Espérance de gains en fonction du hashrate
    ax1=fig.add_subplot(111)
    ax1.grid(linestyle='dotted')
    ax1.plot(Hashrate, EsperanceGains, label='sim')
    ax1.legend() # add a legend
    ax1.plot(Hashrate, Hashrate, label='Honest')
    ax1.legend() # add a legend
    idx = np.argwhere(np.diff(np.sign(np.array(Hashrate) - np.array(EsperanceGains)))).flatten()
    print(idx)
    print('Experimental : minimum Esperance de gain, Hashrate[idx[1]] =' ,Hashrate[idx[1]])
    ax1.set_xlabel('Hashrate')
    ax1.set_ylabel('Esperance de gain')
    ax1.set_title('Selfish mining')
    canvas.draw()

N = tkinter.Scale(master=root, from_=1, to=10000, orient=tkinter.HORIZONTAL, length=200,label="N : nbr d'attaquees", command=Graph)
N.pack(side=tkinter.BOTTOM)

tkinter.mainloop()
def main():
    alpha=0.33 #q hasrate/  the fraction of the network’s total hashpower controlled by the attacker
    # β  = 1 - alpha : Computation power of Bob (public miners, honest)
    # β + α = 1.
    gamma=0.5  #connectivity : attacker’s influence :fraction of Bob’s networkthat will mine on Alice’s block 
    N=10**6

    print ("Simulated probability :",Sim(alpha,gamma,N))
if __name__ == "__main__":
    main()