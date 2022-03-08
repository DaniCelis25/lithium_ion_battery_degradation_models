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
Tref = 298

kt = 4.14 * 10 ** (-10)

sigma = 0.5

kSigma = 1.04
sigmaRef = 0.5

kdelta1 =  1.40 * (10 ** (1))
kdelta2 = -5.01 * (10 ** (-1))
kdelta3 = -1.23 * (10 ** (1))

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

def F_d1(Sd, St, Ssoc, STc):
    result =(Sd + St) * Ssoc * STc
    return result

def L_cyc(N, fd1):
  result = 1 - AlphaSei * (e ** (-(N) * BetaSei * fd1)) - (1 - AlphaSei) * (e ** (-(N) * fd1))
  return result

def f_d1(delta, t, sigma, T):
  Sd_valor = sd(delta)
  St_valor = st(t)
  ssoc_valor = ssoc()
  stc_valor = stc(T)
  result = (Sd_valor + St_valor) * ssoc_valor * stc_valor
  return result

# exponential models Sde
def Sde(delta):
  result = kdelta1 * delta * (e ** (kdelta2 * delta))
  return result

# quadratic models Sdq
def Sdq(delta):
  result = kdelta1 * (delta ** kdelta2)
  return result

list_e = []
list_q = []
list_L_cyc = []

ciclos = 0
for delta in range(20, 140, 20):
    delta = delta/100
    
    F_d1_result = F_d1(delta, Año, sigma, 308)  
    L_cyc_result = L_cyc(ciclos, F_d1_result) 
    list_L_cyc.append(L_cyc_result) 
    ciclos += 20000
    
    Sde_valor = Sde(delta)
    list_e.append(Sde_valor)
    
    Sdq_valor = Sdq(delta)  
    list_q.append(Sdq_valor)

print("Exponencial: "+str(list_e))
print("Cuadratica: "+str(list_q))
print("L_cyc: "+str(list_L_cyc))

p = [0,0.2,0.4,0.6,0.8,1]


plt.subplots()
plt.plot(p[0], list_q[0], marker = 'o')
plt.plot(p[1], list_q[1], marker = 'o')
plt.plot(p[2], list_q[2], marker = 'o')
plt.plot(p[3], list_q[3], marker = 'o')
plt.plot(p[4], list_q[4], marker = 'o')
plt.plot(p[5], list_q[5], marker = 'o')
plt.plot(p[0], list_e[0], marker = 's')
plt.plot(p[1], list_e[1], marker = 's')
plt.plot(p[2], list_e[2], marker = 's')
plt.plot(p[3], list_e[3], marker = 's')
plt.plot(p[4], list_e[4], marker = 's')
plt.plot(p[5], list_e[5], marker = 's')
plt.plot(p[0], list_L_cyc[0], marker = '>')
plt.plot(p[1], list_L_cyc[1], marker = '>')
plt.plot(p[2], list_L_cyc[2], marker = '>')
plt.plot(p[3], list_L_cyc[3], marker = '>')
plt.plot(p[4], list_L_cyc[4], marker = '>')
plt.plot(p[5], list_L_cyc[5], marker = '>')
plt.grid(axis = 'x', color = 'gray', linestyle = 'dashed')
plt.grid(axis = 'y', color = 'gray', linestyle = 'dashed')
plt.title('Envejecimiento ciclico')
plt.xlabel('DoD[%]')
plt.ylabel('Números de ciclos (10^4)')
plt.legend(loc = 'lower left')
plt.ylim(0,30)
plt.show()













