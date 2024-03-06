import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def crecimiento2(img,seed):
    etiquetas=np.zeros_like(img) #genera una matriz de ceros con la misma forma y tipo de dato que la imagen
    n=40 #umbralización
    region=[seed] #Lista que almacena coordenados de los pixeles que estan en ala región
    nivel_gray_seed=img[seed[0],seed[1]]#obtiene el nivel de inteisdad del pixel en la posic+on de la semilla
    #Para que le de referencia si esa región se usa o no

    coordenadas=[] #almacena las coordenadas de los pixeles en la región

    while region: #mientras la región no este vacia
        x,y=region.pop(0) #extrae las coordenadas del primer elemento de la lista

        if 0 <= x < img.shape[0] and 0 <= y < img.shape[1] and etiquetas[x, y] == 0: #verificar si las coordenadas entan dentro del limtie de la imagen y que no haya sido etiquetado
            diferencia=np.abs(img[x,y]-nivel_gray_seed) #se calcula la diferencia entre      nivel gris del pixel actual con la semilla
            if diferencia <=n: #rango permitido
                etiquetas[x,y]=255
                coordenadas.append((x,y)) #se añaden coordenadas de pixeles vecinos a ls region
                region.append((x+1,y))
                region.append((x-1,y))
                region.append((x,y+1))
                region.append((x,y-1))

    return etiquetas,coordenadas


def crecimiento(img,seed):
    etiquetas=np.zeros_like(img) #genera una matriz de ceros con la misma forma y tipo de dato que la imagen
    n=80 #umbralización
    region=[seed] #Lista que almacena coordenados de los pixeles que estan en ala región
    nivel_gray_seed=img[seed[0],seed[1]]#obtiene el nivel de inteisdad del pixel en la posic+on de la semilla
    #Para que le de referencia si esa región se usa o no
    
    coordenadas=[] #almacena las coordenadas de los pixeles en la región

    while region: #mientras la región no este vacia 
        x,y=region.pop(0) #extrae las coordenadas del primer elemento de la lista

        if 0 <= x < img.shape[0] and 0 <= y < img.shape[1] and etiquetas[x, y] == 0: #verificar si las coordenadas entan dentro del limtie de la imagen y que no haya sido etiquetado
            diferencia=np.abs(img[x,y]-nivel_gray_seed) #se calcula la diferencia entre el nivel gris del pixel actual con la semilla
            if diferencia <=n: #rango permitido
                etiquetas[x,y]=255
                coordenadas.append((x,y)) #se añaden coordenadas de pixeles vecinos a ls region
                region.append((x+1,y))
                region.append((x-1,y)) 
                region.append((x,y+1))
                region.append((x,y-1))



    return etiquetas,coordenadas


