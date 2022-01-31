from random import randrange
from hashlib import sha256
from time import perf_counter , perf_counter_ns

#  graphique
import tkinter
import numpy as np
import matplotlib.pyplot as plt
# To display curves in the GUI
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings
from matplotlib.figure import Figure

def time_hash(element,digits):
    """
        Find the total time to hash n strings of k length each.
    """
    n=1
    nelement = element
    start_time= perf_counter()
    while sha256(nelement.encode('utf-8')).hexdigest()[0:digits] !="0"*digits:
        n+=1
        nelement= f'{element}{n}'
    #print(sha256(nelement.encode('utf-8')).hexdigest())
   # return (element,n,sha256(nelement.encode('utf-8')).hexdigest())
    end_time = perf_counter()
    total_time = (end_time - start_time)
    #print("start time:", start_time)
    #print("end time:", end_time)
    #print("Total time:", total_time)
    return total_time
    
def rep(N,T):
    total_time= 0.0
    for i in range(0, N):
        element = str(randrange(0,100000))
        total_time +=time_hash(element,T)
    moyenne = total_time/N
    print("N (Nb de blocs):", N,"\nR (Target) :", T,"\nP (moyenne) : ",moyenne )   
"""
root = tkinter.Tk()
root.wm_title("Proof of Work")
fig = Figure(figsize=(5, 4), dpi=100)

# To create a canvas for the figure
canvas = FigureCanvasTkAgg(fig, master=root) 
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

# To create a toolbar under the figure
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

def Graph(event):
    maxTime= 7
    targetAxis =np.arange(0,maxTime,1)
    Y=[]
    for p in targetAxis:
        #l'attaque est générée pour chaque q représentant q, le hashrate
        Y.append(rep(100,p)) 

    fig.clear()
    #Espérance de gains en fonction du hashrate
    ax1=fig.add_subplot(111)
    ax1.grid(linestyle='dotted')
    ax1.plot(targetAxis, Y, label='sim')
    ax1.legend() # add a legend
    ax1.set_xlabel('Target')
    ax1.set_ylabel('Probability')
    ax1.set_title('Proof of Work')
    canvas.draw()

N = tkinter.Scale(master=root, from_=100, to=120, orient=tkinter.HORIZONTAL, length=200,label=" t : difficulty / target", command=Graph)
N.pack(side=tkinter.BOTTOM)

tkinter.mainloop()"""

if __name__ == "__main__":
    T= 4 # difficulty / target
    rep(100,T)