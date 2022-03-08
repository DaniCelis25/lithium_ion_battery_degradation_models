# -*- coding: utf-8 -*-
"""
@author: Daniela
"""

from math import e
import matplotlib.pyplot as plt

#Constantes
Año = 60 * 60 * 24 * 365

AlphaSei = 5.75 * (10 **(-2))
BetaSei = 121

kT = 6.93 * (10 ** (-2))
Tref = 293

kt = 4.14 * 10 ** (-10)

sigma = 1

kSigma = 1.04
sigmaRef = 0.5

kdelta1 =  1.40 * (10 ** 5)
kdelta2 = -5.01 * (10 ** (-1))
kdelta3 = -1.23 * (10 ** 5)


# STc Funcion
def stc(T):
  result = e ** (kT * (T - Tref) * (Tref/T))
  return result

#Ssoc Funcion
def ssoc():
  result = e ** (kSigma * (sigma - sigmaRef))
  return result

# St Funcion
def st(t):
  result = kt * t
  return result

# Sd Funcion                      
def sd(delta):
  result = (kdelta1 * (delta ** kdelta2) + kdelta3) ** (-1)
  return result

def f_dt(St, Ssoc, STc):
  result = St * Ssoc * STc
  return result

def L_cal(t, f_dt):
  result = 1 - (AlphaSei * (e ** (-t * BetaSei * f_dt))) - (1 - AlphaSei) * (e ** (-t * f_dt))
  return result

list_L = []
count = 0

for T in range(278, 338, 10):
  print("------ Para la temperatura : "+str(T)+" ------")
  list_L.append([])
  for p in range(0,6):
    j = Año * p
    print("      -- Para el año: "+str(p)+" --")
    St_result = st(j)
    print("St_result= " + str(St_result))
    STc_result = stc(T)
    print("STc_result= "+ str(STc_result))
    Ssoc_result = ssoc()
    print("Ssoc_result= "+ str(Ssoc_result))
    fdt_result = f_dt(St_result, Ssoc_result, STc_result)
    print("fdt_result= "+ str(fdt_result))
         
    L = L_cal(p, fdt_result)
    L1 = (1 - L)*100
        
    list_L[count].append(L1)   
  count = count +1

print("L= "+str(list_L))

year = [0,1,2,3,4,5]

plt.subplots()
plt.plot(year, list_L[0], marker = 's', label= 'T=15(°C)')
plt.plot(year, list_L[1], marker = 's', label= 'T=25(°C)')
plt.plot(year, list_L[2], marker = 's', label= 'T=35(°C)')
plt.plot(year, list_L[3], marker = 's', label= 'T=45(°C)')
plt.plot(year, list_L[4], marker = 's', label= 'T=55(°C)')
plt.grid(axis = 'x', color = 'gray', linestyle = 'dashed')
plt.grid(axis = 'y', color = 'gray', linestyle = 'dashed')
plt.title('Envejecimiento calendario con temperatura variable')
plt.xlabel('Tiempo[año]')
plt.ylabel('Capacidad Restante (%)')
plt.legend(loc = 'lower left')
plt.ylim(0,110)
plt.show()


