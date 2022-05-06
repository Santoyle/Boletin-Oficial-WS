# librerias
#from turtle import clear
import requests
import re
import awk
import sed
import os

os.chdir("C://Users//Santoyle//Downloads//66")

from urllib3._collections import HTTPHeaderDict
import pandas as pd
  
# api
URL = "https://timeline.boletinoficial.gob.ar/"


# Leer el archivo de clientes

script_path = os.path.abspath("C://Users//Santoyle//Downloads//8")
#script_dir = os.path.split(script_path)[0]
rel_path = "Clientes.csv"
abs_file_path = os.path.join(script_path, rel_path)
file1 = open(abs_file_path, 'r')
Lines = file1.readlines()

count = 0
for line in Lines:
    count += 1
print('***********************************')
print("Cantidad de Clientes a procesar:", count)
print('***********************************')

df = pd.DataFrame(columns = ['dni','empresa'])

#Procesamos cliente por cliente
for line in Lines:
    print('**************************************************')

    # parametria
    PARAMS = HTTPHeaderDict()
    PARAMS.add('searchtext_type','person')
    personaAux = line
    PARAMS.add('searchtext_person',personaAux)
  
    # enviando request a la API
    r = requests.post(url = URL, data = PARAMS)
  
    # parseando data y dejando solo los nombres de las empresas asociadas
    data = r.text
    regexA='denominacion_original": "\w*[\w ]*[A-Z.]*'
    parseadoA = re.findall(regexA, data)

    # Si el cliente no tiene empresas estimamos que no existe, caso contrario else ok
    sinEmpresas='.*\[].*'
    if re.match(sinEmpresas, str(parseadoA)):
        print('El cliente ', personaAux, ' no tiene empresas asociadas.' )
    else:
        for i in parseadoA:
            df.loc[len(df)] = [personaAux, i]
        
        print('El cliente ', personaAux, ' tiene las siguientes empresas asociadas: ')
        print(parseadoA)

        regexLimpieza=':".*,'
        guardar = re.findall(regexLimpieza, str(parseadoA))

df['dni'].replace('\n', '', regex=True, inplace=True)
df['empresa'].replace('denominacion_original": "', '', regex=True, inplace=True)

df.to_csv('C://Users//Santoyle//Downloads//8//ResultadosDNI.csv')
