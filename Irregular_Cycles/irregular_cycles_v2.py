# -*- coding: utf-8 -*-
"""
@author: Daniela
"""
"""Se necesita el e para el valor de la exponencial"""
"""se importa la libreria rainflow para contabilizar los ciclos irregulares"""
"""se importa la libreria pandas para leer un archivo de excel"""
""" se importa la libreria de matplotlib para graficar y observar la degradacion del envejecimiento ciclico"""
from math import e
import rainflow as rf
import pandas as pd
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
sigmaRef = 0.7
Tref = 298

"""este T es la temperatura promedio que se obtiene al tomar los datos de pruebas de la bateria"""
"""en este caso los datos obtenidos no tenian ese dato así que se tomo como referencia una T= 25°C"""
T = 298
"""se considera el tiempo de un ciclo de carga y descarga de la bateria que es aprox dos horas en segundos"""
hr_cyc = 60 * 60 * 2 

"""modelos de degradacion"""
"""factor de estres de temperatura"""
def stc(T):
    """esta ecuacion exponencial representa el factor de estres de la temperatura"""
    result = e ** (kT * (T - Tref) * (Tref/T))
    return result

"""factor de estres de del de estado de carga"""
def ssoc(sigma):
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

"""se hace dos listas y además se crea una variable para que comience del valor 0"""
list_L_cyc = []
list_L_cyc_L2=[100]
count = 0
"""esta variable se crea para leer un documento de excel"""
df = pd.read_excel('SOC.xlsx')
(df.head())
#print(df)
""" esto es para darle nombre a las columnas que ocupare del excel"""
t = df['time(s)']
soc = df['soc']
#print(soc)
"""esta funcion es para determinar el numero de ciclos irregulares del perfil del SoC"""
soc_rf = rf.count_cycles(soc)
#print(soc_rf)
""" se crean lista para guardar los datos de las datos que se piden extraer de la funcion rf.extract_cycles"""
prom = []
rango_a=[]
media=[]
cycle_count=[]
""" este for es para obtener mas informacion desde el modulo rainflow"""
for rng, mean, conteo, start, end in rf.extract_cycles(soc):
    #print(rng,mean,conteo,start, end)
    """se guardan los datos que se extrajeron del modulo en la listas creadas anteriormente"""
    rango_a.append(rng) 
    media.append(mean)
    cycle_count.append(conteo)
    """ se crean estas variables con los datos que nos da de resultados del modulo rainflow para utilizarlos en los modelos"""
    delta = rng*2
    sigma = mean
    N = conteo
    """se evalua estos parametros en las funciones detalladas anteriormente"""
    Sd_valor = sd(delta)
    St_valor = st(hr_cyc)
    Ssoc_valor = ssoc(sigma)
    STc_valor = stc(T)
    """ aqui se obtiene la funcion de tasa de degradacion linealizada"""
    F_d1_result = F_d1(Sd_valor,St_valor, Ssoc_valor,STc_valor)
    """ el L es el calculo de la vida util evaluada en los parametros"""
    L_cyc_result = L_cyc(N, F_d1_result) 
    L = L_cyc_result
    """y se crea un L2 para poder observar la capacidad restante de la bateria"""
    """cuando esta nueva la bateria es L=0"""
    L2= (list_L_cyc_L2[-1]/100-L)*100  
    #print(L2)
    #print(list_L_cyc_L2)
    """se crea estas listas para guardar los valores"""
    list_L_cyc.append(L)
    list_L_cyc_L2.append(L2) 
    """finalmente cada vez que pase por el for se guardara un valor en el count""" 
    count = count + 1  

"""esto es para graficar el envejecimiento ciclico con respecto a la capcidad restante(%)"""
plt.subplots()
""" se hace un for para que recorra todo los valores del numero de ciclos"""
for i in range(len(list_L_cyc_L2)):
  plt.plot(i, list_L_cyc_L2[i], marker = '>', color = 'g')
plt.grid(axis = 'x', color = 'gray', linestyle = 'dashed')
plt.grid(axis = 'y', color = 'gray', linestyle = 'dashed')
plt.title('Envejecimiento ciclico para ciclos irregulares')
plt.xlabel('Números de ciclos')
plt.ylabel('Capacidad restante (%)')
plt.legend(loc = 'lower left')
plt.xlim(0,550)
plt.ylim(98,102)
plt.show()
