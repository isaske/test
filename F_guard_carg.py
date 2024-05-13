import json

# funcion Cargar Variables
def cargar_variables():
  variables = {}
  with open('variables.txt', 'r') as file:
    for line in file:
      # Buscar la primera aparición del signo igual "="
      index = line.find('=')
      # Si se encontró el signo igual
      if index != -1:
        # Separar la línea en clave y valor (todo antes del primer "=" es la clave, el resto es el valor)
        clave = line[:index].strip()
        valor = line[index + 1:].strip()
        # Asignar clave y valor al diccionario de variables
        variables[clave] = valor
  return variables


# Función para guardar variables
def guardar_variables(variables):
  # Leer el contenido actual del archivo
  with open('variables.txt', 'r') as file:
    lineas = file.readlines()

  # Modificar la línea que contiene la clave que se va a actualizar
  for i, linea in enumerate(lineas):
    # Separar la línea en clave y valor (maxsplit=1 para evitar cortar valores que contengan "=")
    clave_actual, valor_actual = linea.split("=", maxsplit=1)
    # Si la clave está en el diccionario de variables, actualizar el valor
    if clave_actual.strip() in variables:
      valor_nuevo = variables[clave_actual.strip()]
      # Reemplazar el valor actual con el nuevo valor
      lineas[i] = f"{clave_actual.strip()}={valor_nuevo}\n"

  # Escribir todas las variables nuevamente en el archivo
  with open('variables.txt', 'w') as file:
    for linea in lineas:
      file.write(linea)


# Cargar Variables
variables = cargar_variables()
tipMinRequerido = (variables['tipMinRequeridoSave'])
tipMinRequerido = int(tipMinRequerido)

variables = cargar_variables()
tipLimitUserTip = (variables['tipLimitUserTipSave'])
tipLimitUserTip = int(tipLimitUserTip)

variables = cargar_variables()
loopAnuncioSeg = (variables['autoTipSegSave'])
loopAnuncioSeg = int(loopAnuncioSeg)

variables = cargar_variables()
loopAnuncio = (variables['anuncioAuto'])

variables = cargar_variables()
welcomeText = (variables['welcomeTextSave'])

variables = cargar_variables()
tipstate = bool((variables['autoTipSave']))

variables = cargar_variables()
vipstate = (variables['vipStateSave'])

if tipstate:
  variables = cargar_variables()
  tipcantidad = (variables['cantidadTipSave'])
  variables = cargar_variables()
  tiptimerestaurar = (variables['tiempoTipSave'])
  tiptime = (variables['tiempoTipSave'])

with open("Json/danceFloorCoordenadas.json", "r") as json_file:
  danceFloorCoordenadas = json.load(json_file)

with open("Json/botspawnPosSave.json", "r") as json_file:
  botspawnPos = json.load(json_file)

with open("Json/warpsListaSave.json", "r") as json_file:
  warpsLista = json.load(json_file)

with open("Json/carcelListSave.json", "r") as json_file:
  carcelList = json.load(json_file)

with open("Json/inviteListSave.json", "r") as json_file:
  inviteList = json.load(json_file)
