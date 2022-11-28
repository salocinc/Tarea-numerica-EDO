import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

#analitica: float -> float
#Es la solucion analitica exacta, recibe un valor de t y retorna TE(t)
def analitica(t):
    return np.e**(-0.06524*t)

#ecuacion: float,float -> float
#Recibe un t_n y un TE_n para retornar f(t_n,TE_n)
def ecuacion(t_n,TE_n):
    return -0.06524*TE_n

#pasoEuler: float, float -> float
#Recibe las coordenadas (t_n,TE_n) y multiplica f(t_n,TE_n) por h, que es el
#paso de discretizacion, para retornar la integral de f(t_n,TE_n) entre x_n
#y x_n+1
def pasoEuler(t_n,TE_n):
    return ecuacion(t_n,TE_n)*h

#pasoHeun: float,float -> float
#Recibe las coordenadas (t_n,TE_n) y multiplica f(t_n,TE_n)+f(t_n+h,TE_n1) por
#h y divide por 2 para realizar el cálculo de la integral mediante trapecios,
#donde TE_n1 es TE_n+1 calculada mediante el metodo de Euler progresivo
def pasoHeun(t_n,TE_n):
    TE_n1= TE_n+pasoEuler(t_n,TE_n)
    return (ecuacion(t_n,TE_n)+ecuacion(t_n+h,TE_n1))*h/2.0

#Para delta t = x, se necesita dividen los 240 meses en 240/x partes, por lo que
#se procede de la forma siguiente (para conseguir que el programa funcione, se
#tiene que cambiar el valor de x por el valor que corresponda):
deltat=x
particiones=240/deltat
#Para el eje x, se crea un arreglo de (240/x)+1 valores equiespaciados entre 0 y
#240
eje_t=np.linspace(0.0,240.0,int(particiones+1))
#h (paso de discretizacion) es:
h=eje_t[1]-eje_t[0]

#Para el calculo mediante el metodo de Euler progresivo:
#Para el eje de TE, se crea un arreglo de (240/x)+1 ceros en un principio,
#que luego se rellenara
eje_TEEuler=np.zeros(int(particiones+1))
#Debido a la condicion inicial TE(0)=1:
eje_TEEuler[0]=1
#Se rellena el eje de TEEuler de la siguiente manera:
for i in range(len(eje_t)):
    if i==particiones:
        break
    eje_TEEuler[i+1]=eje_TEEuler[i]+pasoEuler(eje_t[i],eje_TEEuler[i])

#Para el calculo mediante el metodo de Heun:
#Para el eje de TE, se crea un arreglo de (240/x)+1 ceros en un principio,
#que luego se rellenara
eje_TEHeun=np.zeros(int(particiones+1))
#Debido a la condicion inicial TE(0)=1:
eje_TEHeun[0]=1
#Se rellena el eje de TEHeun de la siguiente manera:
for i in range(len(eje_t)):
    if i==particiones:
        break
    eje_TEHeun[i+1]=eje_TEHeun[i]+pasoHeun(eje_t[i],eje_TEHeun[i])

#Ademas, como se pide comparar con la solucion analitica, se crea un arreglo de
#(240/x)+1 ceros en un principio,que luego se rellenara:
eje_TEAnalitica=np.zeros(int(particiones+1))
#Se rellena el eje de TEAnalitica de la siguiente manera:
for i in range(len(eje_t)):
    eje_TEAnalitica[i]=analitica(eje_t[i])

#Para graficar, se realiza lo siguiente:
green_patch = mpatches.Patch(color="green",label="Solucion analitica")
blue_patch = mpatches.Patch(color="blue",label="Metodo de Euler")
red_patch = mpatches.Patch(color="red",label="Metodo de Heun")
plt.figure(figsize=(10,5))

#Como se busca comparar ambos metodos con la solucion analitica, se hacen 2
#graficos juntos de la siguiente manera:

#Para la comparacion del calculo mediante el metodo de Euler progresivo con
#la solucion analitica:
plt.subplot(1,2,1)
plt.plot(eje_t,eje_TEAnalitica,color="green")
plt.plot(eje_t,eje_TEEuler, color="blue")
plt.title("Solucion analitica vs metodo de Euler progresivo")
plt.xlabel("t")
plt.ylabel("TE(t)")
plt.legend(handles=[green_patch,blue_patch])

#Para la comparacion del calculo mediante el metodo de Heun con la solucion
#analitica:
plt.subplot(1,2,2)
plt.plot(eje_t,eje_TEAnalitica,color="green")
plt.plot(eje_t,eje_TEHeun,color="red")
plt.title("Solucion analitica vs metodo de Heun")
plt.xlabel("t")
plt.ylabel("TE(t)")
plt.legend(handles=[green_patch,red_patch])

plt.show()

#Para calcular el error del metodo de Euler progresivo:
ErrorEuler=np.linalg.norm(eje_TEAnalitica-eje_TEEuler)
print("Error en norma 2 del metodo de Euler:", ErrorEuler)

#Para calcular el error del metodo de Heun:
ErrorHeun=np.linalg.norm(eje_TEAnalitica-eje_TEHeun)
print("Error en norma 2 del metodo de Heun:", ErrorHeun)









