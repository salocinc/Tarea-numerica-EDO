import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

#ecuacion: float,float,float -> arreglo de numpy de tamaño 2
#Recibe un t_n, un TE_n y un HW_n para retornar f(t_n,TE_n,HW_n)
def ecuacion(t_n,TE_n,HW_n):
    A=np.array([[0.1,0.04428],[-0.612,-0.1]])
    X=np.array([TE_n,HW_n])
    return A.dot(X)

#pasoEuler: float, float, float -> arreglo de numpy de tamaño 2
#Recibe (t_n,TE_n,HW_n) y retorna la multiplicacion de f(t_n,TE_n,HW_n)
#por h, que es el paso de discretizacion.
def pasoEuler(t_n,TE_n,HW_n):
    return ecuacion(t_n,TE_n,HW_n)*h

#pasoRK4: float,float, float -> arreglo de numpy de tamaño 2
#Recibe (t_n,TE_n,HW_n) y retorna el paso correspondiente segun
#el metodo de Runge Kutta a sumar.
def pasoRK4(t_n,TE_n,HW_n):
    g1=ecuacion(t_n,TE_n,HW_n)
    g2=ecuacion(t_n+(h/2.0),TE_n+(h/2.0)*g1[0],HW_n+(h/2.0)*g1[1])
    g3=ecuacion(t_n+(h/2.0),TE_n+(h/2.0)*g2[0],HW_n+(h/2.0)*g2[1])
    g4=ecuacion(t_n+h,TE_n+h*g3[0],HW_n+h*g3[1])
    return (h/6.0)*(g1+2*g2+2*g3+g4)

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
#Para el eje de X, se crea un arreglo de (240/x)+1 arreglos de ceros en
#un principio,que luego se rellenara:
eje_XEuler=np.zeros((int(particiones+1),2))
#Implementando la condicion inicial:
eje_XEuler[0]=np.array([1,-1])
#Se rellena el eje de TEEuler de la siguiente manera:
for i in range(len(eje_t)):
    if i==particiones:
        break
    else:
        eje_XEuler[i+1]=eje_XEuler[i]+pasoEuler(eje_t[i],eje_XEuler[i][0],eje_XEuler[i][1])

#Para el calculo mediante el metodo de Runge Kutta de orden 4:
#Para el eje de X, se crea un arreglo de (240/x)+1 arreglos de ceros en
#un principio,que luego se rellenara:
eje_XRK4=np.zeros((int(particiones+1),2))
#Implementando la condicion inicial:
eje_XRK4[0]=np.array([1,-1])
#Se rellena el eje de XRK4 de la siguiente manera:
for i in range(len(eje_t)):
    if i==particiones:
        break
    else:
        eje_XRK4[i+1]=eje_XRK4[i]+pasoRK4(eje_t[i],eje_XRK4[i][0],eje_XRK4[i][1])

#Como se busca comparar ambos metodos, se hace un grafico de la siguiente manera:
plt.figure(figsize=(10,5))
linea1,=plt.plot(eje_t,eje_XEuler[:,0],linestyle="--",color="red",label="TE(t) calculado con metodo de Euler")
linea2,=plt.plot(eje_t,eje_XEuler[:,1],color="red",label="HW(t) calculado con metodo de Euler")
linea3,=plt.plot(eje_t,eje_XRK4[:,0],linestyle="--",color="blue",label="TE(t) calculado con metodo RK orden 4")
linea4,=plt.plot(eje_t,eje_XRK4[:,1],color="blue",label="HW(t) calculado con metodo RK orden 4")
plt.title("Metodo de Euler vs metodo de Runge Kutta orden 4")
plt.xlabel("t")
plt.ylabel("X(t)")
leyenda=plt.legend(handles=[linea1,linea3,linea2,linea4])
ax = plt.gca().add_artist(leyenda)
plt.show()

#Y se calcula el error entre ambos metodos:
ErrorMetodos=np.linalg.norm(eje_XRK4-eje_XEuler)
print("Error en norma 2 entre ambos metodos:", ErrorMetodos)


#A continuacion, se escribe parte del script obtenido en la parte b,
#para obtener TE(t) a partir del modelo 1 con retraso.

#ecuacionHeun: float,float -> float
#Recibe un t_n y un TE_n para retornar f(t_n,TE_n)
def ecuacionHeun(t_n,TE_n):
    return (0.1*TE_n)-(0.16524*eje_TEHeun[int(t_n/h)-int(5*iteracionesmes)])

#pasoHeun: float,float -> float
#Recibe las coordenadas (t_n,TE_n) y multiplica f(t_n,TE_n)+f(t_n+h,TE_n1) por
#h y divide por 2 para realizar el cálculo mediante trapecios,
#donde TE_n1 es TE_n+1 calculada mediante el metodo de Euler progresivo
def pasoHeun(t_n,TE_n):
    TE_n1= TE_n+ecuacionHeun(t_n,TE_n)*h
    return (ecuacionHeun(t_n,TE_n)+ecuacionHeun(t_n+h,TE_n1))*h/2.0

#iteracionesmes sera la cantidad de iteraciones que hay en un mes.
iteracionesmes=1/deltat

#Para el calculo mediante el metodo de Heun:
#Para el eje de TE, se crea un arreglo de (240/x)+1 ceros en un principio,
#que luego se rellenara:
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

#Se grafican ambos graficos para compararlos:
plt.figure(figsize=(10,5))
TEXRK4,=plt.plot(eje_t,eje_XRK4[:,0],color="green",label="TE(t) calculado con metodo RK orden 4 (modelo 2)")
TEHeun,=plt.plot(eje_t,eje_TEHeun,color="k",label="TE(t) calculado con metodo de Heun (modelo 1)")
plt.title("TE(t) calculado con modelo 2 vs TE(t) calculado con modelo 1")
plt.xlabel("t")
plt.ylabel("TE(t)")
leyenda2=plt.legend(handles=[TEXRK4,TEHeun])
ax = plt.gca().add_artist(leyenda2)
plt.show()

#Y se calcula el error entre ambos metodos:
ErrorMetodos2=np.linalg.norm(eje_XRK4[:,0]-eje_TEHeun)
print("Error en norma 2 entre ambos metodos (con modelo 2 y modelo 1):", ErrorMetodos2)