def imagen():
    
    file_path = filedialog.askopenfilename(title="Seleccionar imagen",
                                           filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        img = cv.imread(file_path, 0)
        pandm(img)

def pandm(img):

    #------Quitar ruido-sal y pimienta
    img_ruido=cv.medianBlur(img,5)


    #-------Imagen umbralizada
    img_umbralizada=cv.threshold(img_ruido,70,255,cv.THRESH_BINARY)[1]

    #Analizar de que lado esta el seno 
    altura, ancho = img_umbralizada.shape
    mitad_ancho = ancho // 2

    #aplicamos slicing para dividir la imagen
    mitad_izquierda = img_umbralizada[:, :mitad_ancho]
    mitad_derecha = img_umbralizada[:, mitad_ancho:]

    #contar cuantos pixeles de la imagen, tanto lado izquiero como derecho,no son 0
    pixeles_blancos_izquierda = cv.countNonZero(mitad_izquierda)
    pixeles_blancos_derecha = cv.countNonZero(mitad_derecha)

    #calculado esto se pone condicionales para aplicar el respectivo procesamiento de imagenes
    if pixeles_blancos_izquierda > pixeles_blancos_derecha:
        print("La mitad izquierda tiene más píxeles blancos.")

        #primero vamos a cortar la imagen en el musculo pectoral, ya que son datos inecesarios con crecimiento de regiones

        seed_inicial=(68, 68) #definimos donde queremos que se haga el crecimiento

        #Utilizamos la función para hacerlo
        resultado_crecimiento1, coordenadas_region = crecimiento(img_ruido, seed_inicial)

        #crea una mascara de la regiión segmentada para poder invertir el resultado
        mascara_region=np.zeros_like(img_ruido)

        for coord in coordenadas_region: #crear mascara en las coordenadas de la región extraida
            mascara_region[coord[0],coord[1]]=255

        #invertimos mascara
        mascara_invet=cv.bitwise_not(mascara_region)

        #aplicamos la mascara invertida a la imagen original
        img_resultante1=cv.bitwise_and(img_ruido,img_ruido,mask=mascara_invet)
        img_resultante1sf=cv.bitwise_and(img_ruido,img_ruido,mask=mascara_invet)#aplica mascara a la imagen

        #Coordenadas del punto de interés
        coordenadas_punto_interes = (75, 276)
        # Aplicar el filtro para recortar la imagen y poner solo la parte que nos interesa
        img_resultante1[img_resultante1 <= 148] = 0
        img_filtrada_punto_interes1 =img_resultante1

        #imagen del filtro umbralizada
        img_umbralizada1 = cv.threshold(img_filtrada_punto_interes1, 70, 255, cv.THRESH_BINARY)[1]

        #Utilizamos la función para hacerlo
        seed_inicial=(250, 50) #definimos donde queremos que se haga el crecimiento

        #Utilizamos la función para hacerlo
        resultado_crecimiento12, coordenadas_region = crecimiento2(img_filtrada_punto_interes1, seed_inicial)

        img_ruido_tk = ImageTk.PhotoImage(Image.fromarray(img_ruido))  #guardamos las imagenes de cada resultado
        resultado_crecimiento_tk1 = ImageTk.PhotoImage(Image.fromarray(resultado_crecimiento1))
        img_resultante1fn = ImageTk.PhotoImage(Image.fromarray(img_resultante1sf))
        img_umbralizada_tk1 = ImageTk.PhotoImage(Image.fromarray(img_umbralizada1))
        img_filtrada_tk1 = ImageTk.PhotoImage(Image.fromarray(img_filtrada_punto_interes1))
        img_crecimientofinal_tk1 = ImageTk.PhotoImage(Image.fromarray(resultado_crecimiento12))

        # Mostrar imágenes en la interfaz
        label_titulo_img_ruido1.config(text="Imagen Original (Ruido)")
        label_img_ruido1.config(image=img_ruido_tk)
        label_img_ruido1.image = img_ruido_tk
    
        label_titulo_crecimiento1.config(text="Resultado del Crecimiento de Regiones-Quitando musculo pectoral")
        label_crecimiento1.config(image=resultado_crecimiento_tk1)
        label_crecimiento1.image = resultado_crecimiento_tk1

    
        label_titulo_img_resultante1fn.config(text="Imagen Resultante después de la mascara")
        label_img_resultante1fn.config(image=img_resultante1fn)
        label_img_resultante1fn.image = img_resultante1fn



        label_titulo_umg_umbralizada1.config(text="Imagen umbralizada")
        label_umg_umbralizada1.config(image=img_umbralizada_tk1)
        label_umg_umbralizada1.image = img_umbralizada_tk1


        label_titulo_img_filtrada1.config(text="Imagen Umbralizada-Después del filtro")
        label_img_filtrada1.config(image=img_filtrada_tk1)
        label_img_filtrada1.image = img_filtrada_tk1

        label_titulo_img_final.config(text="Imagen Final")
        label_img_final.config(image=img_crecimientofinal_tk1)
        label_img_final.image = img_crecimientofinal_tk1



    else:
        print("La mitad izquierda tiene más píxeles blancos.")

        #primero vamos a cortar la imagen en el musculo pectoral, ya que son datos inecesarios con crecimiento de regiones

        seed_inicial=(101, 192) #definimos donde queremos que se haga el crecimiento

        #Utilizamos la función para hacerlo
        resultado_crecimiento1, coordenadas_region = crecimiento(img_ruido, seed_inicial)

        #crea una mascara de la regiión segmentada para poder invertir el resultado
        mascara_region=np.zeros_like(img_ruido)

        for coord in coordenadas_region:
            mascara_region[coord[0],coord[1]]=255

        #invertimos mascara
        mascara_invet=cv.bitwise_not(mascara_region)

        #aplicamos la mascara invertida a la imagen original
        img_resultante1=cv.bitwise_and(img_ruido,img_ruido,mask=mascara_invet)
        img_resultante1sf=cv.bitwise_and(img_ruido,img_ruido,mask=mascara_invet)

        #Coordenadas del punto de interés
        coordenadas_punto_interes = (75, 276)
        # Aplicar el filtro para recortar la imagen y poner solo la parte que nos interesa
        img_resultante1[img_resultante1 <= 148] = 0
        img_filtrada_punto_interes1 =img_resultante1

        #imagen del filtro umbralizada
        img_umbralizada1 = cv.threshold(img_filtrada_punto_interes1, 70, 255, cv.THRESH_BINARY)[1]

        #Utilizamos la función para hacerlo
        seed_inicial=(275, 169) #definimos donde queremos que se haga el crecimiento

        #Utilizamos la función para hacerlo
        resultado_crecimiento12, coordenadas_region = crecimiento2(img_filtrada_punto_interes1, seed_inicial)

        img_ruido_tk = ImageTk.PhotoImage(Image.fromarray(img_ruido))
        resultado_crecimiento_tk1 = ImageTk.PhotoImage(Image.fromarray(resultado_crecimiento1))
        img_resultante1fn = ImageTk.PhotoImage(Image.fromarray(img_resultante1sf))
        img_umbralizada_tk1 = ImageTk.PhotoImage(Image.fromarray(img_umbralizada1))
        img_filtrada_tk1 = ImageTk.PhotoImage(Image.fromarray(img_filtrada_punto_interes1))
        img_crecimientofinal_tk1 = ImageTk.PhotoImage(Image.fromarray(resultado_crecimiento12))

        # Mostrar imágenes en la interfaz
        label_titulo_img_ruido1.config(text="Imagen Original (Ruido)")
        label_img_ruido1.config(image=img_ruido_tk)
        label_img_ruido1.image = img_ruido_tk
    
        label_titulo_crecimiento1.config(text="Resultado del Crecimiento de Regiones-Quitando musculo pectoral")
        label_crecimiento1.config(image=resultado_crecimiento_tk1)
        label_crecimiento1.image = resultado_crecimiento_tk1

    
        label_titulo_img_resultante1fn.config(text="Imagen Resultante después de la mascara")
        label_img_resultante1fn.config(image=img_resultante1fn)
        label_img_resultante1fn.image = img_resultante1fn


        label_titulo_umg_umbralizada1.config(text="Imagen Umbralizada-Después del filtro")
        label_umg_umbralizada1.config(image=img_umbralizada_tk1)
        label_umg_umbralizada1.image = img_umbralizada_tk1


        label_titulo_img_filtrada1.config(text="Imagen despues del filtro")
        label_img_filtrada1.config(image=img_filtrada_tk1)
        label_img_filtrada1.image = img_filtrada_tk1

        label_titulo_img_final.config(text="Imagen Final")
        label_img_final.config(image=img_crecimientofinal_tk1)
        label_img_final.image = img_crecimientofinal_tk1




app = tk.Tk()
app.title("Aplicación de Crecimiento de Regiones")

# Botón para cargar la imagen
btn_cargar_imagen = tk.Button(app, text="Cargar Imagen", command=imagen)
btn_cargar_imagen.grid(row=2, column=0, pady=10)

# Labels para mostrar imágenes
label_titulo_umg_umbralizada1 = tk.Label(app, font=("Helvetica", 12, "bold"))
label_titulo_umg_umbralizada1.grid(row=1, column=0, pady=5)
label_umg_umbralizada1 = tk.Label(app)
label_umg_umbralizada1.grid(row=1, column=1, pady=10)

label_titulo_img_filtrada1 = tk.Label(app, font=("Helvetica", 12, "bold"))
label_titulo_img_filtrada1.grid(row=1, column=2, pady=5)
label_img_filtrada1 = tk.Label(app)
label_img_filtrada1.grid(row=1, column=3, pady=10)

label_titulo_img_final = tk.Label(app, font=("Helvetica", 12, "bold"))
label_titulo_img_final.grid(row=1, column=4, pady=5)
label_img_final = tk.Label(app)
label_img_final.grid(row=1, column=5, pady=10)


# Labels for the first row of images
label_titulo_img_ruido1 = tk.Label(app, font=("Helvetica", 12, "bold"))
label_titulo_img_ruido1.grid(row=0, column=0, pady=5)
label_img_ruido1 = tk.Label(app)
label_img_ruido1.grid(row=0, column=1, pady=10)

label_titulo_crecimiento1 = tk.Label(app, font=("Helvetica", 12, "bold"))
label_titulo_crecimiento1.grid(row=0, column=2, pady=5)
label_crecimiento1 = tk.Label(app)
label_crecimiento1.grid(row=0, column=3, pady=10)

label_titulo_img_resultante1fn = tk.Label(app, font=("Helvetica", 12, "bold"))
label_titulo_img_resultante1fn.grid(row=0, column=4, pady=5)
label_img_resultante1fn = tk.Label(app)
label_img_resultante1fn.grid(row=0, column=5, pady=10)


# Variable global para almacenar las coordenadas de la región
coordenadas_region = []

# Ejecutar la aplicación
app.mainloop()