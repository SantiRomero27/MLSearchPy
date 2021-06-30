import requests
from bs4 import BeautifulSoup
from objeto_producto import *


# Función para buscar precios, arma el vector con todos los productos ordenados
def obtener_productos(parametro_busqueda):

    # Adapto el parametro
    parametro_adaptado1 = parametro_busqueda.replace(' ', '-') + '#D'
    parametro_adaptado2 = '[A:' + parametro_busqueda.replace(' ', '%20') + ']'
    parametro_final = parametro_adaptado1 + parametro_adaptado2

    # La pagina con la busqueda
    url = 'https://listado.mercadolibre.com.ar/' + parametro_final

    # Hago el request
    pagina = requests.get(url)

    # Hago la sopa (ya tengo todos los contenidos)
    sopa = BeautifulSoup(pagina.content, 'html.parser')

    # Obtengo los articulos
    articulos = sopa.find_all(
        'div', class_='ui-search-result__content-wrapper')

    # Variable auxiliar
    listado_productos = []

    # De cada uno de estos articulos, saco el titulo y el precio
    for articulo in articulos:
        titulo = articulo.find(
            'div', class_='ui-search-item__group ui-search-item__group--title').text
        precio = articulo.find(
            'span', class_='price-tag ui-search-price__part').text

        # Adapto el precio para poder utilizarlo
        precio = precio.replace('$', '')
        precio = precio.replace('.', '')
        precio = precio.replace(',', '.')
        precio = precio.split()[0]
        precio = float(precio)

        # Paso el producto al listado
        prod = Producto(titulo, precio)
        listado_productos.append(prod)

    return listado_productos


# Función para ordenar el vector de productos por precios (de menor a mayor)
def ordenar_precios(vector_productos):

    n = len(vector_productos)

    for i in range(n - 1):
        for j in range(i + 1, n):
            if vector_productos[i].precio > vector_productos[j].precio:
                vector_productos[i], vector_productos[j] = vector_productos[j], vector_productos[i]


# Función para crear una cadena y poder mostrar los productos
def llevar_cadena(registro_producto):
    cadena_registro = ''
    cadena_registro += '-' + registro_producto.titulo
    cadena_registro += ' ---> $' + str(registro_producto.precio) + '\n'

    return cadena_registro


# Función para obtener los datos del listado como cadena
def listado_a_cadena(listado_productos):

    # Primero, chequeamos como está el listado
    if len(listado_productos) >= 20:
        listado_productos = listado_productos[:20]

    elif len(listado_productos) == 0:
        return 'No se pudo encontrar nada'

    # Variable auxiliar
    cadena = ''

    # Ciclo
    for producto in listado_productos:
        cadena += llevar_cadena(producto)

    return cadena
