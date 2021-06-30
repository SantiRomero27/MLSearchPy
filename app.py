from tkinter import *
from funcionalidades import *
from requests.exceptions import ConnectionError
from PIL import ImageTk, Image


# Función del Botón para buscar
def boton_buscar():

    # Borro el contenido del widget (primero habilito)
    cuadro_texto.config(state='normal')
    cuadro_texto.delete(1.0, END)

    # Primero, obtenemos el dato
    dato = entry_var.get()

    # Hago la búsqueda (si hay internet)
    try:
        listado = obtener_productos(dato)

        # Ordeno el listado por precio
        ordenar_precios(listado)

        # Con los precios ordenados, los podemos mostrar
        listado_cadena = listado_a_cadena(listado)

        # Tenemos el listado, ponemos el texto, despues deshabilitamos
        cuadro_texto.config(state='normal')
        cuadro_texto.insert(END, listado_cadena)

        # Deshabilito
        cuadro_texto.config(state='disabled')

    except ConnectionError:
        label_error = Label(ventana, text='No hay Internet!', fg='red',
                            bg='#feff57', font=('calibri bold', 12))
        label_error.place(x=20, y=105)


# Creo la ventana
ventana = Tk()

# La configuro
ventana.resizable(False, False)
ventana.title('Buscador MercadoLibre')
ventana.geometry('1050x350')
ventana.config(bg='#feff57')

# Label de búsqueda
label_busqueda = Label(ventana, text='Buscá acá:', fg='blue',
                       font=('calibri bold', 15), bg='#feff57')
label_busqueda.place(x=30, y=10)

# Pongo el logo de MercadoLibre
foto = Image.open('mercadolibre.png')
ajustado = foto.resize((120, 90), Image.ANTIALIAS)

nueva_foto = ImageTk.PhotoImage(ajustado)

label_foto = Label(ventana, image=nueva_foto, bg='#feff57')
label_foto.place(x=15, y=230)

# Entry para buscar
entry_var = StringVar()

entry_busqueda = Entry(ventana, borderwidth=3,
                       bg='#e3e3e3', textvariable=entry_var)
entry_busqueda.place(x=13, y=40)

# Botón para mostrar resultados
boton = Button(ventana, text='Buscar', bd=3, cursor='hand2',
               bg='#9e9bfa', font=('calibri bold', 11), command=boton_buscar)
boton.place(x=50, y=65)

# Ponemos un cuadro de texto que nos va a mostrar los resultados listados de la busqueda
cuadro_texto = Text(ventana, borderwidth=3, cursor='hand1',
                    state='disabled', relief='ridge', font=('Calibri', 11))

cuadro_texto.config(width=124, height=18)
cuadro_texto.place(x=150, y=5)

# Configuro una barra de Scroll para el cuadro de texto
scroll_texto = Scrollbar(ventana, command=cuadro_texto.yview)
scroll_texto.pack(side=RIGHT, fill=Y)

# Seteo el Scrollbar para que funcione
cuadro_texto.config(yscrollcommand=scroll_texto.set)

# Mando el loop
ventana.mainloop()
