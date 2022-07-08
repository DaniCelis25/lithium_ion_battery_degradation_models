# -*- coding: utf-8 -*-
"""
@author: Daniela Celis Álvarez
"""
"""Se necesita el e para el valor de la exponencial"""
""" se importa solo la libreria de matplotlib para graficar y observar la degradacion del envejecimiento ciclico"""
from math import e
import matplotlib.pyplot as plt

""" a continuación se muestran las constantes que se utilizaron"""
"""alpha y beta son constante que dependen del diseño de la bateria"""
"""fueron proporcionadas por el fabricante"""
AlphaSei = 5.75 * (10 **(-2))
BetaSei = 121

"""las constante kT, kt y kSigma, son parametros que se pueden determinar"""
""" obteniendo un conjunto de datos de pruebas de envejecimiento calendario"""
kT = 6.93 * (10 ** (-2))
kt = 4.14 * 10 ** (-10)
kSigma = 1.04


"""las constante kdelta1, kdelta2 y kdelta 3, son parametros que se obtienen de un conjunto de datos de envejecimiento ciclico"""
kdelta1 =  1.40 * (10 ** (5))
kdelta2 = -5.01 * (10 ** (-1))
kdelta3 = -1.23 * (10 ** (5))

"""son valores de referencia"""
Tref = 298
sigmaRef = 0.5 

"""son valores que se consideraron igual a lo de referencia por conveniencia"""
T = 298  # en este caso se considero la temperatura de referencia
sigma = 0.5  # en este caso se considero SoC de referencia

"""se considera el tiempo de un ciclo de carga y descarga de la bateria que es aprox dos horas en segundos"""
hr_cyc = 60 * 60 * 2 

"""modelos de degradacion"""
"""factor de estres de temperatura"""
def stc(T):
   """esta ecuacion exponencial representa el factor de estres de la temperatura"""
   result = e ** (kT * (T - Tref) * (Tref/T))
   return result

"""factor de estres de del de estado de carga"""
def ssoc():
    """esta ecuacion exponencial representa el factor de estres del estado de carga"""
    result = e ** (kSigma * (sigma - sigmaRef))
    return result

"""factor de estres del tiempo"""
def st(t):
    """esta ecuacion lineal representa el factor de estres del tiempo"""
    result = kt * t
    return result

"""factor de estres de la profundidad de descarga"""                
def sd(delta):
    """esta ecuacion representa el factor de estres de la profundidad de descarga"""
    result = ((kdelta1 * (delta ** kdelta2)) + kdelta3) ** (-1)
    return result

"""función de tasa de degradacion linealizada por ciclo de vida de la bateria"""
def F_d1(Sd, St, Ssoc, STc):
    """esta ecuacion representa la tasa de degradacion linealizada por ciclo"""
    result =(Sd + St) * Ssoc * STc
    return result

"""función para calcular la vida util del envejecimiento ciclico de la batería """
def L_cyc(N, fd1):
    """esta ecuacion biexponencial representa la vida util del envejecimiento calendario"""
    result = 1 - AlphaSei * (e ** (-N * BetaSei * fd1)) - (1 - AlphaSei) * (e ** (-N * fd1))
    return result

"""se hace una lista y además se crea una variable para que comience del valor 0"""
list_L_cyc = []
count = 0
"""se realiza un for para el rango de delta"""
for delta in range(20, 120, 10):
    delta = delta/100
    """lo mismo para el N que viene siendo el numero de ciclos"""
    for N in range(0,6000,1000): 
        list_L_cyc.append([]) 
        """se evalua estos parametros en las funciones detalladas anteriormente"""
        Sd_valor = sd(delta)
        St_valor = st(hr_cyc)
        Ssoc_valor = ssoc()
        STc_valor = stc(T)
        """ aqui se obtiene la funcion de tasa de degradacion linealizada"""
        F_d1_result = F_d1(Sd_valor,St_valor, Ssoc_valor,STc_valor)
        """ el L es el calculo de la vida util evaluada en los parametros"""     
        L_cyc_result = L_cyc(N, F_d1_result) 
        L = L_cyc_result
        """y se crea un L2 para poder observar la capacidad restante de la bateria"""
        """cuando esta nueva la bateria es L=0"""
        L2= (1-L)*100 # La batería cuando esta nueva es L=0  y esto se hace para representar la capacidad restante 
        """se crea esta lista para guardar los valores"""
        list_L_cyc[count].append(L2) 
    """finalmente cada vez que pase por el for se guardara un valor en el count""" 
    count = count +1
    
"""esto se hizo para poder representar de mejor manera el eje x"""
N = [0,1000,2000,3000,4000,5000]

"""y esto es para graficar el envejecimiento ciclico con respecto a la profundidad de descarga"""
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
