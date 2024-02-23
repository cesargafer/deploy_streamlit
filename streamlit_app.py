


import streamlit as st

import json
from firebase_admin import initialize_app
import pandas as pd
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore


import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account

import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.C


from firebase_admin import initialize_app
from firebase_admin import credentials, firestore



#@st.cache_resource(hash_funcs={credentials.Certificate: id})
#def initialize_firestore():
#    try:
#        initialize_app(credentials.Certificate(credenciales_json))
#    except ValueError:
#        # La aplicación ya está inicializada, maneja el error según sea necesario
#        pass
#
#    # No necesitamos pasar las credenciales al cliente de Firestore
#    # Inicializar el cliente de Firestore
#    return firestore.client()

# Obtener el cliente de Firestore
#db = initialize_firestore()

# Inicializar Firebase Admin SDK
try:
    initialize_app(credentials.Certificate("reto-netflix-a4e46-firebase-adminsdk-l5d20-32210b41c7.json"))
except ValueError:
    # La aplicación ya está inicializada, maneja el error según sea necesario
    pass

# Obtener el cliente de Firestore
db = firestore.client()


##
##

# Checkbox para visualizar todos los filmes recuperados
if st.sidebar.checkbox("Mostrar Todos los Filmes"):
    # Obtener todos los filmes de la base de datos
    todos_los_filmes = db.collection(u'peliculas').get()

    # Crear una lista para almacenar los datos de todos los filmes
    data = []

    # Recorrer todos los filmes y obtener sus datos
    for filme in todos_los_filmes:
        filme_data = filme.to_dict()
        data.append(filme_data)

    # Crear un DataFrame a partir de los datos obtenidos
    df_todos_los_filmes = pd.DataFrame(data)

    # Mostrar todos los filmes en forma de tabla
    st.header("Todos los filmes:")
    st.write(df_todos_los_filmes)

##

# Campo de texto para ingresar el título de la película a buscar
titulo_busqueda = st.sidebar.text_input("Buscar por Título")

# Botón de comando para realizar la búsqueda
if st.sidebar.button("Buscar", key="buscar_button"):
    # Convertir el título de búsqueda a minúsculas
    titulo_busqueda = titulo_busqueda.lower()

    # Filtrar los filmes que contengan el título de búsqueda (sin importar mayúsculas o minúsculas)
    filmes_coincidentes = [filme.to_dict() for filme in db.collection(u'peliculas').get() if titulo_busqueda in filme.to_dict()['name'].lower()]



    # Mostrar los datos en una tabla si se encontraron filmes coincidentes
    if filmes_coincidentes:
        # Mostrar el total de registros encontrados
        st.write(f"Total de filmes mostrados: {len(filmes_coincidentes)}")
        df_filmes_coincidentes = pd.DataFrame(filmes_coincidentes)
        st.write(df_filmes_coincidentes)
    else:
        st.write("No se encontraron filmes con ese título.")



##

# Obtener todos los filmes de la base de datos
todos_los_filmes = db.collection(u'peliculas').get()

    # Crear una lista para almacenar los datos de todos los filmes
data = []

    # Recorrer todos los filmes y obtener sus datos
for filme in todos_los_filmes:
    filme_data = filme.to_dict()
    data.append(filme_data)

    # Crear un DataFrame a partir de los datos obtenidos
df_todos_los_filmes_ = pd.DataFrame(data)

# 1. Crear el componente selectbox en el sidebar para cargar la columna 'director'
directores = df_todos_los_filmes_['director'].unique()
selected_director = st.sidebar.selectbox("Seleccionar Director", directores)

# 2. Crear el botón de comando para iniciar la búsqueda
if st.sidebar.button("Buscar por Director", key="buscar_button_"):
    # 3. Definir una función que filtre los filmes realizados por el director seleccionado
    filmes_director = df_todos_los_filmes_[df_todos_los_filmes_['director'] == selected_director]

    # 4. Mostrar el total de filmes encontrados y la tabla con los resultados
    st.write(f'Total de filmes encontrados para el director "{selected_director}": {len(filmes_director)}')
    st.write(filmes_director)


##
import streamlit as st
from firebase_admin import firestore

# Función para insertar un nuevo filme en Firestore
def insertar_filme(nombre, director, genero, compañia):
    # Crear un documento en la colección 'peliculas' con los datos proporcionados
    db.collection(u'peliculas').add({
        u'name': nombre,
        u'director': director,
        u'genre': genero,
        u'company': compañia
    })
    st.success("El filme se ha insertado correctamente en la base de datos.")
    # Limpiar los campos del formulario después de insertar el filme
    nombre_input.text_input = ""
    director_input.text_input = ""
    genero_select.selectbox = ""
    compañia_input.text_input = ""

# Interfaz de Streamlit
st.sidebar.title("Agregar Nuevo Filme")

# Crear contenedores para los controles del formulario
form_container = st.sidebar.beta_container()

# Controles para ingresar los datos del nuevo filme
with form_container:
    st.subheader("Ingrese los datos del nuevo filme")
    nombre_input = st.text_input("Nombre del Filme")
    director_input = st.text_input("Director")
    genero_select = st.selectbox("Género", ["Acción", "Comedia", "Drama", "Ciencia Ficción", "Suspenso", "Animación", "Documental"])
    compañia_input = st.text_input("Compañía Productora")
    submit_button = st.form_submit_button("Insertar Filme")

# Botón para insertar el nuevo filme
if submit_button:
    # Validar que se hayan ingresado todos los datos
    if nombre_input.strip() and director_input.strip() and genero_select.strip() and compañia_input.strip():
        # Llamar a la función para insertar el nuevo filme en Firestore
        insertar_filme(nombre_input, director_input, genero_select, compañia_input)
    else:
        st.warning("Por favor ingresa todos los datos del filme.")

