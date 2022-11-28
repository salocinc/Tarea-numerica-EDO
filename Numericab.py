import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

#Para obtener los valores de TE_n-5, se usaran los valores obtenidos anteriormente
#en cada uno de los metodos, por lo que se hacen dos funciones "ecuaciones"

#ecuacionEuler: float,float -> float
#Recibe un t_n y un TE_n para retornar f(t_n,TE_n)
def ecuacionEuler(t_n,TE_n):
    return (0.1*TE_n)-(0.16524*eje_TEEuler[int(t_n/h)-int(5*iteracionesmes)])

#ecuacionHeun: float,float -> float
#Recibe un t_n y un TE_n para retornar f(t_n,TE_n)
def ecuacionHeun(t_n,TE_n):
    return (0.1*TE_n)-(0.16524*eje_TEHeun[int(t_n/h)-int(5*iteracionesmes)])

#pasoEuler: float, float -> float
#Recibe las coordenadas (t_n,TE_n) y multiplica f(t_n,TE_n) por h, que es el
#paso de discretizacion, para retornar la integral de f(t_n,TE_n) entre x_n
#y x_n+1
def pasoEuler(t_n,TE_n):
    return ecuacionEuler(t_n,TE_n)*h

#pasoHeun: float,float -> float
#Recibe las coordenadas (t_n,TE_n) y multiplica f(t_n,TE_n)+f(t_n+h,TE_n1) por
#h y divide por 2 para realizar el cálculo de la integral mediante trapecios,
#donde TE_n1 es TE_n+1 calculada mediante el metodo de Euler progresivo
def pasoHeun(t_n,TE_n):
    TE_n1= TE_n+pasoEuler(t_n,TE_n)
    return (ecuacionHeun(t_n,TE_n)+ecuacionHeun(t_n+h,TE_n1))*h/2.0

#Para delta t = x, se necesita dividen los 240 meses en 240/x partes, por lo que
#se procede de la forma siguiente (para conseguir que el programa funcione, se
#tiene que cambiar el valor de x por el valor que corresponda):
deltat=x
particiones=240/deltat
#iteracionesmes sera la cantidad de iteraciones que hay en un mes.
iteracionesmes=1/deltat

#Para el eje x, se crea un arreglo de (240/x)+1 valores equiespaciados entre 0 y
#240
eje_t=np.linspace(0.0,240.0,int(particiones+1))
#h (paso de discretizacion) es:
h=eje_t[1]-eje_t[0]

#Para el calculo mediante el metodo de Euler progresivo:
#Para el eje de TE, se crea un arreglo de (240/x)+1 ceros en un principio,
#que luego se rellenara
eje_TEEuler=np.zeros(int(particiones+1))
#Se rellena el eje de TEEuler de la siguiente manera:
for i in range(len(eje_t)):
    if i==particiones:
        break
    #debido a la condicion inicial:
    if i>=0 and i<=(5*int(iteracionesmes)):
        eje_TEEuler[i]=1
    else:
        eje_TEEuler[i]=eje_TEEuler[i-1]+pasoEuler(eje_t[i-1],eje_TEEuler[i-1])

#Para el calculo mediante el metodo de Heun:
#Para el eje de TE, se crea un arreglo de (240/x)+1 ceros en un principio,
#que luego se rellenara
eje_TEHeun=np.zeros(int(particiones+1))
#Se rellena el eje de TEHeun de la siguiente manera:
for i in range(len(eje_t)):
    if i==particiones:
        break
    #debido a la condicion inicial:
    if i>=0 and i<=(5*int(iteracionesmes)):
        eje_TEHeun[i]=1
    else:
        eje_TEHeun[i]=eje_TEHeun[i-1]+pasoHeun(eje_t[i-1],eje_TEHeun[i-1])

#Para graficar, se realiza lo siguiente:
blue_patch = mpatches.Patch(color="blue",label="Metodo de Euler")
red_patch = mpatches.Patch(color="red",label="Metodo de Heun")
plt.figure(figsize=(10,5))

#Como se busca comparar ambos metodos, se hace un grafico de la siguiente manera:
plt.plot(eje_t,eje_TEHeun,color="red")
plt.plot(eje_t,eje_TEEuler, color="blue")
plt.title("Metodo de Euler vs metodo de Heun")
plt.xlabel("t")
plt.ylabel("TE(t)")
plt.legend(handles=[red_patch,blue_patch])

plt.show()

#Y se calcula el error entre ambos graficos:
ErrorMetodos=np.linalg.norm(eje_TEHeun-eje_TEEuler)
print("Error en norma 2 entre ambos metodos:", ErrorMetodos)







