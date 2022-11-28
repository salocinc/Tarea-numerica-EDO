#Se importan las actividades b y c:
import Numericab
import Numericac

#IMPORTANTE:
#Los deltat en cada archivo tienen que valer 0.005, ya que para este valor se
#puede calcular el valor de P barra: para delta ts mas chicos, solo se puede
#calcular "al ojo", ya que la resolucion de los resultados disminuye con delta
#t mas grandes y al aumentar el rango de valores admitidos para localizar
#los ceros, se cuelan muchos valores no relacionados.

#calculador de periodo: arreglo de numpy -> float
#calcula el periodo de oscilacion aproximado en los metodos de la actividad b
def calculadorb(ejey,nombremetodo):
    ceros=[]
    for i in range(int(Numericab.particiones+1)):
        #Se busca guardar para que valores en el eje t, la funcion TE
        #se acerca a 0
        if ejey[i] < 0.001 and ejey[i]>-0.001:
            ceros.append(Numericab.eje_t[i])
    #se eligen las posiciones 21 y 0, ya que son las posiciones del inicio
    #y termino de la primera oscilacion. Esto se dedujo experimentalmente
    #imprimiendo el valor de ceros
    Pbarra=ceros[21]-ceros[0]
    print("El periodo aproximado en el modelo 1 con retraso con el metodo de",nombremetodo,"es:", Pbarra)
    
calculadorb(Numericab.eje_TEEuler,"Euler")
calculadorb(Numericab.eje_TEHeun,"Heun")

#--------------------------------------------------------------------
#calculador de periodo: arreglo de numpy -> float
#calcula el periodo de oscilacion aproximado en los metodos de la actividad c
def calculadorc(ejey,nombremetodo):
    ceros=[]
    for i in range(int(Numericac.particiones+1)):
        #Se busca guardar para que valores en el eje t, la funcion TE
        #se acerca a 0
        if ejey[i] < 0.001 and ejey[i]>-0.001:
            ceros.append(Numericac.eje_t[i])
    #se eligen las posiciones 4 y 0, ya que son las posiciones del inicio
    #y termino de la primera oscilacion. Esto se dedujo experimentalmente
    #imprimiendo el valor de ceros
    Pbarra=ceros[4]-ceros[0]
    print("El periodo aproximado en el modelo 2 con el metodo de",nombremetodo,"es:", Pbarra)
    
calculadorc(Numericac.eje_XEuler[:,0],"Euler")
calculadorc(Numericac.eje_XRK4[:,0],"RK4")
