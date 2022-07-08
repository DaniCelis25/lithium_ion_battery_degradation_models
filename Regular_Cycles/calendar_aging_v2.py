# -*- coding: utf-8 -*-
"""
@author: Daniela Celis Álvarez
"""
"""Se necesita el e para el valor de la exponencial"""
""" se importa solo la libreria de matplotlib para graficar y observar la degradacion del envejecimiento calendario"""
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

"""son valores de referencia"""
Tref = 293 
sigmaRef = 0.5

"""tiempo en año medido en segudos""" 
Año = 60 * 60 * 24 * 365  

"""este parametro se modifica para ver distintos SoC"""
sigma = 0.5  

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

"""función de tasa de degradacion linealizada por unidad de tiempo"""
def f_dt(St, Ssoc, STc):
    """esta ecuacion multiplica los factores de estres y representa la tasa de degradacion linealizada por unidad de tiempo"""
    result = St * Ssoc * STc
    return result

"""función para calcular la vida util del envejecimiento calendario de la batería """
def L_cal(t, f_dt):
    """esta ecuacion biexponencial representa la vida util del envejecimiento calendario"""
    result = 1 - (AlphaSei * (e ** (-t * BetaSei * f_dt))) - (1 - AlphaSei) * (e ** (-t * f_dt))
    return result

"""se hace una lista y además se crea una variable para que comience del valor 0"""
list_L = []
count = 0
"""se realiza un for para el rango de temperatura"""
for T in range(278, 338, 10):
  #print("------ Para la temperatura : "+str(T)+" ------")
  list_L.append([])
  """lo mismo para el p que viene siendo la cantidad de años y esto se multiplica por un año en segundos"""
  for p in range(0,11):
    t = Año * p
    #print("      -- Para el año: "+str(t)+" --")
    """se evalua estos parametros en las funciones detalladas anteriormente"""
    St_result = st(t)
    STc_result = stc(T)
    Ssoc_result = ssoc()
    """ aqui se obtiene la funcion de tasa de degradacion linealizada"""
    fdt_result = f_dt(St_result, Ssoc_result, STc_result)
    #print("fdt_result= "+ str(fdt_result))
    """ el L es el calculo de la vida util evaluada en los parametros"""     
    L = L_cal(p, fdt_result)
    """y se crea un L1 para poder observar la capacidad restante de la bateria"""
    """cuando esta nueva la bateria es L=0"""
    L1 = (1 - L)*100 
    """se crea esta lista para guardar los valores"""    
    list_L[count].append(L1)
  """finalmente cada vez que pase por el for se guardara un valor en el count"""
  count = count +1

"""esto se hizo para poder representar de mejor manera el eje x"""
year = [0,1,2,3,4,5,6,7,8,9,10]

"""y esto es para graficar el envejecimiento calendario con respecto a un estado de carga fijo"""
""" pero con temperatura variable"""
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
