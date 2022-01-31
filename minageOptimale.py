# jeu du minage : Stratégie de minage optimale
# 1)Stratégie de minage optimale avec retour sur la blockchain officielle dès que n blocks ont eté découvert 
# i.e longeur d'un cycle<=n où n est un entier fixé : calculer l'espérance du gain maximale

#2)Stratégie en prenant en compte la création de block orphelin: cout suplémentaire de c*(h+1) = h*c +c au lieu de c

from random import random
#  graphique
import tkinter
import numpy as np
import matplotlib.pyplot as plt
# To display curves in the GUI
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings
from matplotlib.figure import Figure
#import sys
#sys.setrecursionlimit(5000)

# a = attacker blocks
# h = network blocks
# n = nb of possible actions
# q = hashrate
# c = cost
def Esim(a,h,n,q,c):
    # let's begin to mine
    if n <= -1:
        return 0
    else:
        if a>h+1 :
            #the mineur has more block than the blockchain : he can wait or crush the blockchain
            #  E(a,h,n,q,c) = Max(h+1-c+E(a-h,0,n,q,c),qE(a+1,h,n-1,q,c)+(1-q)(E(a,h+1,n-1,q,c)-c)) 
            #p=1-q
            return max(h+1-c+Esim(a-h,0,n,q,c), q*(Esim(a+1,h,n-1,q,c)) + (1-q)*(Esim(a,h+1,n-1,q,c)-c))
        elif a==h+1 :
            #the miner will gain nothing if he crushes the blockchain ,he can wait
            # E(a,h,n,q,c)= Max(h+1-c, qE(a+1,h,n-1,q,c)+(1-q)(E(0,h+1,n-1,q,c)-c))
            return max(h+1-c, q*(Esim(a+1,h,n-1,q,c)) + (1-q)*(Esim(a+1,h,n-1,q,c)-c))
        elif a <=h :
            #the miner will gain nothing if he crushes the blockchain ,he can wait or forfait
            # E(a,h,n,q,c)=Max(0,qE(a+1,h,n-1,q,c)+(1-q)(E(a,h+1,n-1,q,c)-c))
            return max(0, q*(Esim(a+1,h,n-1,q,c)) + (1-q)*(Esim(a,h+1,n-1,q,c)-c))

#prise en compte des bloc orphelin remplacer c par c*(h+1) = h*c+c : pour tout n , E(0,0,n,q,c)=0 pour tout q<1/2
def EsimOrphelin(a,h,n,q,c):
    # let's begin to mine
    if n <= -1:
        return 0
    else:
        if a>h+1 :
            #the mineur has more block than the blockchain : he can wait or crush the blockchain
            #  E(a,h,n,q,c) = Max(h+1-c+E(a-h,0,n,q,c),qE(a+1,h,n-1,q,c)+(1-q)(E(a,h+1,n-1,q,c)-c)) 
            #p=1-q
            return max(h+1-c*(h+1)+Esim(a-h,0,n,q,c), q*(Esim(a+1,h,n-1,q,c)) + (1-q)*(Esim(a,h+1,n-1,q,c)-c))
        elif a==h+1 :
            #the miner will gain nothing if he crushes the blockchain ,he can wait
            # E(a,h,n,q,c)= Max(h+1-c, qE(a+1,h,n-1,q,c)+(1-q)(E(0,h+1,n-1,q,c)-c))
            return max(h+1-c*(h+1), q*(Esim(a+1,h,n-1,q,c)) + (1-q)*(Esim(a+1,h,n-1,q,c)-c))
        elif a <=h :
            #the miner will gain nothing if he crushes the blockchain ,he can wait or forfait
            # E(a,h,n,q,c)=Max(0,qE(a+1,h,n-1,q,c)+(1-q)(E(a,h+1,n-1,q,c)-c))
            return max(0, q*(Esim(a+1,h,n-1,q,c)) + (1-q)*(Esim(a,h+1,n-1,q,c)-c))
if __name__ == "__main__":
    a=0
    h=0
    n=3
    q=0.35
    #c=q
    #calculer E(0,0,3,q,q)
    A=Esim(a,h,n,q,q) #doesn't work
    print(A)