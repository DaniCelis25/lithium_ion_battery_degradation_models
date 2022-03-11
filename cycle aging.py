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
Tref = 298
T = 298  # en este caso se considero la temperatura de referencia

kt = 4.14 * 10 ** (-10)
Hr_cyc = 60 * 60 * 2 # dos horas en segundos (es lo que se demora en cargar y descargar un bateria)

sigma = 0.5  # en este caso se considero SoC de referencia
kSigma = 1.04
sigmaRef = 0.5 

kdelta1 =  1.40 * (10 ** (5))
kdelta2 = -5.01 * (10 ** (-1))
kdelta3 = -1.23 * (10 ** (5))


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

# Factor de estrés de profundidad de descarga DoD                     
def sd(delta):
  result = ((kdelta1 * (delta ** kdelta2)) + kdelta3) ** (-1)
  return result

#Función de tasa de degradación linealizada por ciclo
def F_d1(Sd, St, Ssoc, STc):
    result =(Sd + St) * Ssoc * STc
    return result

#Función para calcular la vida útil de la baterería
def L_cyc(N, fd1):
  result = 1 - AlphaSei * (e ** (-N * BetaSei * fd1)) - (1 - AlphaSei) * (e ** (-N * fd1))
  return result


list_L_cyc = []
count = 0

for delta in range(20, 120, 10):
    delta = delta/100
    
    for N in range(0,6000,1000): 
        list_L_cyc.append([]) 
        
        Sd_valor = sd(delta)
        St_valor = st(Hr_cyc)
        Ssoc_valor = ssoc()
        STc_valor = stc(T)
        
        F_d1_result = F_d1(Sd_valor,St_valor, Ssoc_valor,STc_valor)
        L_cyc_result = L_cyc(N, F_d1_result) 
        
        L = L_cyc_result
        L2= (1-L)*100 # La batería cuando esta nueva es L=0  y esto se hace para representar la capacidad restante 
    
        list_L_cyc[count].append(L2) 
    count = count +1
    

N = [0,1000,2000,3000,4000,5000]

plt.subplots()
plt.plot(N, list_L_cyc[1], marker = '>', label= 'DoD = 30%')
plt.plot(N, list_L_cyc[3], marker = '>', label= 'DoD = 50%')
plt.plot(N, list_L_cyc[6], marker = '>', label= 'DoD = 80%')
plt.grid(axis = 'x', color = 'gray', linestyle = 'dashed')
plt.grid(axis = 'y', color = 'gray', linestyle = 'dashed')
plt.title('Envejecimiento ciclico')
plt.xlabel('Números de ciclos')
plt.ylabel('Capacidad restante (%)')
plt.legend(loc = 'lower left')
plt.ylim(40,110)
plt.show()












