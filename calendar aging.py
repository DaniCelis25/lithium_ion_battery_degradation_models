# -*- coding: utf-8 -*-
"""
@author: Daniela Celis Álvarez
"""

from math import e
import matplotlib.pyplot as plt

#Constantes de Tabla I
AlphaSei = 5.75 * (10 **(-2))
BetaSei = 121

kT = 6.93 * (10 ** (-2))
Tref = 293

kt = 4.14 * 10 ** (-10)
Año = 60 * 60 * 24 * 365  # un año en segundos

kSigma = 1.04
sigmaRef = 0.5
sigma = 0.5  # Aca lo modifque para los distintos SoC 


# Modelos:
# Factor de estrés de temperatura 
def stc(T):
  result = e ** (kT * (T - Tref) * (Tref/T))
  return result

# Factor de estrés de estado de carga SoC
def ssoc():
  result = e ** (kSigma * (sigma - sigmaRef))
  return result

# Factor de estrés de tiempo 
def st(t):
  result = kt * t
  return result

#Función de tasa de degradación linealizada por unidad de tiempo 
def f_dt(St, Ssoc, STc):
  result = St * Ssoc * STc
  return result

#Función para calcular la vida útil de la baterería
def L_cal(t, f_dt):
  result = 1 - (AlphaSei * (e ** (-t * BetaSei * f_dt))) - (1 - AlphaSei) * (e ** (-t * f_dt))
  return result

list_L = []
count = 0



for T in range(278, 338, 10):
  print("------ Para la temperatura : "+str(T)+" ------")
  list_L.append([])
  for p in range(0,11):
    t = Año * p
    print("      -- Para el año: "+str(t)+" --")
    St_result = st(t)
    STc_result = stc(T)
    Ssoc_result = ssoc()
    fdt_result = f_dt(St_result, Ssoc_result, STc_result)
    print("fdt_result= "+ str(fdt_result))
         
    L = L_cal(p, fdt_result)
    L1 = (1 - L)*100 #La batería cuando esta nueva es L=0  y esto se hace para representar la capacidad restante
        
    list_L[count].append(L1)   
  count = count +1


year = [0,1,2,3,4,5,6,7,8,9,10]

plt.subplots()
plt.plot(year, list_L[0], marker = 's', label= 'T = 288K')
plt.plot(year, list_L[1], marker = 's', label= 'T = 298K')
plt.plot(year, list_L[2], marker = 's', label= 'T = 308K')
plt.plot(year, list_L[3], marker = 's', label= 'T = 318K')
plt.plot(year, list_L[4], marker = 's', label= 'T = 328K')
plt.grid(axis = 'x', color = 'gray', linestyle = 'dashed')
plt.grid(axis = 'y', color = 'gray', linestyle = 'dashed')
plt.title('Envejecimiento calendario')
plt.xlabel('Tiempo[año]')
plt.ylabel('Capacidad Restante (%)')
plt.legend(loc = 'lower left')
plt.ylim(0,110)
plt.show()


