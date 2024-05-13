#🤍♥️
#from highrise import BaseBot, Position
import asyncio
import random
import time
import requests
import json

#from asyncio import run as arun
from asyncio import run

#from highrise.models import SessionMetadata, User
from highrise import (
    BaseBot,
    Item,
    Position,
    SessionMetadata,
    User,
    __main__,
)
from highrise.models import *
from global_variables import *
from F_guard_carg import *


class BotDefinition:

  def __init__(self, bot, room_id, api_token):
    self.bot = bot
    self.room_id = room_id
    self.api_token = api_token
    
def enter_user_carcel(user_id, tiempo_var, userName):
  global carcelList
  carcelList[user_id] = {"tiempo": tiempo_var, "nombre": userName}
  with open("Json/carcelListSave.json", "w") as json_file:
    json.dump(carcelList, json_file)

async def com_summon(self: BaseBot, user, message: str) -> None:
  if user.username == owner_name or user.username in adminsList:
    partes = message.split()
    mi_id = user.id
    if len(partes) == 1:
      if user.username == owner_name or user.username in adminsList:
        await self.highrise.send_whisper(
            user.id, "\n/summon @usuario - para atraer un usuario a ti.\n/summon all - para traer a todos a ti.")
        return
      else:
        await self.highrise.send_whisper(
          user.id, "\n/summon @usuario - para atraer un usuario a ti.")
        return
    elif len(partes) >= 2:
      
      if partes[1] == "all":
        room_users = (await self.highrise.get_room_users()).content
        detector = False
        miPos =[]
        for usr, pos in room_users:
          if usr.id == mi_id:
            detector = True
            miPos = pos
            if isinstance(pos, Position):
              pass
            else:
              await self.highrise.send_whisper(
                user.id, "no puedes usar este comando sentado.")
        if detector:
          for usr, pos in room_users:
            if usr.username != user.username and usr.username != bot_name:
              try:
                await self.highrise.teleport(usr.id, miPos)
              except:
                pass
      else:
        name = message.split("@")
        if len(name) == 2:
          splitName = name[1].strip()
          room_users = (await self.highrise.get_room_users()).content
          detector = False
          miPos =[]
          for usr, pos in room_users:
            if usr.id == mi_id:
              detector = True
              miPos = pos
              if isinstance(pos, Position):
                pass
              else:
                await self.highrise.send_whisper(
                  user.id, "no puedes usar este comando sentado.")
          if detector:
            detector = False
            for usr, pos in room_users:
              if usr.username == splitName:
                detector = True
                try:
                  await self.highrise.teleport(usr.id, miPos)
                except:
                  pass
          if not detector:
            await self.highrise.send_whisper(
              user.id, "usuario no está en la sala.")
  else:
    await self.highrise.send_whisper(
      user.id, "no puedes usar este comando.")


async def com_emote(self: BaseBot, user, message: str) -> None:
  if user.username == owner_name or user.username in adminsList or user.username in modsList or user.username in vipList:
    partes = message.split()
    if len(partes) == 1:
      if user.username == owner_name or user.username in adminsList or user.username in modsList:
        await self.highrise.send_whisper(
            user.id, "\n/emote @usuario [emote] - para hacer bailar a un usuario.\n/emote all [emote] para activar el emote a todos en la sala.\n/emote list - para ver la lista de emotes.")
        return
      if user.username in vipList:
        await self.highrise.send_whisper(
            user.id, "\n/emote @usuario [emote] - para hacer bailar a un usuario.")
        return
      else:
        await self.highrise.send_whisper(
            user.id, "necesitas rango VIP para usar este comando.")
        return
    elif partes[1] == "all":
      return
    if len(partes) == 3:
      emote_name = partes[2].strip()
      name = message.split("@")
      if len(name) == 2:
        splitName = name[1].strip()
        nombre_usuario2 = splitName.split(" ")[0]
        if user.username in vipList:
          if not (user.username == owner_name or user.username in adminsList
            or user.username in modsList):
            if nombre_usuario2 == owner_name or nombre_usuario2 in adminsList or nombre_usuario2 in modsList:
              await self.highrise.send_whisper(user.id, "no puedes usarlo en este usuario.")
              return
        user_id = ""
        room_users = (await self.highrise.get_room_users()).content
        
        for room_user, _ in room_users:
          if room_user.username == nombre_usuario2:
            user_id = room_user.id
        if user_id in dancing_users:
          dancing_users[user_id]["status"] = False
        tiempoReset = 0
        emote_id = ""
        detector = False
        if emote_name in listReset:
          detector = True
          emote_id = listReset[emote_name]['id']
          tiempoReset = listReset[emote_name]['tiempo']
        if not detector:
          await self.highrise.send_whisper(user.id, "Emote no existe")
          return
        
        try:
          await self.highrise.send_emote(emote_id, user_id)
          await asyncio.sleep(tiempoReset)

          for user_info in room_users:
            user_id = user_info[0].id

            if user_id in dancing_users:
              dancing_users[user_id]["status"] = True
              dancing_users[user_id]["tiempo"] = 0
        except:
          pass
      else:
        if user.username == owner_name or user.username in adminsList or user.username in modsList:
          await self.highrise.send_whisper(
              user.id, "\n/emote @usuario [emote] - para hacer bailar a un usuario.\n/emote all [emote] para activar el emote a todos en la sala.\n/emote list - para ver la lista de emotes.")
          return
    else:
      if user.username == owner_name or user.username in adminsList or user.username in modsList:
        await self.highrise.send_whisper(
            user.id, "\n/emote @usuario [emote] - para hacer bailar a un usuario.\n/emote all [emote] para activar el emote a todos en la sala.\n/emote list - para ver la lista de emotes.")
        return
      else:
        await self.highrise.send_whisper(
            user.id, "\n/emote @usuario [emote] - para hacer bailar a un usuario.")
        return
      
  else:
    await self.highrise.send_whisper(
        user.id, "necesitas rango VIP para usar este comando.")
    return


async def com_heart(self: BaseBot, user, message: str) -> None:
  if user.username == owner_name or user.username in adminsList or user.username in modsList or user.username in vipList:
    partes = message.split()
    if len(partes) == 1:
      if user.username == owner_name or user.username in adminsList or user.username in modsList:
        await self.highrise.send_whisper(
            user.id, "\n/heart @user [1-50](opcional) - para enviar corazones a un usuario.\n/heart all - para enviar corazones a todos.")
        return
      if user.username in vipList:
        await self.highrise.send_whisper(
            user.id, "\n/heart @user [1-50](opcional) - para enviar corazones a un usuarios.")
        return
      else:
        await self.highrise.send_whisper(
            user.id, "necesitas rango VIP para usar este comando.")
        return
        
    elif len(partes) >= 2:
      if partes[1] == "all":
        if user.username in vipList:
          if not user.username == owner_name and not user.username in adminsList and not user.username in modsList:
            await self.highrise.send_whisper(
              user.id, "\n/heart @user [1-50](opcional) - para enviar corazones a un usuarios.")
            return
        await self.highrise.send_whisper(user.id, "Enviando corazones a todos!")
        room_users = (await self.highrise.get_room_users()).content
        for i in range(4):
          for room_user, _ in room_users:
            if not room_user.id == bot_id:
                try:
                  await self.highrise.react("heart", room_user.id)
                except:
                  pass
                await asyncio.sleep(0.1)
        return
      else:
        name = message.split("@")
        cantidad = 1
        if len(name) == 2:
          if len(partes) == 3:
            test_cantidad = partes[2]
            if test_cantidad.isdigit():
              cantidad = int(test_cantidad)
              if cantidad <= 1:
                cantidad = 1
              if cantidad >= 50:
                cantidad = 50

          splitName = name[1].strip()
          nombre_usuario2 = splitName.split(" ")[0]
          room_users = (await self.highrise.get_room_users()).content
          for room_user, _ in room_users:
            if room_user.username == nombre_usuario2:
              user_id = room_user.id
              for i in range(cantidad):
                try:
                  await self.highrise.react("heart", user_id)
                except:
                  pass
                await asyncio.sleep(0.1)
        else:
          if user.username == owner_name or user.username in adminsList or user.username in modsList:
            await self.highrise.send_whisper(
                user.id, "\n/heart @user [1-50](opcional) - para enviar corazones a un usuario.\n/heart all - para enviar corazones a todos.")
            return
          if user.username in vipList:
            await self.highrise.send_whisper(
                user.id, "\n/heart @user [1-50](opcional) - para enviar corazones a un usuarios.")
            return
  else:
    await self.highrise.send_whisper(
        user.id, "necesitas rango VIP para usar este comando.")
    return


async def com_emote_list(self: BaseBot, user, message: str) -> None:
  emote_nombres = list(listReset.keys())  # Obtiene una lista de nombres de emotes
  emote_nombres.reverse() 
  # Divide la lista de nombres en sublistas de tamaño 15
  sublistas_emotes = [emote_nombres[i:i+20] for i in range(0, len(emote_nombres), 20)]

  for sublist in sublistas_emotes:
      # Convierte la lista de nombres de emotes en una cadena separada por comas
      nombres_emotes = ', '.join(sublist)
      # Envía la cadena de nombres de emotes por susurro al usuario
      await self.highrise.send_whisper(user.id, nombres_emotes)


async def com_invite(self: BaseBot, user, message: str) -> None:
  if user.username == owner_name or user.username in adminsList:
    partes = message.split()
    cantidad = len(inviteList)
    if len(partes) == 1:
      await self.highrise.send_whisper(
          user.id,
          "\n/invite all - para invitar a la sala a todos los usuarios suscritos.\n/invite [mensaje] - para enviar un mensaje a todos los usuarios suscritos."
      )
      await self.highrise.send_whisper(
          user.id,
          "\nno abusar de este comando.\nlos usuarios se pueden suscribir con /sub y desuscribir con /unsub"
      )
      return
    if partes[1] == "all":   
      await self.highrise.send_whisper( user.id, f"se enviará invitaciones a {cantidad} usuarios suscritos.")
      for user_id in inviteList:
        __id = f"1_on_1:{bot_id}:{user_id}"
        __idx = f"1_on_1:{user_id}:{bot_id}"
        try:
          await self.highrise.send_message(__id, "Join Room", "invite", room_id)
          await self.highrise.send_message(__id, "\n/unsub para dejar de recibir invitaciones.")
        except:
          try:
            await self.highrise.send_message(__idx, "Join Room", "invite",
                                            room_id)
            await self.highrise.send_message(__idx, "\n/unsub para dejar de recibir invitaciones.")
          except:
            pass

      await self.highrise.send_whisper( user.id, f"invitaciones enviadas con exito!")

    else: 
      mensaje = ' '.join(partes[1:])
      await self.highrise.send_whisper( user.id, f"se enviará el mensaje a {cantidad} usuarios suscritos.")
      for user_id in inviteList:
        __id = f"1_on_1:{bot_id}:{user_id}"
        __idx = f"1_on_1:{user_id}:{bot_id}"
        try:
          await self.highrise.send_message(__id, mensaje)
          await self.highrise.send_message(__id, "\n/unsub para dejar de recibir mensajes.")
        except:
          try:
            await self.highrise.send_message(__idx, mensaje)
            await self.highrise.send_message(__idx, "\n/unsub para dejar de recibir mensajes.")
          except:
            pass

      await self.highrise.send_whisper( user.id, f"mensaje enviado con exito!")


async def com_setjail(self: BaseBot, user, message: str) -> None:
  global carcelPos
  if user.username == owner_name or user.username in adminsList:
    room_users = (await self.highrise.get_room_users()).content
    user_id = user.id
    for usr, pos in room_users:  #Cambiado user a usr para evitar sobrescribir la variable user
      if usr.id == user_id:
        carcelPos = [pos.x, pos.y, pos.z]
        guardar = {'carcelPosSave': carcelPos}
        guardar_variables(guardar)
        await self.highrise.chat("Posicion de la cárcel actualizada. 👮")


async def com_jail(self: BaseBot, user, message: str) -> None:
  global carcelAuto, carcelList
  if user.username == owner_name or user.username in adminsList:
    mi_id = user.id
    if message == "/jail auto":
      if carcelAuto == False:
        carcelAuto = True
        await self.highrise.chat("Cárcel automática activada")
        return
      else:
        carcelAuto = False
        await self.highrise.chat("Cárcel automática desactivada")
      return

    if message == "/jail free":
      room_users = (await self.highrise.get_room_users()).content
      user_ids_in_room = {user_info[0].id for user_info in room_users}
      carcelList_keys = list(carcelList.keys())
      detectar = any(user_id in user_ids_in_room
                     for user_id in carcelList_keys)
      

      if detectar:
        await self.highrise.chat("¡Todos libres! 👮👍")
      else:
        await self.highrise.chat("No hay nadie en la cárcel para liberar 👮")
        return

      for user_id in carcelList_keys:
        name = carcelList[user_id]["nombre"]
        del carcelList[user_id]
        if user_id in user_ids_in_room:
          try:
            await self.highrise.teleport(user_id, puerta_pos)
          except:
            pass
      with open("Json/carcelListSave.json", "w") as json_file:
        json.dump(carcelList, json_file)
      return
    if message == "/jail all":
      room_users = (await self.highrise.get_room_users()).content
      user_ids_in_room = {(user_info[0].id, user_info[0].username)
                          for user_info in room_users}
      carcelList_keys = list(carcelList.keys())
      comprobar = False
      # Verificar si hay al menos dos usuarios en la habitación
      for user_id, name in user_ids_in_room:
        if user_id not in carcelList_keys:
          if user_id not in [owner_id, bot_id]:
            comprobar = True

      if comprobar:
        await self.highrise.chat("Todos encarcelados por 30min! 👮👍")
        partesA = str(carcelPos).replace('[', '').replace(']', '')
        partes = partesA.split(',')
        x = float(partes[0].strip())
        y = float(partes[1].strip())
        z = float(partes[2].strip())
        for user_id, name in user_ids_in_room:
          if user_id not in carcelList_keys:
            if user_id not in [owner_id, bot_id]:
              enter_user_carcel(user_id, 30 * 60, name)
              try:
                await self.highrise.teleport(
                    user_id, Position(x, y, z, facing='FrontLeft'))
              except:
                pass

        return
      else:
        await self.highrise.chat("No hay nadie libre para encarcelar 👮")
        return
    if message == "/jail clear":
      room_users = (await self.highrise.get_room_users()).content
      user_ids_in_room = {user_info[0].id for user_info in room_users}
      carcelList_keys = list(carcelList.keys())
      detectar = False
      for user_id in carcelList_keys:
        if user_id not in user_ids_in_room:
          detectar = True
          name = carcelList[user_id]["nombre"]
          del carcelList[user_id]
      with open("Json/carcelListSave.json", "w") as json_file:
        json.dump(carcelList, json_file)
      if detectar:
        await self.highrise.chat(
            "lista cárcel actualizada con solo los presentes👮")
      else:
        await self.highrise.chat(
            "Lista limpia, todos los encarcelados están presente 👮")
      return

    if message == "/jail list":
      segureList = dict(carcelList)
      print(carcelList)
      detector = False
      mensajes = []  # Lista para almacenar los mensajes
      usuarios_enviados = set(
      )  # Conjunto para mantener un registro de los usuarios a los que se les ha enviado mensaje
      for user_id, user_data in segureList.items():
        try:
          if user_id in carcelList:
            detector = True
            vartiempo = user_data["tiempo"]
            name = user_data["nombre"]
            horas = vartiempo // 3600
            minutos = (vartiempo % 3600) // 60
            segundos = vartiempo % 60
            mensaje = ""
            if vartiempo >= 3600:
              mensaje += f"\n{name} le quedan {horas}h {minutos}m {segundos}s"
            elif vartiempo >= 60:
              mensaje += f"\n{name} le quedan {minutos}m {segundos}s"
            else:
              mensaje += f"\n{name} le quedan {segundos}s"
            # Verificar si el usuario ya ha sido enviado
            if user_id not in usuarios_enviados:
              mensajes.append(mensaje)  # Agregar mensaje a la lista
              usuarios_enviados.add(
                  user_id)  # Registrar que se envió un mensaje a este usuario
        except Exception:
          pass

      # Enviar mensajes en grupos de 5 cada 0.5 segundos
      for i in range(0, len(mensajes), 5):
        await asyncio.sleep(0.5)  # Esperar 0.5 segundos
        await self.highrise.chat(''.join(mensajes[i:i + 5])
                                 )  # Enviar mensajes del grupo

      if detector == False:
        await self.highrise.chat("no hay nadie en la carcel")
      return
    partesEspacios = message.split()
    if len(partesEspacios) >= 3:
      partes = message.split("@")
      if len(partes) == 2:
        nombre_usuario2 = partes[1].strip().split()[0]
        numCarcel = partes[0].strip().split()[0]
        if nombre_usuario2 == bot_name:
          await self.highrise.chat("yo no hice nada! 😠")
          return
        vartiempo = partesEspacios[2].strip()
        mensaje_restante = ""
        if len(partesEspacios) >= 4:
          # Obtener el texto siguiente al tercer espacio
          texto_siguiente = ' '.join(partesEspacios[3:])
          # Tomar los primeros 40 caracteres del texto siguiente
          mensaje_restante = texto_siguiente[:1000]

        if vartiempo.isdigit():
          vartiempo = int(vartiempo)
          room_users = (await self.highrise.get_room_users()).content
          user_info = [(usr.username, usr.id) for usr, _ in room_users]
          user_names = [info[0] for info in user_info]
          if nombre_usuario2 in user_names:
            id_usuario2 = user_info[user_names.index(nombre_usuario2)][1]
            if vartiempo == 0:
              segureList = dict(carcelList)
              enLaLista = False
              for user_id, user_data in segureList.items():
                try:
                  if user_id in carcelList:
                    await self.highrise.teleport(id_usuario2, puerta_pos)
                    del carcelList[id_usuario2]
                    enLaLista = True

                    await self.highrise.chat(
                        f"Ya eres libre @{nombre_usuario2.upper()}! portate bien! 👮"
                    )
                    await self.highrise.react("thumbs", id_usuario2)
                    with open("Json/carcelListSave.json", "w") as json_file:
                      json.dump(carcelList, json_file)

                    return
                except:
                  pass
              if not enLaLista:
                await self.highrise.chat(
                    f"@{nombre_usuario2.upper()} no está en la cárcel 👮")
              return
            if vartiempo >= 1440:
              vartiempo = 1440

            enter_user_carcel(id_usuario2, vartiempo * 60, nombre_usuario2)

            partesA = str(carcelPos).replace('[', '').replace(']', '')
            partes = partesA.split(',')
            x = float(partes[0].strip())
            y = float(partes[1].strip())
            z = float(partes[2].strip())

            if vartiempo >= 60:
              horas = vartiempo // 60  #
              minutos_restantes = vartiempo % 60
              vartiempo = str(horas) + "h y " + str(minutos_restantes)

            await self.highrise.chat(
                f"{nombre_usuario2} estarás encerrad@ por {vartiempo}min {mensaje_restante} 👮"
            )
            try:
              await self.highrise.teleport(id_usuario2,
                                           Position(x, y, z, facing='FrontLeft'))
            except:
              pass
          else:
            await self.highrise.send_whisper(
                mi_id,
                "ERROR: usuario no existe\nUsa: /jail @nombre [minutos] (motivo opcional)n/jail @nombre 0 para liberar"
            )
        else:
          await self.highrise.send_whisper(
              mi_id,
              "ERROR: minutos\n Usa: /jail @nombre [minutos] (motivo opcional)n/jail @nombre 0 para liberar"
          )
      else:
        await self.highrise.send_whisper(
            mi_id,
            "ERROR: falta @\nUsa: /jail @nombre [minutos] (motivo opcional)n/jail @nombre 0 para liberar"
        )
    else:
      partes = message.split("@")
      if len(partes) == 2:
        nombre_usuario2 = partes[1].strip().split()[0]
        if nombre_usuario2 == bot_name:
          await self.highrise.chat("yo no hice nada! 😠")
          return
        room_users = (await self.highrise.get_room_users()).content
        user_info = [(usr.username, usr.id) for usr, _ in room_users]
        user_names = [info[0] for info in user_info]
        if nombre_usuario2 in user_names:
          id_usuario2 = user_info[user_names.index(nombre_usuario2)][1]
          enter_user_carcel(id_usuario2, 30 * 60, nombre_usuario2)

          partesA = str(carcelPos).replace('[', '').replace(']', '')
          partes = partesA.split(',')
          x = float(partes[0].strip())
          y = float(partes[1].strip())
          z = float(partes[2].strip())

          await self.highrise.chat(
              f"@{nombre_usuario2.upper()} estarás encerrad@ por 30 min 👮")
          try:
            await self.highrise.teleport(id_usuario2,
                                         Position(x, y, z, facing='FrontLeft'))
          except:
            pass
        else:
          await self.highrise.send_whisper(
              mi_id,
              "ERROR: usuario no esta en la sala.\n/jail @nombre [minutos] (motivo opcional)\n/jail @nombre 0 para liberar"
          )
      else:
        await self.highrise.send_whisper(
            mi_id,
            "\n/jail @nombre [minutos] (motivo opcional)\n/jail @nombre 0 para liberar\n/jail free, para liberar a todos\n/jail all, para encarcelar a todos\n/jail list para ver la lista y tiempo restante"
        )
        await self.highrise.chat(
            "\n/jail auto, activar o desactivar que entren automaticamente a la cárcel\n/setjail para establecer la posicion de la carcel"
        )


async def com_death(self: BaseBot, user, message: str) -> None:
  usuario = user.id
  hash_usuario = hash(str(usuario))
  compatibilidad = abs(hash_usuario) % 61
  if compatibilidad >= 60:
    mensajeFinal = "Morirás por aguantar un estornudo durante una reunión importante 🤧"
  elif compatibilidad >= 50:
    mensajeFinal = "Te reirás tanto que literalmente te partirás de risa 😂 y morirás 💀"
  elif compatibilidad >= 40:
    mensajeFinal = "Morirás por ser lanzado por un cañón en un circo después de confundirte con un payaso 🤡"
  elif compatibilidad >= 30:
    mensajeFinal = "Serás abducid@ por un grupo de vacas 🐄 alienígenas 👽 que querían aprender a bailar la macarena 💃"
  elif compatibilidad >= 20:
    mensajeFinal = "Morirás por intentar surfear una ola 🌊 en una tabla de planchar 💀"
  elif compatibilidad >= 10:
    mensajeFinal = "Morirás al ser tragado por un agujero de gusano 🐛🌌 en tu jardín mientras cavabas un hoyo 🕳️"
  elif compatibilidad >= 1:
    mensajeFinal = "Mueres de exceso de salud por comer una ensalada y atragantarte con una lechuga 🥬"
  elif compatibilidad >= 0:
    mensajeFinal = "Morirás pronto por jugar demaciado Highrise 👾💀"
  await self.highrise.chat(
      f"{user.username} Te quedan {compatibilidad} años de vida, {mensajeFinal}"
  )


async def com_future(self: BaseBot, user, message: str) -> None:
  partes = message.split()
  if len(partes) == 1:
    await self.highrise.send_whisper(
        user.id, "/future [pregunta] - para preguntarle a la bot")
  else:
    pregunta = message[8:]
    FraseFinal = random.choice(
        ["Obviamente si 😎", " si 😎", "nel 🙄", "no, pero tu mamá si 😎"])
    await self.highrise.chat(
        f"@{user.username} pregunta: {pregunta} Respuesta: {FraseFinal}")


async def com_joke(self: BaseBot, user, message: str) -> None:
  global dancing_users
  partes = message.split("@")
  id_usuario1 = user.id
  if len(partes) == 2:
    nombre_usuario1 = user.username
    nombre_usuario2 = partes[1].strip()
    room_users = (await self.highrise.get_room_users()).content
    user_info = [(user.username, user.id) for user, _ in room_users]

    user_names = [info[0] for info in user_info]

    if nombre_usuario2 in user_names:
      user2_id = user_info[user_names.index(nombre_usuario2)][1]
      try:
        if user.id in dancing_users:
          dancing_users[user2_id]["status"] = False
      except:
        pass

      await self.highrise.chat(
          f"@{nombre_usuario1.upper()} esta molestando a {nombre_usuario2.upper()}!"
      )
      emote_id = "emote-gravity"
      await self.highrise.send_emote(emote_id, user2_id)

    else:
      await self.highrise.send_whisper(
          id_usuario1, f"El usuario que mencionas no esta dentro de la sala")
  else:
    await self.highrise.send_whisper(
        id_usuario1, f"/joke @usuario - para molestar a un usuario")


async def com_battle(self: BaseBot, user, message: str) -> None:
  global dancing_users
  partes = message.split("@")
  if len(partes) == 2:
    nombre_usuario1 = user.username
    id_usuario1 = user.id
    nombre_usuario2 = partes[1].strip()

    if user.id in dancing_users:
      dancing_users[user.id]["status"] = False

    room_users = (await self.highrise.get_room_users()).content
    user_info = [(user.username, user.id) for user, _ in room_users]

    user_names = [info[0] for info in user_info]

    if nombre_usuario2 in user_names:
      user2_id = user_info[user_names.index(nombre_usuario2)][1]
      try:
        if user.id in dancing_users:
          dancing_users[user2_id]["status"] = False
      except:
        pass

      await self.highrise.chat(
          f"@{nombre_usuario1.upper()} a retado a una pelea epica a @{nombre_usuario2.upper()}! ¿quien ganará?"
      )
      emote_id = "emote-swordfight"
      await self.highrise.send_emote(emote_id, user2_id)
      await self.highrise.send_emote(emote_id, id_usuario1)
      time.sleep(5)
      winner_name = random.choice([nombre_usuario1, nombre_usuario2])
      loser_name = ""
      if winner_name.lower() == nombre_usuario1.lower():
        winner_name = winner_name.upper()
        loser_name = nombre_usuario2.upper()
        emote_id = "emoji-celebrate"
        await self.highrise.send_emote(emote_id, id_usuario1)
        emote_id = "emote-sad"
        await self.highrise.send_emote(emote_id, user2_id)

      else:
        winner_name = winner_name.upper()
        loser_name = nombre_usuario1.upper()
        emote_id = "emote-sad"
        await self.highrise.send_emote(emote_id, id_usuario1)
        emote_id = "emoji-celebrate"
        await self.highrise.send_emote(emote_id, user2_id)

      fraseFinal = random.choice([
          f"@{winner_name} emerge montando un unicornio invisible 🦄 que lanza rayos invisibles ⚡ @{loser_name} quedó impactado y rendido 😲",
          f"En medio de la pelea, @{winner_name} sacó un pinguino disfrazado de monja 🐧 @{loser_name} estuvo tan ocupado riéndose que no pudo contraatacar 😂",
          f"@{winner_name} invocó un tornado de algodón de azúcar que envolvió a @{loser_name} en dulzura, dejándolo con diabetes e incapaz de luchar 😞",
          f"La pelea se desvió hacia una competición de chistes malos, @{winner_name} hizo un chiste tan malo que @{loser_name} se desmayó de lo malo que era 🤡",
          f"En un giro inesperado, @{winner_name} desafió a @{loser_name} a un concurso de carreras de caracoles ciegos 🐌. Sorprendentemente ganó por un centímetro!😱",
          f"La pelea se convirtió en una competencia de baile de pollos hipnotizados🐥. La mirada hipnótica de @{winner_name} 👁️👄👁️ hizo que su pollo hiciera unos pasos increíbles!"
      ])
      await self.highrise.chat(f"{fraseFinal}. El ganador es @{winner_name}! ")
      await asyncio.sleep(3)
      if user.id in dancing_users:
        try:
          dancing_users[user.id]["status"] = True
          dancing_users[user.id]["tiempo"] = 0
        except:
          pass
        try:
          dancing_users[user2_id]["status"] = True
          dancing_users[user2_id]["tiempo"] = 0
        except:
          pass

    else:
      await self.highrise.send_whisper(
          user.id, f"El usuario que mencionas no esta dentro de la sala")
  else:
    await self.highrise.send_whisper(
        user.id, f"/battle @usuario - para pelear contra un usuario")


async def com_match(self: BaseBot, user, message: str) -> None:
  partes = message.split("@")
  if len(partes) == 3:
    nombre_usuario1 = partes[1].strip()
    nombre_usuario2 = partes[2].strip()
    hash_usuario1 = hash(nombre_usuario1) + 4
    hash_usuario2 = hash(nombre_usuario2) + 2
    compatibilidad = abs(hash_usuario1 + hash_usuario2) % 101
    mensajeFinal = ""
    if compatibilidad >= 100:
      mensajeFinal = "¿esto es perfección o algo del diablo? 😱 no importa ya casense! 😍"
    elif compatibilidad >= 99:
      mensajeFinal = "no sé si estar feliz por tanta compatibilidad ❤️" "o triste porque solo faltaba 1% para la perfección 😳"
    elif compatibilidad >= 80:
      mensajeFinal = "los numeros hablan por si solos, ahora todo queda en sus manos, viviran entre las llamas de del amor o dejaran que la llama se extinga"
    elif compatibilidad >= 51:
      mensajeFinal = "Tienen una conexión más fuerte que mi internet! ¡eso es bastante! 😎"
    elif compatibilidad >= 50:
      mensajeFinal = "ni frío ni caliente, ¿quizás amigos con beneficios? 😏"
    elif compatibilidad >= 40:
      mensajeFinal = "bueno podría funcionar si evitan discusiones sobre la pizza con piña 🙄 "
    elif compatibilidad >= 20:
      mensajeFinal = "el amor es complicado, pero ¿porque no hacerlo más interesante? 😈"
    elif compatibilidad >= 2:
      mensajeFinal = "¿compañeros de vida o compañeros de celda? He ahí el dilema 🙃"
    elif compatibilidad >= 1:
      mensajeFinal = "increible mas de 0! hagan el intento! yo les pago la terapia 😎"
    elif compatibilidad >= 0:
      mensajeFinal = "¿Quién los emparejó? ¿Un experto en comedia romántica? 🤡"
    await self.highrise.chat(
        f"La compatibilidad de @{nombre_usuario1} y @{nombre_usuario2} es {compatibilidad}% {mensajeFinal}"
    )
  else:
    await self.highrise.send_whisper(
        user.id,
        "/match @usuario1 @ususario2 - para ver la compatibilidad de dos usuarios"
    )


async def com_help(self: BaseBot, user, message: str) -> None:
  global room_id
  if user.username == owner_name:
    await self.highrise.send_whisper(
        user.id,
        "lista de comandos para 'dueño'.\n(puedes usar '/' o '!')\ntodos los comandos se pueden usar por whisp al bot.\npara más informacion escribe el comando.\n"
    )
    await self.highrise.send_whisper(
        user.id,
        "/tip - dar oro.\n/autotip - tips automaticos.\n/wallet - dinero del bot.\n/tp - teletransportarse.\n/summon - atraer a usuarios."
    )
    await self.highrise.send_whisper(
        user.id,
        "\n/admin - administrar admins.\n/mod - administrar mods.\n/vip - administrar vips.\n\n/dancefloor - editar pista de baile.\n/emote all - enviar emote a todos.\n/emote list - para ver lista de emotes\n/emote @usuario [emote] para enviar emote a un usuario."
    )
    await self.highrise.send_whisper(
        user.id,
        "\n/kick - expulsar a usuarios.\n/ban - banear a usuarios.\n/mute - silenciar a usuarios.\n"
    )
    await self.highrise.send_whisper(
        user.id,
        "/invite - invitar o enviar mensaje a usuarios\n/heart - enviar corazones.\n"
    )
    await self.highrise.send_whisper(
        user.id,
        "/room - cambiar de sala.\n/bot spawn - cambiar spawn del bot.\n/bot follow - el bot te sigue.\n/bot emote - cambiar baile del bot.\n/welcome - cambiar mensaje de bienvenida.\n/loop - cambiar mensaje mensaje automatico.\n"
    )
    await self.highrise.send_whisper(
        user.id,
        "/match - para ver la compatibilidad de dos usuarios.\n/battle - para pelear contra un usuario.\n/future - preguntarle a la bot.\n/joke - molestar a un usuario."
    )
    return
  elif user.username in adminsList:
    await self.highrise.send_whisper(
        user.id,
        "lista de comandos para 'admin'.\n(puedes usar '/' o '!')\ntodos los comandos se pueden usar por whisp al bot.\npara más informacion escribe el comando.\n"
    )
    await self.highrise.send_whisper(user.id, "/tp - teletransportarse.\n/summon - atraer a usuarios.")
    await self.highrise.send_whisper(
        user.id,
        "\n/mod - administrar mods.\n/vip - administrar vips.\n\n/dancefloor - editar pista de baile.\n/emote all - enviar emote a todos.\n/emote list - para ver lista de emotes\n/emote @usuario [emote] para enviar emote a un usuario."
    )
    await self.highrise.send_whisper(
        user.id,
        "\n/kick - expulsar a usuarios.\n/ban - banear a usuarios.\n/mute - silenciar a usuarios.\n"
    )
    await self.highrise.send_whisper(
        user.id,
        "/invite - invitar o enviar mensaje a usuarios\n/heart - enviar corazones.\n"
    )
    await self.highrise.send_whisper(
        user.id,
        "/room - cambiar de sala.\n/bot spawn - cambiar spawn del bot.\n/bot follow - el bot te sigue.\n/bot emote - cambiar baile del bot.\n/welcome - cambiar mensaje de bienvenida.\n/loop - cambiar mensaje mensaje automatico.\n"
    )
    await self.highrise.send_whisper(
        user.id,
        "/match - para ver la compatibilidad de dos usuarios.\n/battle - para pelear contra un usuario.\n/future - preguntarle a la bot.\n/joke - molestar a un usuario."
    )
    return
  elif user.username in modsList:
    await self.highrise.send_whisper(
        user.id,
        "lista de comandos para 'mod'.\n(puedes usar '/' o '!')\ntodos los comandos se pueden usar por whisp al bot.\npara más informacion escribe el comando.\n"
    )
    await self.highrise.send_whisper(user.id, "/tp - teletransportarse.\n/emote list - para ver lista de emotes\n/heart - enviar corazones.\n/emote @usuario [emote] para enviar emote a un usuario.")
    await self.highrise.send_whisper(
        user.id,
        "\n/kick - expulsar a usuarios.\n/ban - banear a usuarios.\n/mute - silenciar a usuarios.\n"
    )
    await self.highrise.send_whisper(
        user.id,
        "/match - para ver la compatibilidad de dos usuarios.\n/battle - para pelear contra un usuario.\n/future - preguntarle a la bot.\n/joke - molestar a un usuario."
    )
    return
  elif user.username in vipList:
    await self.highrise.send_whisper(
        user.id,
        "lista de comandos para 'vip'.\ntodos los comandos se pueden usar por whisp al bot.\npara más informacion escribe el comando.\n"
    )
    await self.highrise.send_whisper(user.id, "/tp - teletransportarse.\n/emote list - para ver lista de emotes\n/heart - enviar corazones.\n/emote @usuario [emote] para enviar emote a un usuario.")
    await self.highrise.send_whisper(
        user.id,
        "\n/match - para ver la compatibilidad de dos usuarios.\n/battle - para pelear contra un usuario.\n/future - preguntarle a la bot.\n/joke - molestar a un usuario."
    )
    return
  else:
    await self.highrise.send_whisper(
        user.id,
        "lista de comandos.\npara más informacion escribe el comando.\n")
    await self.highrise.send_whisper(user.id, "/tp - teletransportarse.")
    await self.highrise.send_whisper(
        user.id,
        "\n/emote list - para ver lista de emotes\n/match - para ver la compatibilidad de dos usuarios.\n/battle - para pelear contra un usuario.\n/future - preguntarle a la bot.\n/joke - molestar a un usuario"
    )
    return


async def com_room(self: BaseBot, user, message: str) -> None:
  global room_id
  if user.username == owner_name or user.username in adminsList:
    user_id = user.id
    partes = message.split()
    partesLink = message.split("=")
    if len(partes) == 1:
      room_users = (await self.highrise.get_room_users()).content
      await self.highrise.send_whisper(
          user_id,
          "usa:\n /room [id_room] para mandar al bot a otra sala.\npuedes usar el numero id solo o el link completo."
      )
      await self.highrise.send_whisper(
          user_id,
          "para obtener el id de la sala, seleecciona la lista de usuarios arriba a la derecha de la pantalla y presiona al lado del icono de la bandera, se copiara el link con el id de la sala."
      )
      await self.highrise.send_whisper(
          user_id,
          "recuerda que el bot debe tener permiso de diseñador para entrar a una sala y moderador para poder kickear"
      )
      return
    elif len(partes) == 2:
      roomLink = ""
      if len(partesLink) == 2:
        roomLink = partesLink[1].strip()
      else:
        roomLink = partes[1].strip()
        print(roomLink)
      if roomLink:
        room_id = roomLink
        guardar = {'room_idSave': room_id}
        guardar_variables(guardar)
        await self.highrise.send_whisper(
            user_id,
            "Entendido me iré en 5 segundos, volvere aqui si ocurre un error.")
        await self.highrise.send_whisper(
            user_id,
            "recuerda que el bot debe tener permiso de diseñador para entrar a una sala y moderador para poder kickear"
        )
        await asyncio.sleep(5)
        await self.highrise.send_whisper(":v", "error forzado")


async def com_dancefloor(self: BaseBot, user, message: str) -> None:
  global danceFloorCoordenadas
  if user.username == owner_name or user.username in adminsList:
    user_id = user.id
    partes = message.split()
    if len(partes) == 1:
      room_users = (await self.highrise.get_room_users()).content
      await self.highrise.send_whisper(
          user_id,
          "usa:\n /dancefloor [1-2] para la crear la pista de baile.\n/dancefloor stop, para detener la pista\n/dancefloor play para activar lapistazona"
      )
      return
    elif len(partes) == 2:
      parteDos = partes[1]
      if parteDos == "stop" or parteDos == "off" or parteDos == "desactive":
        if room_id in danceFloorCoordenadas:
          try:
            danceFloorCoordenadas[room_id]["status"] = False
            with open("Json/danceFloorCoordenadas.json", "w") as json_file:
              json.dump(danceFloorCoordenadas, json_file)
            await self.highrise.send_whisper(user_id, "dancefloor desactivado")
          except Exception:
            pass
        else:
          await self.highrise.send_whisper(
              user_id,
              "no hay dancerfloor creado en esta sala, usa:\n /dancefloor [1-2] para crear la pista de baile."
          )
        return

      elif parteDos == "play" or parteDos == "active" or parteDos == "on":
        if room_id in danceFloorCoordenadas:
          try:
            danceFloorCoordenadas[room_id]["status"] = True
            with open("Json/danceFloorCoordenadas.json", "w") as json_file:
              json.dump(danceFloorCoordenadas, json_file)
            await self.highrise.send_whisper(user_id, "dancefloor activado")
          except Exception:
            pass
        else:
          await self.highrise.send_whisper(
              user_id,
              "no hay dancerfloor creado en esta sala, usa: /dancefloor [1-2] para crear la pista de baile."
          )
        return

      elif partes[1] == "1":

        room_users = (await self.highrise.get_room_users()).content
        for room_user, pos in room_users:
          if room_user.id == user_id:
            if isinstance(pos, Position):
              if room_id in danceFloorCoordenadas:
                danceFloorCoordenadas[room_id]["min_x"] = pos.x
                danceFloorCoordenadas[room_id]["min_y"] = pos.y
                danceFloorCoordenadas[room_id]["min_z"] = pos.z
                try:
                  min_x = danceFloorCoordenadas[room_id]["max_x"]
                  danceFloorCoordenadas[room_id]["status"] = True
                  await self.highrise.send_whisper(
                      user_id, "punto 1 actualizado y dancefloor activado.")
                except Exception:
                  await self.highrise.send_whisper(
                      user_id,
                      "punto 1 actualizado, usa: /dancefloor [1-2] para actualizar el punto 2"
                  )
                  pass
              else:
                danceFloorCoordenadas[room_id] = {
                    "min_x": pos.x,
                    "min_y": pos.y,
                    "min_z": pos.z,
                    "status": False
                }

                await self.highrise.send_whisper(
                    user_id,
                    "punto 1 creado, usa:\n/dancefloor 2 para actualizar el punto 2"
                )

              with open("Json/danceFloorCoordenadas.json", "w") as json_file:
                json.dump(danceFloorCoordenadas, json_file)
      elif partes[1] == "2":
        room_users = (await self.highrise.get_room_users()).content
        for room_user, pos in room_users:
          if room_user.id == user_id:
            if isinstance(pos, Position):
              if room_id in danceFloorCoordenadas:
                danceFloorCoordenadas[room_id]["max_x"] = pos.x
                danceFloorCoordenadas[room_id]["max_y"] = pos.y
                danceFloorCoordenadas[room_id]["max_z"] = pos.z
                try:
                  min_x = danceFloorCoordenadas[room_id]["min_x"]
                  danceFloorCoordenadas[room_id]["status"] = True
                  await self.highrise.send_whisper(
                      user_id, "punto 2 actualizado y dancefloor activado.")
                except Exception:
                  await self.highrise.send_whisper(
                      user_id,
                      "punto 2 actualizado, usa:\n/dancefloor 1 para actualizar el punto 1"
                  )
                  pass
              else:
                danceFloorCoordenadas[room_id] = {
                    "max_x": pos.x,
                    "max_y": pos.y,
                    "max_z": pos.z,
                    "status": False
                }
                await self.highrise.send_whisper(
                    user_id,
                    "punto 2 creado, usa:\n/dancefloor 1 para actualizar el punto 1"
                )
              with open("Json/danceFloorCoordenadas.json", "w") as json_file:
                json.dump(danceFloorCoordenadas, json_file)
      else:
        await self.highrise.send_whisper(
            user_id,
            "usa:\n /dancefloor [1-2] para la crear la pista de baile.\n/dancefloor stop, para detener la pista\n/dancefloor play para activar lapistazona"
        )
  else:
    await self.highrise.send_whisper(user_id,
                                     "no tienes permiso de usar este comando")


async def com_bot_emote(self: BaseBot, user, message: str) -> None:
  global BotDanceBaile, Botemotetime, BotemoteTimerest
  if user.username == owner_name or user.username in adminsList:
    partes = message.split()
    if len(partes) == 2:
      await self.highrise.send_whisper(
          user.id,
          f"el bot puede usar todos los emotes del juego, debes usar el nombre completo del emote.\n"
      )
      await self.highrise.send_whisper(
          user.id,
          "/bot emote [emote] para activar emote al bot.\n/bot emote list, para ver la lista de emotes.\n/bot emotes random, para que el bot haga bailes randoms"
      )
    if len(partes) >= 3:
      if message == "/bot emote list" or message == "!bot emote list":
        # Obtener todos los nombres de los emoticones
        nombres_emotes = [emote.name for emote in emotes]
        # Dividir los nombres en grupos de 10
        grupos_de_15 = [
            ", ".join(grupo) for grupo in [
                nombres_emotes[i:i + 15]
                for i in range(0, len(nombres_emotes), 15)
            ]
        ]
        # Enviar cada grupo por el chat
        for grupo in grupos_de_15:
          try:
            await self.highrise.send_whisper(user.id, grupo)
          except Exception as e:
            pass
        # Si sobran nombres, enviarlos también
        sobrantes = nombres_emotes[len(grupos_de_15) * 15:]
        if sobrantes:
          try:
            await self.highrise.send_whisper(user.id, ", ".join(sobrantes))
          except Exception as e:
            pass
      elif message == "/bot emote random":
        BotemoteTimerest = 0
        BotDanceBaile = "random"
        Botemotetime = 0
      else:
        emote_name = ' '.join(partes[2:]).strip().lower()

        idEmote, timeEmote = emoteObtener(emote_name)

        if idEmote is not None:
          BotemoteTimerest = timeEmote
          BotDanceBaile = idEmote
          Botemotetime = 0

        else:
          await self.highrise.send_whisper(
              user.id,
              f"Emote '{emote_name}' no encontrado\nel bot puede usar todos los emotes del juego, debes usar el nombre completo del emote.\n"
          )
          await self.highrise.send_whisper(
              user.id,
              f"para ver la lista usa:\n/bot emote list o usa /bot emote random para que tenga emotes de bailes al azar"
          )


async def com_bot_spawn(self: BaseBot, user, message: str) -> None:
  global botspawnPos
  if user.username == owner_name or user.username in adminsList:
    room_users = (await self.highrise.get_room_users()).content
    user_id = user.id
    for room_user, pos in room_users:
      if room_user.id == user_id:
        if isinstance(pos, Position):
          spawnPos = [pos.x, pos.y, pos.z, pos.facing]
          caraAngulo = pos.facing
          botspawnPos[room_id] = spawnPos
          with open("Json/botspawnPosSave.json", "w") as json_file:
            json.dump(botspawnPos, json_file)
          try:
            await self.highrise.teleport(
                bot_id, Position(pos.x, pos.y, pos.z, pos.facing))
          except:
            pass
          await asyncio.sleep(0.5)
          await self.highrise.walk_to(Position(pos.x, pos.y, pos.z,
                                               pos.facing))
          await self.highrise.send_whisper(
              user_id, "punto de spawn actualizado para esta sala.")
          return
        else:
          await self.highrise.send_whisper(
              user_id, "no puedes actualizar el spawn del bot sentado.")


async def com_follow_stop(self: BaseBot, user, message: str) -> None:
  global nombreParaSeguir, botDanceState, Botemotetime
  if user.username == owner_name or user.username in adminsList:
    nombreParaSeguir = ""
    botDanceState = True
    Botemotetime = 0
    await self.highrise.send_whisper(user.id, "entendido me detendré!")


async def com_follow(self: BaseBot, user, message: str) -> None:
  global nombreParaSeguir, botDanceState
  if user.username == owner_name or user.username in adminsList:
    user_id = user.id
    partes = message.split()
    if len(partes) == 1:
      botDanceState = False
      nombreParaSeguir = user.username
      room_users = (await self.highrise.get_room_users()).content
      await self.highrise.send_whisper(
          user_id,
          "te sigo! usa:\n/follow stop para que deje de seguirte\n\n/follow [@nombre] para que siga a algún un usuario"
      )
      for room_user, pos in room_users:
        if room_user.id == user_id:
          if isinstance(pos, Position):
            await self.highrise.walk_to(
                Position(pos.x - 1, pos.y, pos.z - 1, pos.facing))
            return
    elif partes[1].startswith("@"):
      nameUser = partes[1].strip()
      nameUser = nameUser.split("@")[1]
      verificar = False
      room_users = (await self.highrise.get_room_users()).content
      user_info = [(usr.username, usr.id) for usr, _ in room_users]
      name_id = ""
      user_position = None
      for user, position in room_users:
        if bot_name == nameUser:
          await self.highrise.send_whisper(user_id,
                                           "no puedo seguirme a mi mismo 😠")
          return
        if user.username == nameUser:
          botDanceState = False
          nombreParaSeguir = user.username
          pos = position
          await self.highrise.send_whisper(
              user_id,
              "entendido lo seguiré! usa:\n/follow stop, para que deje de seguirlo"
          )
          if isinstance(pos, Position):
            try:
              await self.highrise.walk_to(
                  Position(pos.x - 1, pos.y, pos.z - 1, pos.facing))
            except Exception:
              pass
            return


async def com_loop(self: BaseBot, user, message: str) -> None:
  global loopAnuncio, loopAnuncioSeg
  if user.username == owner_name or user.username in adminsList:
    partes = message.split()
    if len(partes) == 1:
      await self.highrise.chat(
          "usa:\n/loop [mensaje] para actualizar el loop\n/loop [segundos] para cambiar cada cuantos segundos se enviara el loop"
      )
    if len(partes) == 2:
      if partes[1].isdigit():
        try:
          loopAnuncioSeg = int(partes[1])
          if loopAnuncioSeg < 10:
            loopAnuncioSeg = 10
          guardar = {'autoTipSegSave': loopAnuncioSeg}
          guardar_variables(guardar)
          await self.highrise.send_whisper(
              user.id, f"se enviarán loops cada {loopAnuncioSeg} segundos")
        except Exception:
          return
        return
    if len(partes) >= 2:
      partes = message.split(" ")
      anuncio = ' '.join(partes[1:])
      if anuncio == "stop":
        await self.highrise.send_whisper(
            user.id, "se han detenido los loops automaticos")
      guardar = {'anuncioAuto': anuncio}
      guardar_variables(guardar)
      loopAnuncio = (guardar['anuncioAuto'])
      if loopAnuncio != "stop":
        await self.highrise.send_whisper(user.id, f"texto loop Actualizado.")


async def com_emote_all(self: BaseBot, user, message: str) -> None:
  global dancing_users, dance_floor_status, botDanceState, Botemotetime, dance_floor_tiempo
  if user.username == owner_name or user.username in adminsList:
    partes = message.split()
    if len(partes) == 2:
      await self.highrise.send_whisper(
          user.id,
          "usa:\n/emote all [emote] para activar el emote a todos en la sala.\n/emote list - para ver la lista de emotes.")
      return
    if len(partes) == 3:
      emote_name = partes[2].strip().lower()

      room_users = (await self.highrise.get_room_users()).content
      dance_floor_status = False
      botDanceState = False
      for user_info in room_users:
        user_id = user_info[0].id
        if user_id in dancing_users:
          dancing_users[user_id]["status"] = False

      tiempoReset = 0
      emote_id = ""
      detector = False
      if emote_name in listReset:
        detector = True
        emote_id = listReset[emote_name]['id']
        tiempoReset = listReset[emote_name]['tiempo']
      if not detector:
        await self.highrise.send_whisper(user.id, "Emote no existe")
        return
      for user_info in room_users:
        user = user_info[0]
        try:
          await self.highrise.send_emote(emote_id, user.id)
        except:
          pass

      await asyncio.sleep(tiempoReset)

      for user_info in room_users:
        user_id = user_info[0].id

        if user_id in dancing_users:
          dancing_users[user_id]["status"] = True
          dancing_users[user_id]["tiempo"] = 0
      dance_floor_status = True
      dance_floor_tiempo = 0
      botDanceState = True
      Botemotetime = 0
  else:
    await self.highrise.send_whisper(
        user.id, "No tienes permiso para usar este comando")


async def com_tip(self: BaseBot, user, message: str) -> None:
  if user.username == owner_name:
    partes = message.split()
    user_id = user.id
    if len(partes) == 1:
      await self.highrise.send_whisper(
          user_id,
          "usa:\n/tip [oro] - para dar tips a todos\n/tip [oro] [cantidad de usuarios] - para dar tips a usuarios al azar\n/tip [oro] @usuario - para dar a un usuario\n\n/autotip, para ver opciones de tips automaticos"
      )

      return

    cantidad_a_tipo = {
        1: "gold_bar_1",
        5: "gold_bar_5",
        10: "gold_bar_10",
        50: "gold_bar_50",
        100: "gold_bar_100",
        500: "gold_bar_500",
        1000: "gold_bar_1k",
        5000: "gold_bar_5000",
        10000: "gold_bar_10k",
    }
    if len(partes) >= 2:
      if len(partes) >= 3:
        if partes[1].startswith("@"):
          userTip = partes[1].replace("@", "")
          parteCantidad = partes[2].strip()

          if not parteCantidad.isdigit():
            await self.highrise.send_whisper(
                user_id,
                "ERROR: oro invalido\n/tip [oro] - para dar tips a todos\n/tip [oro] [cantidad de usuarios] - para dar tips a usuarios al azar\n/tip [oro] @usuario - para dar a un usuario"
            )
            return

          tipo_barra_de_oro = cantidad_a_tipo.get(int(parteCantidad))
          room_users = (await self.highrise.get_room_users()).content
          user_info = [(usr.username, usr.id) for usr, _ in room_users]
          verificar = False
          user_id_tip = 0
          for username, uid in user_info:
            if username == userTip:
              verificar = True
              user_id_tip = uid
              break
          if verificar:
            try:
              result = await self.highrise.tip_user(user_id_tip,
                                                    tipo_barra_de_oro)
              if result == "success":
                await self.highrise.chat(
                    f"{parteCantidad}g enviado a {userTip}")
              elif result == "insufficient_funds":
                oroDisponible = (await
                                 self.highrise.get_wallet()).content[0].amount

                await self.highrise.send_whisper(
                    user_id,
                    f"bot sin fondos suficientes para dar {parteCantidad}g\nla billetera del bot tiene {oroDisponible}g"
                )
            except Exception:
              pass
          else:
            await self.highrise.send_whisper(
                user_id,
                "ERROR: el usuario no esta en la sala\n/tip [oro] - para dar tips a todos\n/tip [oro] [cantidad de usuarios] - para dar tips a usuarios al azar\n/tip [oro] @usuario - para dar a un usuario"
            )

          return
        else:
          pass

      if partes[1].startswith("@"):
        await self.highrise.send_whisper(
            user_id,
            "ERROR: falta cantidad de oro\n/tip [oro] - para dar tips a todos\n/tip [oro] [cantidad de usuarios] - para dar tips a usuarios al azar\n/tip [oro] @usuario - para dar a un usuario"
        )
        return

      numeros_validos = {1, 5, 10, 50, 100, 500, 1000, 5000, 10000}
      partes = message.split(" ")
      parteCantidad = partes[1].strip()

      if not parteCantidad.isdigit():
        parteCantidad = 0

      if int(parteCantidad) not in numeros_validos:
        await self.highrise.send_whisper(
            user_id,
            "ERROR: cantidad de oro invalido\n/tip [oro] - para dar tips a todos\n/tip [oro] [cantidad de usuarios] - para dar tips a usuarios al azar\n/tip [oro] @usuario - para dar a un usuario"
        )
        return

      else:
        parteLimit = 0
        if len(partes) >= 3:
          parteLimit = partes[2].strip()
          if not parteLimit.startswith("@"):
            if parteLimit.isdigit():
              parteLimit = int(parteLimit)
              if parteLimit <= 0:
                await self.highrise.send_whisper(
                    user_id,
                    "ERROR: no puedes usar 0 en [cantidad de usuarios]\n/tip [oro] - para dar tips a todos\n/tip [oro] [cantidad de usuarios] - para dar tips a usuarios al azar\n/tip [oro] @usuario - para dar a un usuario"
                )
                return
              pass
            else:
              await self.highrise.send_whisper(
                  user_id,
                  "ERROR: [cantidad de usuarios] no es un numero valido\n/tip [oro] - para dar tips a todos\n/tip [oro] [cantidad de usuarios] - para dar tips a usuarios al azar\n/tip [oro] @usuario - para dar a un usuario"
              )
              return

        tipo_barra_de_oro = cantidad_a_tipo.get(int(parteCantidad))
        wallet = (await self.highrise.get_wallet()).content
        oroDisponible = wallet[0].amount
        room_users_response = await self.highrise.get_room_users()
        room_users = room_users_response.content
        room_users = [(user, position) for user, position in room_users
                      if user.username not in [owner_name, bot_name]]

        if len(room_users) > int(parteLimit):
          random_users = random.sample(room_users, int(parteLimit))

        else:
          random_users = room_users

        num_users = len(room_users)
        NumUserTip = len(random_users)
        if num_users <= 0:
          await self.highrise.send_whisper(
              user_id, "No hay suficientes usuarios para dar tips.")
        else:

          #se suma la comision dependiendo de la cantidad

          oroSolicitado = NumUserTip * int(parteCantidad)

          if int(parteCantidad) in numeros_validos:
            oroSolicitado += NumUserTip
          elif int(parteCantidad) == 50:
            oroSolicitado += 5 * NumUserTip
          elif int(parteCantidad) == 100:
            oroSolicitado += 10 * NumUserTip
          elif int(parteCantidad) == 500:
            oroSolicitado += 50 * NumUserTip
          elif int(parteCantidad) == 1000:
            oroSolicitado += 100 * NumUserTip
          elif int(parteCantidad) == 5000:
            oroSolicitado += 500 * NumUserTip
          else:
            oroSolicitado += 1000 * NumUserTip

          if oroDisponible >= oroSolicitado:
            if len(room_users) > parteLimit:
              await self.highrise.send_whisper(
                  user_id,
                  f"se enviará {parteCantidad}g a {NumUserTip} usuarios al azar\nel oro solicitado es de {oroSolicitado}g"
              )

            else:
              await self.highrise.send_whisper(
                  user_id,
                  f"se enviará {parteCantidad}g a {NumUserTip} usuarios\nel oro solicitado es de {oroSolicitado}g"
              )
            for user, _ in random_users:
              tip_user_id = user.id
              user_name = user.username
              try:
                await self.highrise.tip_user(tip_user_id, tipo_barra_de_oro)
                await self.highrise.chat(
                    f"{parteCantidad}g enviado a {user_name}")
              except Exception:
                pass
          else:
            await self.highrise.send_whisper(
                user_id,
                f"no es posible repartir a todos, el bot tiene {oroDisponible}g y necesita {oroSolicitado}g"
            )
  else:
    await self.highrise.send_whisper(user.id,
                                     "solo el dueño puede usar este comando")


async def com_welcome(self: BaseBot, user, message: str) -> None:
  global welcomeText, loopAnuncio
  if user.username == owner_name or user.username in adminsList:
    partes = message.split()
    if len(partes) == 1:
      await self.highrise.chat(
          "usa:\n/welcome [mensaje] para cambiar el mensaje de ingreso a la sala.\nusa un '@' para que mencione al un usuario."
      )
      return
    if len(partes) >= 2:
      partes = message.split(" ")
      welcomeText = ' '.join(partes[1:])
      if welcomeText == "stop":
        await self.highrise.send_whisper(
            user.id, "se ha detenido el anuncio de bienvenida")
      welcomeText = welcomeText.replace("@", "@{user.username}")
      guardar = {'welcomeTextSave': welcomeText}
      guardar_variables(guardar)

      if welcomeText != "stop":
        await self.highrise.send_whisper(user.id,
                                         "mensaje de bienvenida actualizado.")


async def com_autotip(self: BaseBot, user, message: str) -> None:
  global tipstate, tipLimitUserTip, tipMinRequerido, tipcantidad, tiptimerestaurar, tiptime
  if user.username == owner_name:
    partes = message.split()
    user_id = user.id
    if len(partes) == 2:
      partes = message.split(" ")
      parteComando = partes[1].strip()
      if parteComando == "limit":
        await self.highrise.send_whisper(
            user_id,
            "usa:\n/autotip limit [numero] para establecer el limite de usuarios a los que se le repartirán tips al azar con autotip. (usa 0 para que no tenga limite y de tips a toda la sala)"
        )
        return

      elif parteComando == "min":
        await self.highrise.send_whisper(
            user_id,
            "usa:\n/autotip min [numero] para establecer el minimo de usuarios requeridos en la sala para activarse el autotip."
        )
        return

      elif parteComando == "stop" or parteComando == "off" or parteComando == "desactive":
        print("autotip apagado")
        tipstate = False
        guardar = {'autoTipSave': ""}
        guardar_variables(guardar)
        await self.highrise.send_whisper(
            user_id,
            "Tips automaticos desactivados correctamente.\nPara volver a activar usa:\n/autotip [oro] [minutos]"
        )
        return
      else:
        pass
    if len(partes) <= 2:

      if tipstate:
        await self.highrise.send_whisper(
            user_id,
            f"[aviso] Los tips automaticos estan activados,se enviaran {tipcantidad}g a {tipLimitUserTip} usuarios cada {tiptime} minutos cuando hayan {tipMinRequerido} o mas en la sala."
        )
      await self.highrise.send_whisper(
          user_id,
          "\n/autotip [cantidad] [minutos]\npara repartir tips automaticamente cuando hayan X o mas en la sala cada X minutos\n\n/autotip stop, para detenerlo.\n"
      )
      await self.highrise.send_whisper(
          user_id,
          "/autotip limit - para establecer el limite de usuarios a los que se le repartirán tips al azar con autotip. (usa 0 para que no tenga limite y de tips a toda la sala)\n"
      )
      await self.highrise.send_whisper(
          user_id,
          "/autotip min - para establecer el minimo de usuarios requerido en sala para activarse el autotip."
      )
      return

    if len(partes) >= 3:
      parteComando = partes[1].strip()
      if parteComando == "min":
        minimo = partes[2].strip()
        if minimo.isdigit():
          if int(minimo) <= 2:
            minimo = 3
          tipMinRequerido = int(minimo)
          guardar = {'tipMinRequeridoSave': minimo}
          guardar_variables(guardar)
          await self.highrise.send_whisper(
              user_id,
              f"se ha establecido en '{minimo}' el minimo de usuarios requeridos en la sala para activarse el autotip."
          )
          return
        else:
          await self.highrise.send_whisper(
              user_id,
              "Error: no es un numero, usa\n/autotip min [numero] para establecer el minimo de usuarios en sala para activarse el autotip."
          )
          return
      elif parteComando == "limit":
        limitNum = partes[2].strip()
        if limitNum.isdigit():
          tipLimitUserTip = int(limitNum)
          guardar = {'tipLimitUserTipSave': limitNum}
          guardar_variables(guardar)
          if tipLimitUserTip == 0:
            await self.highrise.send_whisper(
                user_id,
                f"establecido 'sin limite' se repartirá a toda la sala con autotip."
            )
            return
          else:
            await self.highrise.send_whisper(
                user_id,
                f"se ha establecido en '{limitNum}' el limite de usuarios a los que se le repartirán tips al azar con autotip."
            )
            return
        else:
          await self.highrise.send_whisper(
              user_id,
              "Error: no es un numero, usa\n/autotip limit [numero] para establecer el limite de usuarios a los que se le repartirán tips al azar con autotip.  (usa 0 para que no tenga limite y de tips a toda la sala)"
          )
          return
      else:

        numeros_validos = {1, 5, 10, 50, 100, 500, 1000, 5000, 10000}
        partes = message.split(" ")
        parteCantidad = partes[1].strip()
        parteTiempo = partes[2].strip()
        ComandoAprobado = True

        if not parteCantidad.isdigit() or int(
            parteCantidad) not in numeros_validos:
          ComandoAprobado = False
          await self.highrise.send_whisper(
              user_id,
              "Error cantidad de oro, numero no valido, solo se admite 1, 5, 10, 50, 100. etc."
          )

        if not (parteTiempo.isdigit() and 1 <= int(parteTiempo) <= 60):
          ComandoAprobado = False
          await self.highrise.send_whisper(
              user_id,
              "Error Tiempo: debe ser un numero entre 1 y 60 (minutos)")

        if ComandoAprobado:

          tiptimerestaurar = int(parteTiempo)
          tiptime = parteTiempo
          tipcantidad = parteCantidad
          tipstate = True

          guardar = {'autoTipSave': "True"}
          guardar_variables(guardar)
          guardar = {'cantidadTipSave': tipcantidad}
          guardar_variables(guardar)
          guardar = {'tiempoTipSave': tiptime}
          guardar_variables(guardar)

          wallet = (await self.highrise.get_wallet()).content
          await self.highrise.send_whisper(
              user_id,
              f"se enviaran {tipcantidad}g cada {tiptime} minutos cuando hayan {tipMinRequerido} o mas en la sala.\noro disponible: {wallet[0].amount}g\n\n/autotip stop, para detenertlo\n/autotip, para ver mas configuraciones"
          )
        else:
          await self.highrise.send_whisper(
              user_id,
              "Utiliza\n/autotip [oro] [minutos]\npara repartir tips automaticamente cuando hayan X o mas en la sala cada X minutos.\n\n/autotip stop, para detenerlo"
          )
        return
  else:
    await self.highrise.send_whisper(user.id,
                                     "solo el dueño puede usar este comando")


async def com_wallet(self: BaseBot, user, message: str) -> None:
  if user.username == owner_name or user.username in adminsList:
    wallet = (await self.highrise.get_wallet()).content
    await self.highrise.send_whisper(
        user.id, f"La billetera del bot tiene {wallet[0].amount}g")
  else:
    await self.highrise.send_whisper(
        user.id, "solo el dueño y admins pueden usar este comando")


def convertir_tiempo(segundos):
  dias, segundos = divmod(segundos, 86400)
  horas, segundos = divmod(segundos, 3600)
  minutos, segundos = divmod(segundos, 60)
  return dias, horas, minutos, segundos


async def com_kick(self: BaseBot, user, message: str) -> None:
  if user.username == owner_name or user.username in adminsList or user.username in modsList:
    partes = message.split()
    user_id = user.id
    if len(partes) == 1:
      await self.highrise.send_whisper(
          user.id,
          "usa:\n/kick @usuario, para expulsar a un usuario de la sala")
      return
    #/kick
    if len(partes) >= 2:
      nameUser = partes[1].strip()
      verificar = False
      if "@" in nameUser:
        nameUser = nameUser.split("@")[1]
        room_users = (await self.highrise.get_room_users()).content
        user_info = [(usr.username, usr.id) for usr, _ in room_users]
        for username, uid in user_info:
          if username == nameUser:
            verificar = True
            user_id = uid
            if bot_name == nameUser:
              await self.highrise.send_whisper(user.id,
                                               "no puedes kickear al bot")
              return

            if owner_name == nameUser:
              await self.highrise.send_whisper(
                  user.id, f"no puedes usar este comando con el dueño del bot")
              return
            if owner_name == modsList or owner_name == adminsList:
              await self.highrise.send_whisper(
                  user.id, f"no puedes kickear a moderadores o admins")
              return
            try:
              await self.highrise.moderate_room(user_id, "kick")
              await self.highrise.send_whisper(
                  user.id, f"@{nameUser} ha sido kickeado")
              return
            except Exception:
              await self.highrise.send_whisper(
                  user.id,
                  "el bot necesita permiso de mooderar para kickear a usuarios"
              )
              return

        if verificar == False:
          await self.highrise.send_whisper(user.id,
                                           f"@{nameUser} no esta en la sala")
          return
      else:
        await self.highrise.send_whisper(
            user.id,
            f"usa /kick @usuario, para expulsar a un usuario de la sala")
  else:
    await self.highrise.send_whisper(
        user.id, "No tienes permiso para usar este comando")


async def com_ban(self: BaseBot, user, message: str) -> None:
  global banList
  if user.username == owner_name or user.username in adminsList or user.username in modsList:
    partes = message.split()
    user_id = user.id
    #sin text
    if len(partes) == 1:
      await self.highrise.send_whisper(
          user.id,
          "usa:\n/ban @usuario, para expulsar a un usuario de la sala para siempre"
      )
      return
    #/BAN LIST
    if any(message.lower().startswith(prefix)
           for prefix in ["/ban list", "!ban list"]):
      nameUser = partes[1].strip()
      if not nameUser == owner_name or nameUser not in adminsList:
        if not banList:
          await self.highrise.send_whisper(
              user.id,
              "No hay nadie en la lista de BAN, usa:\m/ban @usuario pora bannear a un usuario de la sala para siempre"
          )
          return
        # Dividir la lista de administradores en bloques de 5 usuarios
        users_chunks = [banList[i:i + 10] for i in range(0, len(banList), 10)]
        # Enviar los mensajes de forma asincrónica
        for chunk in users_chunks:
          # Construir el mensaje para el grupo de usuarios
          messages = [f"-{username}" for username in chunk]
          # Unir todos los mensajes en un solo mensaje para enviar
          message = "Lista de BANEADOS:\n" + "\n".join(messages)
          # Enviar el mensaje al usuario actual
          await self.highrise.send_whisper(user.id, f"\n{message}")
          await asyncio.sleep(1)
        return
    #/BAN DELETE
    if any(message.lower().startswith(prefix) for prefix in
           ["/ban delete", "!ban delete", "/ban remove", "!ban remove"]):
      if len(partes) >= 3:
        nameUser = partes[2].strip()
        verificar = False
        if "@" in nameUser:
          nameUser = nameUser.split("@")[1]
          if nameUser in banList:
            banList.remove(nameUser)
            guardar = {'banListSave': banList}
            guardar_variables(guardar)
            await self.highrise.send_whisper(
                user.id, f"@{nameUser} ha sido removido de la lista de BAN")
            return
          else:
            await self.highrise.send_whisper(
                user.id,
                f"@{nameUser} no esta en la lista de BAN, o está mal escrito el nombre"
            )
            return
        else:
          await self.highrise.send_whisper(
              user.id,
              f"usa:\n/ban delete @usuario, para eliminar a un usuario de la lista de BAN"
          )
          return
      else:
        await self.highrise.send_whisper(
            user.id,
            "usa:\n/ban delete @usuario, para eliminar a un usuario de la lista de BAN"
        )
        return

    #/BAN @USUARIO
    if len(partes) >= 2:
      nameUser = partes[1].strip()
      verificar = False
      if "@" in nameUser:
        nameUser = nameUser.split("@")[1]
        room_users = (await self.highrise.get_room_users()).content
        user_info = [(usr.username, usr.id) for usr, _ in room_users]
        for username, uid in user_info:
          if username == nameUser:
            verificar = True
            user_id = uid
            if bot_name == nameUser:
              await self.highrise.send_whisper(user.id,
                                               "no puedes bannear al bot")
              return
            if owner_name == nameUser:
              await self.highrise.send_whisper(
                  user.id, f"no puedes usar este comando con el dueño del bot")
              return
            if owner_name == modsList or owner_name == adminsList:
              await self.highrise.send_whisper(
                  user.id, f"no puedes bannear a moderadores o admins")
              return
            try:
              await self.highrise.moderate_room(user_id, "kick")
              banList.append(nameUser)
              guardar = {'banListSave': banList}
              guardar_variables(guardar)
              await self.highrise.send_whisper(user.id,
                                               f"@{nameUser} ha sido baneado")
              return
            except Exception:
              await self.highrise.send_whisper(
                  user.id,
                  "el bot necesita permiso de mooderar para bannear a usuarios"
              )
              return

        if verificar == False:
          await self.highrise.send_whisper(user.id,
                                           f"@{nameUser} no esta en la sala")
          return
      else:
        await self.highrise.send_whisper(
            user.id,
            f"usa /ban @usuario, para expulsar a un usuario de la sala para siempre"
        )
  else:
    await self.highrise.send_whisper(
        user.id, "No tienes permiso para usar este comando")


async def com_mute(self: BaseBot, user, message: str) -> None:
  if user.username == owner_name or user.username in adminsList or user.username in modsList:
    partes = message.split()
    user_id = user.id
    if len(partes) == 1:
      await self.highrise.send_whisper(
          user.id,
          "usa:\n/mute @usuario [minutos], para mutear (0 para desmutear) a un usuario de la sala"
      )
      return
    #/mute
    if len(partes) >= 2:
      nameUser = partes[1].strip()
      tiempo = -1
      if len(partes) >= 3:
        tiempo = partes[2].strip()
        if tiempo.isdigit():
          tiempo = int(tiempo)
        else:
          await self.highrise.send_whisper(
              user.id,
              "usa:\n/mute @usuario [minutos], para mutear (0 para desmutear) a un usuario de la sala"
          )
          return
      verificar = False
      if "@" in nameUser:
        nameUser = nameUser.split("@")[1]
        room_users = (await self.highrise.get_room_users()).content
        user_info = [(usr.username, usr.id) for usr, _ in room_users]
        for username, uid in user_info:
          if username == nameUser:
            verificar = True
            user_id = uid
            if bot_name == nameUser:
              await self.highrise.send_whisper(user.id,
                                               "no puedes mutear al bot")
              return

            if owner_name == nameUser:
              await self.highrise.send_whisper(
                  user.id, f"no puedes usar este comando con el dueño del bot")
              return
            if owner_name == modsList or owner_name == adminsList:
              await self.highrise.send_whisper(
                  user.id, f"no puedes mutear a moderadores o admins")
              return
            if tiempo == -1:
              tiempo = 5
            if tiempo > 60:
              tiempo = 60
            tiempo = tiempo * 60
            if tiempo >= 1:
              try:
                await self.highrise.moderate_room(user_id, "mute", tiempo)
                await self.highrise.send_whisper(
                    user.id,
                    f"@{nameUser} ha sido muteado por {int(tiempo/60)} minutos"
                )
                await self.highrise.send_whisper(
                    user_id,
                    f"@{nameUser} has sido muteado por {int(tiempo/60)} minutos"
                )
                return
              except Exception:
                await self.highrise.send_whisper(
                    user.id,
                    "el bot necesita permiso de mooderar para mutear a usuarios"
                )
                return
            else:
              try:
                await self.highrise.moderate_room(user_id, "mute", 1)
                await self.highrise.send_whisper(
                    user.id, f"@{nameUser} ha sido desmuteado")
                await self.highrise.send_whisper(
                    user_id, f"@{nameUser} has sido desmuteado")
                return
              except Exception:
                await self.highrise.send_whisper(
                    user.id,
                    "no puedes desmutear a moderadores o diseñadores o dueño de la sala"
                )
                return

        if not verificar:
          await self.highrise.send_whisper(user.id,
                                           f"@{nameUser} no esta en la sala")
          return
      else:
        await self.highrise.send_whisper(
            user.id,
            f"usa:\n/mute @usuario [minutos], para mutear (0 para desmutear) a un usuario de la sala"
        )
  else:
    await self.highrise.send_whisper(
        user.id, "No tienes permiso para usar este comando")


async def com_admin(self: BaseBot, user, message: str) -> None:
  global adminsList
  if user.username == owner_name:
    partes = message.split()
    user_id = user.id
    if len(partes) == 1:
      await self.highrise.send_whisper(
          user.id,
          "usa:\n/admin @usuario, para dar ADMIN\n/admin delete @usuario, para quitar ADMIN\n/admin list, para ver la lista de ADMINS"
      )
      return

    #ADMIN DELETE
    if any(
        message.lower().startswith(prefix) for prefix in
        ["/admin delete", "!admin delete", "/admin remove", "!admin remove"]):
      if len(partes) <= 2:
        await self.highrise.send_whisper(
            user_id, "usa:\n/admin delete @usuario quitar ADMIN a un usuario")
        return
      if len(partes) >= 3:
        nameUser = partes[2].strip()
        verificar = False
        if "@" in nameUser:
          nameUser = nameUser.split("@")[1]
          if owner_name != nameUser:
            if nameUser in adminsList:
              adminsList.remove(nameUser)
              guardar = {'adminsListSave': adminsList}
              guardar_variables(guardar)
              await self.highrise.send_whisper(
                  user.id, f"@{nameUser} ya no es 'ADMIN'")
              verificar = True
            if not verificar:
              await self.highrise.send_whisper(
                  user.id,
                  f"@{nameUser} no es 'ADMIN' o verifica que esté bien escrito el nombre"
              )
            return
          else:
            await self.highrise.send_whisper(
                user.id, f"no puedes usar este comando con el dueño del bot")
            return
        else:
          await self.highrise.send_whisper(
              user.id, f"usa /admin delete @usuario, para quitar admin")
    # ADMIN LIST
    elif any(message.lower().startswith(prefix)
             for prefix in ["/admin list", "!admin list"]):
      if user.username == owner_name or user.username in adminsList:
        if not adminsList:
          await self.highrise.send_whisper(
              user.id,
              "No hay ADMINISTRADORES, usa:\m/admin @usuario para agregar ADMINS"
          )
          return
        # Dividir la lista de administradores en bloques de 5 usuarios
        users_chunks = [
            adminsList[i:i + 10] for i in range(0, len(adminsList), 10)
        ]
        # Enviar los mensajes de forma asincrónica
        for chunk in users_chunks:
          # Construir el mensaje para el grupo de usuarios
          messages = [f"-{username}" for username in chunk]
          # Unir todos los mensajes en un solo mensaje para enviar
          message = "Lista de ADMINS:\n" + "\n".join(messages)
          # Enviar el mensaje al usuario actual
          await self.highrise.send_whisper(user.id, f"\n{message}")
          await asyncio.sleep(1)
    #ADMIN
    elif len(partes) >= 2:
      nameUser = partes[1].strip()
      verificar = False
      if "@" in nameUser:
        nameUser = nameUser.split("@")[1]
        room_users = (await self.highrise.get_room_users()).content
        user_info = [(usr.username, usr.id) for usr, _ in room_users]
        user_names = [info[0] for info in user_info]
        user_names_id = [info[1] for info in user_info]
        if nameUser in user_names:
          if owner_name != nameUser:
            if nameUser in adminsList:
              verificar = True
              await self.highrise.send_whisper(user.id,
                                               f"@{nameUser} ya es 'ADMIN'")
            if not verificar:
              adminsList.append(nameUser)
              guardar = {'adminsListSave': adminsList}
              guardar_variables(guardar)
              await self.highrise.send_whisper(
                  user_id, f"@{nameUser} ahora es 'ADMIN'")
            return
          else:
            await self.highrise.send_whisper(
                user.id, f"no puedes usar este comando con el dueño del bot")
            return

        else:
          await self.highrise.send_whisper(user.id,
                                           f"@{nameUser} no esta en la sala")
          return

      else:
        await self.highrise.send_whisper(
            user.id,
            "usa:\n/admin @usuario, para dar 'ADMIN' a un usuario\n/admin delete @usuario, para quitar admin\n/admin list, para ver la lista de admins"
        )
  else:
    await self.highrise.send_whisper(user.id,
                                     "solo el dueño puede usar este comando")


async def com_vip(self: BaseBot, user, message: str) -> None:
  global vipList, vipstate
  partes = message.split()
  user_id = user.id
  if len(partes) == 1:
    if user.username == owner_name or user.username in adminsList:
      if not vipstate:
        await self.highrise.send_whisper(
            user.id,
            "[aviso] teleports vip esta desactivado, usa /vip active, para activarlo"
        )
      await self.highrise.send_whisper(
          user.id,
          "usa:\n/vip @usuario [horas] (pon 0 para dar VIP permanente)\n/vip delete @usuario, para quitar vip\n/vip list, para ver la lista de vips"
      )
      await self.highrise.send_whisper(
          user.id,
          "\n/vip desactive, para desactivar los comandos teleport vip y pausar el tiempo vip\n/vip active para volver a activarlos"
      )
      await self.highrise.send_whisper(
          user.id,
          "\n*Informacion que ve el usuario*"
      )
      await self.highrise.send_whisper(
          user.id,
          "obten VIP automaticamente tipeando al bot.\nprecios:\n1 dia: 10g\n1 semana: 50g\n1 mes: 100g\n6 meses: 500g\npermanente: 1K o más."
      )
      await self.highrise.send_whisper(
        user.id,
        "\nBeneficios:\n/tele @usuario - ir a un usuario.\n/heart @usuario [1-50] enviar corazones.\n/emote @usuario [emote] para hacer bailar a un usuario.\n/tele vip - zona vip.\n\n-teleport automatico para subir o bajar."
      )
      return
    elif user.username in modsList:
      await self.highrise.send_whisper(user.id,
                                       "los MODS ya tienen los beneficios VIPS.")
      await self.highrise.send_whisper(
          user.id,
          "obten VIP automaticamente tipeando al bot.\nprecios:\n1 dia: 10g\n1 semana: 50g\n1 mes: 100g\n6 meses: 500g\npermanente: 1K o más."
      )
      await self.highrise.send_whisper(
        user.id,
        "\nBeneficios:\n/tele @usuario - ir a un usuario.\n/heart @usuario [1-50] enviar corazones.\n/emote @usuario [emote] para hacer bailar a un usuario.\n/tele vip - zona vip.\n\n-teleport automatico para subir o bajar."
      )
      return
    elif user.username in vipList:
      time_left = vipList[user.username]
      if time_left == 0:
        await self.highrise.send_whisper(
            user.id, f"@{user.username} Tienes VIP permanente")
        return
      dias, horas, minutos, segundos = convertir_tiempo(time_left)
      if dias == 0:
        message = f"{horas}h {minutos}m"
      else:
        message = f"{dias}d {horas}h {minutos}m"
      await self.highrise.send_whisper(
          user.id,
          f"te quedan:\n{message} de VIP, puedes comprar más tiempo de VIP tipeando al bot."
      )
      await self.highrise.send_whisper(
          user.id,
          "precios:\n1 dia: 10g\n1 semana: 50g\n1 mes: 100g\n6 meses: 500g\npermanente: 1K o más."
      )
      await self.highrise.send_whisper(
        user.id,
        "\nBeneficios:\n/tele @usuario - ir a un usuario.\n/heart @usuario [1-50] enviar corazones.\n/emote @usuario [emote] para hacer bailar a un usuario.\n/tele vip - zona vip.\n\n-teleport automatico para subir o bajar."
      )
      return
      
    else:
      await self.highrise.send_whisper(
          user.id,
          "obten VIP automaticamente tipeando al bot.\nprecios:\n1 dia: 10g\n1 semana: 50g\n1 mes: 100g\n6 meses: 500g\npermanente: 1K o más."
      )
      await self.highrise.send_whisper(
        user.id,
        "\nBeneficios:\n/tele @usuario - ir a un usuario.\n/heart @usuario [1-50] enviar corazones.\n/emote @usuario [emote] para hacer bailar a un usuario.\n/tele vip - zona vip.\n\n-teleport automatico para subir o bajar."
      )
      return

  if user.username == owner_name or user.username in adminsList:
    #VIP desactive
    if any(message.lower().startswith(prefix) for prefix in [
        "/vip stop", "!vip stop", "/vip off", "!vip off", "/vip desactive",
        "!vip desactive"
    ]):
      vipstate = ""
      guardar = {'vipStateSave': vipstate}
      guardar_variables(guardar)
      await self.highrise.send_whisper(
          user_id,
          "tiempo VIP pausado y teleports desactivados. usa: /vip active, para activarlo"
      )
      return
    #VIP desactive
    if any(message.lower().startswith(prefix) for prefix in [
        "/vip active", "!vip active", "/vip on", "!vip on", "/vip play",
        "!vip play"
    ]):
      vipstate = "True"
      guardar = {'vipStateSave': vipstate}
      guardar_variables(guardar)
      await self.highrise.send_whisper(
          user_id,
          "tiempo VIP activado y teleports vips activados. usa: /vip desactive, para desactivarlo"
      )
      return
    #VIP DELETE
    if any(message.lower().startswith(prefix) for prefix in
           ["/vip delete", "!vip delete", "/vip remove", "!vip remove"]):
      if len(partes) <= 2:
        await self.highrise.send_whisper(
            user_id, "usa:\n/vip delete @usuario quitar VIP a un usuario")
        return
      if len(partes) >= 3:
        nameUser = partes[2].strip()
        verificar = False
        if "@" in nameUser:
          nameUser = nameUser.split("@")[1]
          if owner_name != nameUser:
            if nameUser in vipList:
              del vipList[nameUser]
              guardar = {'vipListSave': vipList}
              guardar_variables(guardar)
              await self.highrise.send_whisper(user.id,
                                               f"@{nameUser} ya no es 'VIP'")
              verificar = True
            if not verificar:
              await self.highrise.send_whisper(
                  user.id,
                  f"@{nameUser} no es 'VIP' o verifica que esté bien escrito el nombre"
              )
            return
          else:
            await self.highrise.send_whisper(
                user.id, f"no puedes usar este comando con el dueño del bot")
            return
        else:
          await self.highrise.send_whisper(
              user.id, f"usa /vip delete @usuario, para quitar VIP")
    # VIP LIST
    elif any(message.lower().startswith(prefix)
             for prefix in ["/vip list", "!vip list"]):
      if user.username == owner_name or user.username in adminsList:
        # Función para convertir segundos a días, horas, minutos y segundos
        if not vipList:
          await self.highrise.send_whisper(
              user.id,
              "no hay VIPS usa: \m/vip @usuario [horas] (pon 0 para dar VIP permanente)"
          )
          return
        # Dividir la lista de VIPs en bloques de 5 usuarios
        users_chunks = [
            list(vipList.items())[i:i + 5] for i in range(0, len(vipList), 5)
        ]
        # Enviar los mensajes de forma asincrónica
        for chunk in users_chunks:
          # Construir el mensaje para el grupo de usuarios
          messages = []
          for username, time_left in chunk:
            dias, horas, minutos, segundos = convertir_tiempo(time_left)
            if dias == 0:
              message = f"{username} {horas}h {minutos}m de VIP"
            else:
              message = f"{username} {dias}d {horas}h {minutos}m de VIP"
            messages.append(message)
          # Unir todos los mensajes en un solo mensaje para enviar
          message = "Lista de VIPs:\n" + "\n".join(messages)
          # Enviar el mensaje al usuario actual
          await self.highrise.send_whisper(user.id, message)
          await asyncio.sleep(1)
    #VIP set
    elif len(partes) >= 3:
      nameUser = partes[1].strip()
      if "@" in nameUser:
        nameUser = nameUser.split("@")[1]
        room_users = (await self.highrise.get_room_users()).content
        user_info = [(usr.username, usr.id) for usr, _ in room_users]
        user_names = [info[0] for info in user_info]
        if nameUser in user_names:
          if owner_name != nameUser:
            tiempo = partes[2].strip().split()[0]
            try:
              tiempo = int(tiempo)
              if tiempo >= 25:
                tiempo = 24
              segundos = tiempo * 3600
              vipList[nameUser] = segundos
              guardar = {'vipListSave': vipList}
              guardar_variables(guardar)
              if tiempo == 0:
                await self.highrise.send_whisper(
                    user_id, f"'{nameUser}' ahora es 'VIP' para siempre")
              else:
                await self.highrise.send_whisper(
                    user_id, f"'{nameUser}' será 'VIP' por {tiempo} horas")

            except Exception:
              await self.highrise.send_whisper(
                  user_id,
                  f"Error: no es un numero, ingresa el tiempo de vip en horas\n/role [nombre] vip [tiempo] usa 0 para dar vip permantente"
              )
            return
          else:
            await self.highrise.send_whisper(
                user.id, "no puedes usar este comando con el dueño del bot")
            return

        else:
          await self.highrise.send_whisper(user.id,
                                           f"@{nameUser} no esta en la sala")
      else:
        await self.highrise.send_whisper(
            user.id,
            "usa:\n/vip @usuario [horas] (pon 0 para dar VIP permanente)")

    else:
      await self.highrise.send_whisper(
          user.id,
          "usa:\n/vip @usuario [horas] (pon 0 para dar VIP permanente)\n/vip delete @usuario, para quitar VIP\n/vip list, para ver la lista de VIPS"
      )
      await self.highrise.send_whisper(
          user.id,
          "\n/vip desactive, para desactivar los comandos teleport vip y pausar el tiempo vip\n/vip active para volver a activarlos"
      )
  else:
    await self.highrise.send_whisper(
        user.id, "No tienes permiso para usar este comando")


async def com_mod(self: BaseBot, user, message: str) -> None:
  global modsList
  partes = message.split()
  user_id = user.id
  if len(partes) == 1:
    if user.username == owner_name or user.username in adminsList:
      await self.highrise.send_whisper(
          user.id,
          "usa:\n/mod @usuario, para dar MOD\n/mod delete @usuario, para quitar MOD\n/mod list, para ver la lista de MODS"
      )
    if user.username == owner_name or user.username in adminsList or user.username in modsList:
      await self.highrise.send_whisper(
          user.id, "\ncomandos MODS\n/kick - /ban - / mute")
    return
  if user.username == owner_name or user.username in adminsList:

    #MOD DELETE
    if any(message.lower().startswith(prefix) for prefix in
           ["/mod delete", "!mod delete", "/mod remove", "!mod remove"]):
      if len(partes) <= 2:
        await self.highrise.send_whisper(
            user_id, "usa:\n/mod delete @usuario quitar 'MOD' a un usuario")
        return
      if len(partes) >= 3:
        nameUser = partes[2].strip()
        verificar = False
        if "@" in nameUser:
          nameUser = nameUser.split("@")[1]
          if owner_name != nameUser:
            if nameUser in modsList:
              modsList.remove(nameUser)
              guardar = {'modListSave': modsList}
              guardar_variables(guardar)
              await self.highrise.send_whisper(user.id,
                                               f"@{nameUser} ya no es 'MOD'")
              verificar = True
            if not verificar:
              await self.highrise.send_whisper(
                  user.id,
                  f"@{nameUser} no es 'MOD' o verifica que esté bien escrito el nombre"
              )
            return
          else:
            await self.highrise.send_whisper(
                user.id, f"no puedes usar este comando con el dueño del bot")
            return
        else:
          await self.highrise.send_whisper(
              user.id, f"usa /mod delete @usuario, para quitar 'MOD'")
    # MOD LIST
    elif any(message.lower().startswith(prefix)
             for prefix in ["/mod list", "!mod list"]):
      if user.username == owner_name or user.username in adminsList:
        if not modsList:
          await self.highrise.send_whisper(
              user.id,
              "No hay MODERADORES, usa:\m/mod @usuario para agregar MODS")
          return
        # Dividir la lista de administradores en bloques de 5 usuarios
        users_chunks = [
            modsList[i:i + 10] for i in range(0, len(modsList), 10)
        ]
        # Enviar los mensajes de forma asincrónica
        for chunk in users_chunks:
          # Construir el mensaje para el grupo de usuarios
          messages = [f"-{username}" for username in chunk]
          # Unir todos los mensajes en un solo mensaje para enviar
          message = "Lista de MODS:\n" + "\n".join(messages)
          # Enviar el mensaje al usuario actual
          await self.highrise.send_whisper(user.id, f"\n{message}")
          await asyncio.sleep(1)

    elif len(partes) >= 2:
      nameUser = partes[1].strip()
      verificar = False
      if "@" in nameUser:
        nameUser = nameUser.split("@")[1]
        room_users = (await self.highrise.get_room_users()).content
        user_info = [(usr.username, usr.id) for usr, _ in room_users]
        user_names = [info[0] for info in user_info]
        if nameUser in user_names:
          if owner_name != nameUser:
            if nameUser in modsList:
              verificar = True
              await self.highrise.send_whisper(user.id,
                                               f"@{nameUser} ya es 'MOD'")
            if not verificar:
              modsList.append(nameUser)
              guardar = {'modListSave': modsList}
              guardar_variables(guardar)
              await self.highrise.send_whisper(user_id,
                                               f"@{nameUser} ahora es 'MOD'")
            return
          else:
            await self.highrise.send_whisper(
                user.id, f"no puedes usar este comando con el dueño del bot")
            return

        else:
          await self.highrise.send_whisper(user.id,
                                           f"@{nameUser} no esta en la sala")
      else:
        await self.highrise.send_whisper(
            user.id,
            "usa:\n/mod @usuario, para dar 'MOD' a un usuario\n/mod delete @usuario, para quitar MOD\n/mod list, para ver la lista de MODS"
        )

    else:
      await self.highrise.send_whisper(
          user.id,
          "usa:\n/mod @usuario, para dar 'MOD' a un usuario\n/mod delete @usuario, para quitar MOD\n/mod list, para ver la lista de MODS"
      )
  else:
    await self.highrise.send_whisper(
        user.id, "No tienes permiso para usar este comando")


async def com_tele(self: BaseBot, user, message: str) -> None:
  global warpsLista, room_id
  if any(message.lower().startswith(prefix)
         for prefix in ["/tele list", "!tele list", "/tp list", "!tp list"]):

    if room_id in warpsLista:
      name_list = [
          f"{entry['name']} [{entry['rol']}]"
          if entry['rol'] != 'user' else entry['name']
          for entry in warpsLista[room_id]
      ]
      name_str = "\n-".join(name_list)
      await self.highrise.send_whisper(user.id,
                                       f"lista teleports:\n-{name_str}")
    else:
      await self.highrise.send_whisper(
          user.id,
          f"no hay teleports en esta sala\nusa /tp create [nombre] para crear un nuevo teleport"
      )
    return
  #TELE CREATE
  if any(message.lower().startswith(prefix) for prefix in [
      "/tele create", "!tele create", "/tp create", "!tp create", "/tp set",
      "!tp set"
  ]):
    if user.username == owner_name or user.username in adminsList:
      user_id = user.id
      partes = message.split()
      if len(partes) == 3:
        warp = partes[2].strip().lower()

        room_users = (await self.highrise.get_room_users()).content
        for room_user, pos in room_users:
          if room_user.id == user_id:
            if isinstance(pos, Position):
              mipos = [pos.x, pos.y, pos.z]
              rol = "user"
              await enter_warp(self, room_id, warp, mipos, user_id, rol)

            else:
              await self.highrise.send_whisper(
                  user_id, "no puedes crear un teleport sentado")
      elif len(partes) == 4:
        warp = partes[2].strip().lower()
        rol = partes[3].strip().lower()
        user_id = user.id
        if rol.lower() in ["user", "mod", "vip", "admin"]:
          room_users = (await self.highrise.get_room_users()).content
          for room_user, pos in room_users:
            if room_user.id == user_id:
              if isinstance(pos, Position):
                mipos = [pos.x, pos.y, pos.z]
                await enter_warp(self, room_id, warp, mipos, user_id, rol)

              else:
                await self.highrise.send_whisper(
                    user_id, "no puedes crear un teleport sentado")
        else:
          await self.highrise.send_whisper(
              user_id, "rol no valido, usa /tp create [nombre] [admin o vip]")

      else:
        await self.highrise.send_whisper(
            user.id,
            "usa /tp create [nombre] [vip-mod-admin](opcional) para crear o modificar un teleport"
        )
    else:
      await self.highrise.send_whisper(
          user.id, f"no tienes permisos para usar este comando")
    return
  #TELE DELETE
  if any(message.lower().startswith(prefix) for prefix in [
      "/tele delete", "!tele delete", "/tp delete", "!tp delete",
      "/tele remove", "!tele remove", "/tp remove", "!tp remove"
  ]):
    if user.username == owner_name or user.username in adminsList:
      parts = message.split()
      if len(parts) >= 3:
        tercer_texto = parts[2]
        print(tercer_texto)
        if room_id in warpsLista:
          teleport_list = warpsLista[room_id]
          for teleport in teleport_list:
            if teleport['name'] == tercer_texto:
              teleport_list.remove(teleport)
              with open("Json/warpsListaSave.json", "w") as json_file:
                json.dump(warpsLista, json_file)
              await self.highrise.send_whisper(
                  user.id, f"teleport '{tercer_texto}' eliminado")
              break
          else:
            await self.highrise.send_whisper(
                user.id, f"teleport '{tercer_texto}' no existe")
        else:
          await self.highrise.send_whisper(
              user.id, f"teleport '{tercer_texto}' no existe")
      else:
        await self.highrise.send_whisper(user.id, "/tp delete [teleport]")
    else:
      await self.highrise.send_whisper(
          user.id, f"no tienes permisos para usar este comando")
    return
  partes = message.split()
  try:
    command, soloParteDos = message.split(" ", 1)
  except Exception:
    if user.username == owner_name or user.username in adminsList:
      await self.highrise.send_whisper(
          user.id,
          "/tp @user para ir a un usuario\n/tp [coordenada] para ir a una coordenada\n/tp [teleport] para ir a un teleport\n"
      )
      await self.highrise.send_whisper(
          user.id,
          "/tp @user @user para mover un usuario a otro\n/tp @user [teleport] para mover un usuario a una coordenada\n/tp @user [teleport] para mover un usuario a un teleport\n"
      )
      await self.highrise.send_whisper(
          user.id,
          "/tp create [teleport] [vip-mod-admin](opcional) para crear o modificar un teleport\n/tp list - para mostrar lista de teleports\n/tp delete [teleport] - para eliminar un teleport"
      )

    elif user.username in modsList:
      await self.highrise.send_whisper(
          user.id,
          "/tp @user para ir a un usuario\n/tp [coordenada] para ir a una coordenada\n/tp [teleport] para ir a un teleport\n"
      )
      await self.highrise.send_whisper(
          user.id,
          "/tp @user @user para mover un usuario a otro\n/tp @user [teleport] para mover un usuario a una coordenada\n/tp @user [teleport] para mover un usuario a un teleport\n"
      )

    elif user.username in vipList:
      await self.highrise.send_whisper(
          user.id,
          "/tp @user para ir a un usuario\n/tp [teleport] para ir a un teleport\n/tp list - para mostrar lista de teleports"
      )

    else:
      await self.highrise.send_whisper(
          user.id,
          "/tp [teleport] para ir a un teleport\n/tp list - para mostrar lista de teleports"
      )
    return
  room_users = (await self.highrise.get_room_users()).content
  # Caso: /tele @usuario
  if len(partes) == 2 and partes[1].startswith("@"):
    if not vipstate:
      if user.username in vipList:
        if not (user.username == owner_name or user.username in adminsList
                or user.username in modsList):

          await self.highrise.send_whisper(
              user.id, "los comandos vips estan desactivados")
          return
    if user.username == owner_name or user.username in adminsList or user.username in modsList or user.username in vipList:

      userTP = soloParteDos.replace("@", "")
      if not (user.username == owner_name or user.username in adminsList
              or user.username in modsList):

        if bot_name == userTP:
          await self.highrise.send_whisper(
              user.id, "no puedes teletransportarte hacia el bot")
          return
        if userTP == owner_name or userTP in adminsList:
          await self.highrise.send_whisper(
              user.id, "no puedes teletransportarte hacia un ADMIN")
          return
        else:
          pass
      detector = False
      for usr, pos in room_users:
        if usr.username == userTP:
          detector = True
          try:
            await self.highrise.teleport(user.id, pos)
          except:
            pass
          return
      if not detector:
        await self.highrise.send_whisper(
            user.id, f"el usuario {userTP} no está en la sala")
        return
    else:
      await self.highrise.send_whisper(
          user.id, "se requiere rol VIP para usar este comando")
      return

    # Caso: /tele [coordenada]
  elif len(partes) == 4:
    if user.username == owner_name or user.username in adminsList or user.username in modsList:
      try:
        #MOVER HACIA UNA COORDENADA
        x, y, z = soloParteDos.split(" ")
        try:
          await self.highrise.teleport(user.id,
                                       dest=Position(float(x), float(y),
                                                     float(z)))
        except:
          pass
      except ValueError:
        await self.highrise.chat("formato de coordenada incorrecto, usa x y z")
        return
    else:
      await self.highrise.send_whisper(
          user.id, "se requiere rol ADMIN para usar este comando")

    # Caso: /tele [teleport]
  elif len(partes) == 2:
    partes = partes[1]
    if room_id in warpsLista:
      teleport_list = warpsLista[room_id]
      for teleport in teleport_list:
        if teleport['name'] == partes:
          pos = teleport['pos']
          rol = teleport['rol']
          dale = False
          if rol == "vip":
            if user.username == owner_name or user.username in adminsList or user.username in vipList or user.username in modsList:
              dale = True
            else:
              await self.highrise.send_whisper(
                  user.id, "se requiere VIP para usar este comando")
              return
          elif rol == "admin":
            if user.username == owner_name or user.username in adminsList:
              dale = True
            else:
              await self.highrise.send_whisper(
                  user.id, "se requiere rol ADMIN para usar este comando")
              return
          else:
            dale = True
          if dale:
            x, y, z = map(float, pos)
            try:
              await self.highrise.teleport(user.id,
                                           dest=Position(float(x), float(y),
                                                         float(z)))
            except:
              pass
          break
      else:
        await self.highrise.send_whisper(user.id,
                                         f"teleport '{partes}' no existe")
    else:
      await self.highrise.send_whisper(user.id,
                                       f"teleport '{partes}' no existe")

  #/tele @usuario @usuario
  elif len(partes) == 3 and all(part.startswith("@") for part in partes[1:]):
    if user.username == owner_name or user.username in adminsList or user.username in modsList:
      userTP = partes[1].replace("@", "")
      userTP2 = partes[2].replace("@", "")
      detector = False
      for usr, pos in room_users:
        if usr.username == userTP:
          userTP = usr.id
          detector = True
          break
      if detector:
        detector = False
        for usr, pos in room_users:
          if usr.username == userTP2:
            detector = True
            if isinstance(pos, Position):
              try:
                await self.highrise.teleport(userTP, pos)
              except:
                pass
              break
            else:
              await self.highrise.send_whisper(
                  user.id, "el segundo usuario está sentado")
              return
        if not detector:
          await self.highrise.send_whisper(
              user.id, f"el usuario {userTP2} no esta en la sala")
          return

      else:
        await self.highrise.send_whisper(
            user.id, f"el usuario {userTP} no esta en la sala")
        return

    else:
      await self.highrise.send_whisper(user.id, "no puedes usar este comando")
      return
    return

  # Caso: /tele @usuario [coordenada]
  elif len(partes) == 5 and partes[1].startswith("@"):
    if user.username == owner_name or user.username in adminsList or user.username in modsList:
      userTP = partes[1].replace("@", "")
      coordenada = partes[2:]

      detector = False
      for usr, pos in room_users:
        if usr.username == userTP:
          userTP = usr.id
          detector = True
          if len(coordenada) == 3:
            try:
              x, y, z = map(float, coordenada)
              await self.highrise.teleport(userTP,
                                           dest=Position(
                                               float(x), float(y), float(z)))
            except ValueError:
              await self.highrise.send_whisper(
                  user.id,
                  "/tp @usuario [coordenada] La coordenada no es válida")
              return
          return
      if not detector:
        await self.highrise.send_whisper(
            user.id, f"el usuario {userTP} no está en la sala")

      else:
        # La coordenada no tiene el formato correcto
        pass
    else:
      await self.highrise.send_whisper(user.id, "no puedes usar este comando")

  # Caso: /tele @usuario [teleport]
  elif len(partes) == 3 and partes[1].startswith(
      "@") or user.username in modsList:
    if user.username == owner_name or user.username in adminsList or user.username in modsList:
      userTP = partes[1].replace("@", "")
      tele = partes[2]
      print(userTP)
      print(tele)
      detector = False
      for usr, pos in room_users:
        if usr.username == userTP:
          userTP_id = usr.id
          detector = True
          if room_id in warpsLista:
            teleport_list = warpsLista[room_id]
            for teleport in teleport_list:
              if teleport['name'] == tele:
                pos = teleport['pos']
                dale = False
                try:
                  x, y, z = map(float, pos)
                  await self.highrise.teleport(userTP_id,
                                               dest=Position(
                                                   float(x), float(y),
                                                   float(z)))
                except ValueError:
                  await self.highrise.send_whisper(
                      user.id, "no se pudo teletransportar")
                  return

                break

            else:
              await self.highrise.send_whisper(user.id,
                                               f"teleport '{tele}' no existe")
              return
          else:
            await self.highrise.send_whisper(user.id,
                                             f"teleport '{tele}' no existe")
            return
      if not detector:
        await self.highrise.send_whisper(
            user.id, f"el usuario {userTP} no está en la sala")

      else:
        # La coordenada no tiene el formato correcto
        pass
    else:
      await self.highrise.send_whisper(user.id, "no puedes usar este comando")
      return
  elif len(partes) == 3:
    if user.username == owner_name or user.username in adminsList:
      await self.highrise.send_whisper(
          user.id,
          "usa /tp create [nombre] [vip-mod-admin](opcional) para crear o modificar un teleport"
      )

    else:
      await self.highrise.send_whisper(user.id, "no puedes usar este comando")

  # Otros casos
  else:
    # Realizar acciones para otros casos
    await self.highrise.send_whisper(
        user.id,
        "usa /tp create [nombre] [vip-mod-admin](opcional) para crear o modificar un teleport"
    )
    pass


async def enter_warp(self, room_id, warpname, pos, user_id, rol):
  global warpsLista
  # Si la sala_id ya existe en warpsLista, actualiza o agrega el warpname
  if room_id in warpsLista:
    warps = warpsLista[room_id]

    # Busca si ya existe un warp con el mismo nombre
    warp_exists = False
    for warp in warps:
      if warp['name'] == warpname:
        # Si ya existe un warp con el mismo nombre, actualiza su posición
        warp['pos'] = pos
        warp['rol'] = rol
        warp_exists = True
        with open("Json/warpsListaSave.json", "w") as json_file:
          json.dump(warpsLista, json_file)
        await self.highrise.send_whisper(
            user_id,
            f"se ha actualizado el teleport {warpname} en tu ubicación para el rol '{rol}'"
        )

        break
    if not warp_exists:
      # Si no existe un warp con el mismo nombre, agrega uno nuevo
      warps.append({'name': warpname, 'rol': rol, 'pos': pos})
      with open("Json/warpsListaSave.json", "w") as json_file:
        json.dump(warpsLista, json_file)
      await self.highrise.send_whisper(
          user_id,
          f"se ha creado el teleport '{warpname}' en tu ubicación para el rol '{rol}'"
      )

  else:
    # Si la sala_id no existe en warpsLista, crea una nueva entrada
    warpsLista[room_id] = [{'name': warpname, 'rol': rol, 'pos': pos}]
    with open("Json/warpsListaSave.json", "w") as json_file:
      json.dump(warpsLista, json_file)
    await self.highrise.send_whisper(
        user_id,
        f"se ha creado el teleport '{warpname}' en tu ubicación para el rol '{rol}'"
    )


class Bot(BaseBot):

  async def on_start(self, session_metadata: SessionMetadata) -> None:
    global owner_id, bot_id, bot_name, puerta_pos, carcelPos, owner_name, botspawnPos, caraAngulo, warpsLista, vipList, adminsList, banList, modsList, room_id
    print("-Bot iniciado-")
    bot_id = session_metadata.user_id
    room_users = await self.highrise.get_room_users()
    for room_user, position in room_users.content:
      if room_user.id == bot_id:
        bot_name = room_user.username
        puerta_pos = position
        carcelPos = puerta_pos
        break

    variables = cargar_variables()
    carcelPos = (variables['carcelPosSave'])
    variables = cargar_variables()
    vipList = (variables['vipListSave'])
    variables = cargar_variables()
    adminsList = (variables['adminsListSave'])
    variables = cargar_variables()
    modsList = (variables['modListSave'])
    variables = cargar_variables()
    banList = (variables['banListSave'])
    variables = cargar_variables()
    room_id = (variables['room_idSave'])

    try:
      if room_id in botspawnPos:
        x, y, z, caraAngulo = botspawnPos[room_id]
      else:
        x = puerta_pos.x
        y = puerta_pos.y
        z = puerta_pos.z
        caraAngulo = puerta_pos.facing
    except Exception:
      x = puerta_pos.x
      y = puerta_pos.y
      z = puerta_pos.z
      caraAngulo = puerta_pos.facing
      botspawnPos = {}
      pass
    try:
      vipList = eval(vipList)
    except Exception:
      pass
    try:
      adminsList = eval(adminsList)
    except Exception:
      pass
    try:
      modsList = eval(modsList)
    except Exception:
      pass
    try:
      banList = eval(banList)
    except Exception:
      pass

    async def send_continuous_random_emotes_in_dance_floor():
      global dance_floor_tiempo, botDanceState
      emote_id = "emote-zombierun"
      while True:
        if room_id in danceFloorCoordenadas:
          status = danceFloorCoordenadas[room_id]["status"]
          if status:
            try:
              min_x = danceFloorCoordenadas[room_id]["min_x"]
              min_y = danceFloorCoordenadas[room_id]["min_y"]
              min_z = danceFloorCoordenadas[room_id]["min_z"]
              max_x = danceFloorCoordenadas[room_id]["max_x"]
              max_y = danceFloorCoordenadas[room_id]["max_y"]
              max_z = danceFloorCoordenadas[room_id]["max_z"]

              if dance_floor_tiempo <= 0 and dance_floor_status:
                emote_nombre = random.choice(list(listReset.keys()))
                dance_floor_tiempo = listReset[emote_nombre]['tiempo']
                emote_id = listReset[emote_nombre]['id']
                room_users = await self.highrise.get_room_users()
                for user, position in room_users.content:
                  try:
                    if isinstance(position, Position):
                      x = position.x
                      y = position.y
                      z = position.z
                    elif isinstance(position, AnchorPosition):
                      # Handle AnchorPosition differently if needed
                      continue  # Skip processing for AnchorPosition for now
                    else:
                      # Unexpected type, skip processing
                      continue
                  # Check if the user's position is within the defined box-shaped region
                    if ((min_x <= x <= max_x and min_y <= y <= max_y
                         and min_z <= z <= max_z)
                        or (max_x <= x <= min_x and max_y <= y <= min_y
                            and max_z <= z <= min_z)):
                      if user.id == bot_id:
                        botDanceState = False
                      await self.highrise.send_emote(emote_id, user.id)
                  except Exception:
                    pass
              dance_floor_tiempo -= 0.5

            except Exception:
              pass
        await asyncio.sleep(0.5)

    async def danceBotBucle():
      global Botemotetime
      while True:
        if botDanceState:
          if Botemotetime <= 0:
            if BotDanceBaile == "random":
              
              nombre_emote, id_emote, duracion_emote = obtener_emote_aleatorio()
              Botemotetime = duracion_emote
              await self.highrise.send_emote(id_emote)
            else:
              
              await self.highrise.send_emote(BotDanceBaile)
              Botemotetime = BotemoteTimerest
          else:
            Botemotetime -= 0.5
        await asyncio.sleep(0.5)

    async def avisobot():
      while True:
        await asyncio.sleep(loopAnuncioSeg)
        if loopAnuncio != "stop":
          await self.highrise.chat(loopAnuncio)

    async def start_dance_casual():
      global dancing_users, roomUsersGlobalVar
      while True:
        segureList = dict(dancing_users)
        for user_id, user_data in segureList.items():
          try:
            emote = user_data["emote"]
            status = user_data["status"]
            tiempo = user_data["tiempo"]

            if status:
              if tiempo <= 0:
                await self.highrise.send_emote(emote, user_id)
                tiempoReset = 0
                id_buscar = emote
                for emote, info in listReset.items():
                  if info['id'] == id_buscar:
                    tiempoReset = info['tiempo']

                dancing_users[user_id]["tiempo"] = tiempoReset
              else:
                tiempo -= 0.5  # Restar 0.5 al tiempo si no es menor o igual a cero
                dancing_users[user_id][
                    "tiempo"] = tiempo  # Actualizar el tiempo en el diccionario
                #print(dancing_users)
            # Si status es False, el código no envía el emote y continúa con el siguiente usuario.

          except:
            if user_id in dancing_users:
              del dancing_users[user_id]
            pass  # Manejar las excepciones según sea necesario
        roomUsersGlobalVar = await self.highrise.get_room_users()
        await asyncio.sleep(0.5)

    async def carcelLoop():
      global carcelList
      while True:
        if carcelList:
          segureList = dict(carcelList)
          for user_id, user_data in segureList.items():
            try:
              tiempovar = user_data["tiempo"]
              username = user_data["nombre"]

              if tiempovar <= 0:
                if user_id in carcelList:
                  await self.highrise.teleport(user_id, puerta_pos)
                  del carcelList[user_id]
                  await self.highrise.chat(
                      f"Ya eres libre @{username}! portate bien! 👮")
                  await self.highrise.react("thumbs", user_id)
                pass

              else:
                tiempovar -= 1
                carcelList[user_id]["tiempo"] = tiempovar

            except:
              if user_id in carcelList:
                del carcelList[user_id]
              pass
       
        await asyncio.sleep(1)

    async def vipLoop():
      global vipList
      segundos = 0
      segundosAnuncio = 0
      while True:
        if vipList:
          segureList = dict(vipList)
          for user_name, user_time in segureList.items():
            try:
              tiempo = user_time
              nombre = user_name
              if tiempo == 1:
                if nombre in vipList:
                  del vipList[nombre]
                pass
              elif tiempo >= 2:
                tiempo -= 1
                vipList[nombre] = tiempo
            except Exception:
              pass
          segundos += 1
          segundosAnuncio += 1
          if segundos == 60:
            segundos = 0
            guardar = {'vipListSave': vipList}
            guardar_variables(guardar)
          if segundosAnuncio == 120:
            segundosAnuncio = 0
            if vipstate:
              await self.highrise.chat(
                "obten VIP usa /vip para mas informacion!."
              )
        await asyncio.sleep(1)

    async def tiptimebucle():
      global tiptime
      segundos = 0
      while True:
        if tipstate:
          segundos += 1
          if segundos == 60:
            segundos = 0
            tiptime = int(tiptime)
            tiptime -= 1
            cantidad_a_tipo = {
                1: "gold_bar_1",
                5: "gold_bar_5",
                10: "gold_bar_10",
                50: "gold_bar_50",
                100: "gold_bar_100",
                500: "gold_bar_500",
                1000: "gold_bar_1k",
                5000: "gold_bar_5000",
                10000: "gold_bar_10k",
            }
            if tiptime <= 0:
              tiptime = tiptimerestaurar
              wallet = (await self.highrise.get_wallet()).content
              oroDisponible = wallet[0].amount
              tipo_barra_de_oro = cantidad_a_tipo.get(int(tipcantidad))
              wallet = (await self.highrise.get_wallet()).content
              oroDisponible = wallet[0].amount
              room_users_response = await self.highrise.get_room_users()
              room_users = room_users_response.content
              num_users_total = len(room_users)
              room_users = [(user, position) for user, position in room_users
                            if user.username not in [owner_name, bot_name]]
              parteLimit = tipLimitUserTip
              if parteLimit <= 0:
                parteLimit = len(room_users)
              if len(room_users) > int(parteLimit):
                random_users = random.sample(room_users, int(parteLimit))

              else:
                random_users = room_users
              num_users = len(room_users)
              NumUserTip = len(random_users)
              if num_users_total < tipMinRequerido:
                #no hay suficientes usuarios para dar tips
                return
              else:

                #se suma la comision dependiendo de la cantidad
                parteCantidad = int(tipcantidad)
                oroSolicitado = NumUserTip * int(parteCantidad)
                numeros_validos = {1, 5, 10, 50, 100, 500, 1000, 5000, 10000}
                if int(parteCantidad) in numeros_validos:
                  oroSolicitado += NumUserTip
                elif int(parteCantidad) == 50:
                  oroSolicitado += 5 * NumUserTip
                elif int(parteCantidad) == 100:
                  oroSolicitado += 10 * NumUserTip
                elif int(parteCantidad) == 500:
                  oroSolicitado += 50 * NumUserTip
                elif int(parteCantidad) == 1000:
                  oroSolicitado += 100 * NumUserTip
                elif int(parteCantidad) == 5000:
                  oroSolicitado += 500 * NumUserTip
                else:
                  oroSolicitado += 1000 * NumUserTip

                if oroDisponible >= oroSolicitado:
                  if len(room_users) > parteLimit:

                    try:
                      await self.highrise.send_whisper(
                          owner_id,
                          f"se enviará {parteCantidad}g a {NumUserTip} usuarios al azar."
                      )
                    except Exception:
                      pass

                  else:
                    try:
                      await self.highrise.send_whisper(
                          owner_id,
                          f"se enviará {parteCantidad}g a {NumUserTip} usuarios."
                      )
                    except Exception:
                      pass
                  await asyncio.sleep(2)
                  for user, _ in random_users:
                    tip_user_id = user.id
                    user_name = user.username
                    try:
                      await self.highrise.tip_user(tip_user_id,
                                                   tipo_barra_de_oro)
                      await self.highrise.chat(
                          f"{parteCantidad}g enviado a {user_name}")
                    except Exception:
                      pass
                    await asyncio.sleep(1)
                else:
                  try:
                    await self.highrise.send_whisper(
                        owner_id,
                        f"Bot sin fondos, se intento enviar autotip, tienes {oroDisponible}g y necesitas {oroSolicitado}g"
                    )
                  except Exception:
                    pass

        await asyncio.sleep(1)

    asyncio.create_task(avisobot())
    asyncio.create_task(start_dance_casual())
    asyncio.create_task(tiptimebucle())
    asyncio.create_task(carcelLoop())
    asyncio.create_task(vipLoop())
    asyncio.create_task(send_continuous_random_emotes_in_dance_floor())

    await self.highrise.set_outfit(outfit=[
        Item(type='clothing',
             amount=1,
             id='body-flesh',
             account_bound=False,
             active_palette=0),
        Item(type='clothing',
             amount=1,
             id='eye-n_basic2018malesquaresleepy',
             account_bound=False,
             active_palette=7),
        Item(type='clothing',
             amount=1,
             id='eyebrow-n_basic2018newbrows07',
             account_bound=False,
             active_palette=0),
        Item(type='clothing',
             amount=1,
             id='nose-n_basic2018newnose05',
             account_bound=False,
             active_palette=0),
        Item(type='clothing',
             amount=1,
             id='mouth-basic2018chippermouth',
             account_bound=False,
             active_palette=-1),
        Item(type='clothing',
             amount=1,
             id='glasses-n_starteritems201roundframesbrown',
             account_bound=False,
             active_palette=-1),
        Item(type='clothing',
             amount=1,
             id='bag-n_room32019sweaterwrapblack',
             account_bound=False,
             active_palette=-1),
        Item(type='clothing',
             amount=1,
             id='shirt-n_starteritems2019tankwhite',
             account_bound=False,
             active_palette=-1),
        Item(type='clothing',
             amount=1,
             id='shorts-f_pantyhoseshortsnavy',
             account_bound=False,
             active_palette=-1),
        Item(type='clothing',
             amount=1,
             id='shoes-n_whitedans',
             account_bound=False,
             active_palette=-1),
    ])
    await self.highrise.teleport(bot_id, Position(x, y, z, facing=caraAngulo))
    await self.highrise.chat("Hola a todos!")
    await asyncio.sleep(0.5)
    await self.highrise.walk_to(Position(x, y, z, facing=caraAngulo))
    if not vipstate:
      await self.highrise.chat(
          "[aviso] los teleports para VIP están desactivados, usa /vip active, para activarlo."
      )
    if tipstate:
      await self.highrise.chat(
          f"Los tips automaticos estan activados, se enviará {tipcantidad}g a {tipLimitUserTip} usuarios cada {tiptimerestaurar} minutos cuando hayan {tipMinRequerido} o mas en la sala."
      )
      await self.highrise.chat(
          f"\n /autotip stop, para desactivarlo\n/autotip, para ver mas configuraciones."
      )
    await asyncio.sleep(0.5)
    asyncio.create_task(danceBotBucle())

  async def on_emote(self, user: User, emote_id: str,
                     receiver: User | None) -> None:
    """On a received emote."""
    #print(emote_id, user.username)

  async def on_tip(self, sender: User, receiver: User,
                   tip: CurrencyItem | Item) -> None:
    if receiver.username == bot_name:
      mensaje = ""
      corazones = 0
      buytime = -1
      if tip.amount == 1:
        mensaje = "tacañ@ 😒"
        corazones = 1
      elif tip.amount == 5:
        mensaje = "te quiero 💖"
        corazones = 3
      elif tip.amount == 10:
        mensaje = "nada mal 😉"
        corazones = 5
        buytime = 86400
      elif tip.amount == 50:
        mensaje = "se ve que me quieres 🥺"
        corazones = 10
        buytime = 604800
      elif tip.amount == 100:
        mensaje = "me amas admitelo 😏"
        corazones = 20
        buytime = 2592000
      elif tip.amount == 500:
        mensaje = "me enamore 😍"
        corazones = 30
        buytime = 373248000
      else:
        mensaje = "hazme un hijo 😳"
        corazones = 60
        buytime = 0
      await self.highrise.chat(
          f"{sender.username} gracias por tu donacion de {tip.amount}g! {mensaje}"
      )
      if not owner_name == sender.username and not sender.username in adminsList and not sender.username in modsList:
        if buytime >= 0:
          if sender.username in vipList:
            time_left = vipList[sender.username]
            if time_left == 0:
              await self.highrise.chat(
                  f"@{sender.username}! ya tenias VIP permanente!")
              return
            time_left += buytime
            dias, horas, minutos, segundos = convertir_tiempo(time_left)
            if dias == 0:
              message = f"{horas}h {minutos}m"
            else:
              message = f"{dias}d {horas}h {minutos}m"

            vipList[sender.username] = time_left
            guardar = {'vipListSave': vipList}
            guardar_variables(guardar)

            await self.highrise.chat(
                f"Felicidades {sender.username}! VIP actualizado! ahora tienes:\n{message} de VIP!"
            )
          else:
            vipList[sender.username] = buytime
            guardar = {'vipListSave': vipList}
            guardar_variables(guardar)
            dias, horas, minutos, segundos = convertir_tiempo(buytime)
            if buytime == 0:
              await self.highrise.chat(
                  f"@{sender.username} Felicidades {sender.username}! ahora tienes VIP permanente!"
              )
              return
            if dias == 0:
              message = f"{horas}h {minutos}m"
            else:
              message = f"{dias}d {horas}h {minutos}m"
            await self.highrise.chat(
                f"Felicidades @{sender.username} ahora tienes VIP por:\n{message}!\nusa /vip para ver tus beneficios y tiempo restante."
            )

      for i in range(corazones):
        await self.highrise.react("heart", sender.id)
        await asyncio.sleep(0.2)

  async def on_user_leave(self, user: User) -> None:
    global nombreParaSeguir, botDanceState, Botemotetime
    if user.username == nombreParaSeguir:
      nombreParaSeguir = ""
      botDanceState = True
      Botemotetime = 0

  async def on_user_join(self, user: User,
                         position: Position | AnchorPosition) -> None:
    global carcelAuto

    if user.username in banList:
      room_users = (await self.highrise.get_room_users()).content
      user_info = [(usr.username, usr.id) for usr, _ in room_users]
      verificar = False
      user_id = ""
      for username, uid in user_info:
        if username == user.username:
          verificar = True
          user_id = uid
          break
      if verificar:
        try:
          await self.highrise.moderate_room(user_id, "kick")
          return
        except Exception:
          return
      return

    await self.highrise.react("wave", user.id)
    try:
      await self.highrise.send_whisper(user.id, welcomeText.format(user=user))
    except Exception:
      try:
        await self.highrise.send_whisper(
            owner_id,
            "mensaje bienvenida demaciado largo, usa /welcome [mensaje] para cambiar el mensaje de bienvenida."
        )
      except Exception:
        pass

    myid = user.id
    myname = user.username
    segureList = dict(carcelList)
    for user_id, user_data in segureList.items():
      try:
        if myid == user_id:
          vartiempo = user_data["tiempo"]
          name = user_data["nombre"]
          partesA = str(carcelPos).replace('[', '').replace(']', '')
          partes = partesA.split(',')
          x = float(partes[0].strip())
          y = float(partes[1].strip())
          z = float(partes[2].strip())
          horas = vartiempo // 3600
          minutos = (vartiempo % 3600) // 60
          segundos = vartiempo % 60
          if vartiempo >= 3600:
            await self.highrise.chat(
                f"@{name.upper()} aun te quedan {horas}h {minutos}m {segundos}s en la cárcel bandid@! 👮"
            )

          elif vartiempo >= 60:
            await self.highrise.chat(
                f"@{name.upper()} aun te quedan {minutos}m {segundos}s en la cárcel bandid@! 👮"
            )

          else:
            await self.highrise.chat(
                f"@{name.upper()} aun te quedan {segundos}s en la cárcel bandid@! 👮"
            )
          await self.highrise.teleport(myid,
                                       Position(x, y, z, facing='FrontLeft'))
          return
      except:
        pass
    if carcelAuto:
      if not myid == owner_id:
        enter_user_carcel(myid, 30 * 60, myname)

        partesA = str(carcelPos).replace('[', '').replace(']', '')
        partes = partesA.split(',')
        x = float(partes[0].strip())
        y = float(partes[1].strip())
        z = float(partes[2].strip())

        await self.highrise.chat(
            f"@{myname.upper()} estarás encerrad@ por 30 min 👮")
        try:
          await self.highrise.teleport(myid, Position(x,
                                                      y,
                                                      z,
                                                      facing='FrontLeft'))
        except:
          pass
        with open("Json/carcelListSave.json", "w") as json_file:
          json.dump(carcelList, json_file)
          

  #CONFESIONES
  async def on_whisper(self, user: User, message: str) -> None:
    #await self.highrise.chat(message)
    #print(f"[WHISPER] {user.username} {message}")
    
    if any(message.lower().startswith(prefix)
       for prefix in ["/help", "!help"]):
     await com_help(self, user, message)

    if any(message.lower().startswith(prefix)
       for prefix in ["/room", "!room"]):
     await com_room(self, user, message)

    if any(message.lower().startswith(prefix)
       for prefix in ["/dancefloor", "!dancefloor"]):
      await com_dancefloor(self, user, message)

    if any(message.lower().startswith(prefix)
       for prefix in ["/loop", "!loop"]):
      await com_loop(self, user, message)

    if any(message.lower().startswith(prefix)
       for prefix in ["/welcome", "!welcome"]):
     await com_welcome(self, user, message)

    if any(message.lower().startswith(prefix) for prefix in [
    "/wallet", "!wallet", "/billetera", "!billetera", "/dinero", "!dinero"
    ]):
     await com_wallet(self, user, message)

    if any(message.lower().startswith(prefix) for prefix in ["/tip", "!tip"]):
     await com_tip(self, user, message)

    if message.lower().startswith("/autotip"):
      await com_autotip(self, user, message)

    if "/follow" in message.lower():
     await com_follow(self, user, message)

    if "/follow stop" in message.lower():
     await com_follow_stop(self, user, message)

    if any(message.lower().startswith(prefix)
       for prefix in ["/future", "!future"]):
      await com_future(self, user, message)

    if any(message.lower().startswith(prefix)
       for prefix in ["/bot emote", "!bot emote"]):
      await com_bot_emote(self, user, message)

    if any(message.lower().startswith(prefix)
       for prefix in ["/emote all", "!emote all"]):
      await com_emote_all(self, user, message)

    if any(message.lower().startswith(prefix)
       for prefix in ["/match", "!match"]):
     await com_match(self, user, message)

    if any(message.lower().startswith(prefix)
       for prefix in ["/battle", "!battle"]):
     await com_battle(self, user, message)

    if any(message.lower().startswith(prefix)
       for prefix in ["/joke", "!joke"]):
      await com_joke(self, user, message)

    if any(message.lower().startswith(prefix)
       for prefix in ["/death", "!death"]):
     await com_death(self, user, message)

    if any(message.lower().startswith(prefix)
       for prefix in ["/jail", "!jail"]):
     await com_jail(self, user, message)

    if any(message.lower().startswith(prefix)
       for prefix in ["/setjail", "!setjail"]):
     await com_setjail(self, user, message)

    if any(message.lower().startswith(prefix)
       for prefix in ["/bot spawn", "!bot spawn"]):
     await com_bot_spawn(self, user, message)

    if any(message.lower().startswith(prefix)
       for prefix in ["/tele", "!tele", "/tp", "!tp"]):
     await com_tele(self, user, message)

    if any(message.lower().startswith(prefix)
       for prefix in ["/admin", "!admin"]):
      await com_admin(self, user, message)

    if any(message.lower().startswith(prefix) for prefix in ["/vip", "!vip"]):
     await com_vip(self, user, message)

    if any(message.lower().startswith(prefix) for prefix in ["/mod", "!mod"]):
     await com_mod(self, user, message)

    if any(message.lower().startswith(prefix)
       for prefix in ["/kick", "!kick"]):
     await com_kick(self, user, message)

    if any(message.lower().startswith(prefix) for prefix in ["/ban", "!ban"]):
     await com_ban(self, user, message)

    if any(message.lower().startswith(prefix)
       for prefix in ["/mute", "!mute"]):
     await com_mute(self, user, message)

    if message.lower().startswith(("/invite", "!nvite")):
      await com_invite(self, user, message)

    if message.lower().startswith(("/emote list", "!emote list")):
       await com_emote_list(self, user, message)

    if message.lower().startswith(("/heart", "!heart")):
       await com_heart(self, user, message)

    if message.lower().startswith(("/emote", "!emote")):
       await com_emote(self, user, message)

    if message.lower().startswith(("/summon", "!summon")):
       await com_summon(self, user, message)

  async def on_message(self, user_id: str, conversation_id: str, is_new_conversation: bool) -> None:
    global inviteList
    response = await self.highrise.get_messages(conversation_id)
    if isinstance(response, GetMessagesRequest.GetMessagesResponse):
        message = response.messages[0].content
      
    if any(message.lower().startswith(prefix)
       for prefix in ["/sub", "!sub"]):
        if user_id not in inviteList:
          inviteList.append(user_id)
          with open("Json/inviteListSave.json", "w") as json_file:
            json.dump(inviteList, json_file)
          await self.highrise.send_message(conversation_id, "ahora estás suscrito para recibir mensajes!\n/unsub - para dejar de recibir mensajes.")
        else:
          await self.highrise.send_message(conversation_id, "ya estabas suscrito!\n/unsub - para dejar de recibir mensajes.")
      
    if any(message.lower().startswith(prefix)
       for prefix in ["/unsub", "!unsub"]):
        if user_id in inviteList:
          inviteList.remove(user_id)
        with open("Json/inviteListSave.json", "w") as json_file:
          json.dump(inviteList, json_file)
        await self.highrise.send_message(conversation_id, "Listo dejarás de recibir mensajes!\n para recibir mensajes nuevamente usa /sub")

  async def on_chat(self, user: User, message: str) -> None:
    global tiptimerestaurar, tiptime, tipstate, tipcantidad, loopAnuncio, \
     nombreParaSeguir, dancing_users, owner_name, carcelList, carcelPos, \
     bot_name, carcelAuto, adminsList, caraAngulo, BotDanceBaile, \
     Botemotetime, BotemoteTimerest, Game1num, Game1Status, \
     vipList, warpsLista,  botspawnPos, tipMinRequerido, tipLimitUserTip, botDanceState, Botemotetime
    """En un chat recibido en toda la sala."""
    if message.lower().startswith("/id"):
      room_users = (await self.highrise.get_room_users()).content
      users_info = "\n".join(
          [f"{user.username} {user.id}" for user, _ in room_users])
      print(users_info)


    if message.startswith("/usuarios"):
      room_users = (await self.highrise.get_room_users()).content
      user_names = [user.username for user, _ in room_users]
      for name in user_names:
        print(name)

    if "/poses" in message.lower():
      await self.highrise.send_whisper(
          user.id,
          "kiss sad wave tired angry thumb lust cursing greedy flex gagg celebrate bow curtsy hot confused super cute pose7 pose8 pose1 pose3 pose5 cute"
      )

    if any(message.lower().startswith(prefix)
           for prefix in ["/help", "!help"]):
      await com_help(self, user, message)

    if any(message.lower().startswith(prefix)
           for prefix in ["/room", "!room"]):
      await com_room(self, user, message)

    if any(message.lower().startswith(prefix)
           for prefix in ["/dancefloor", "!dancefloor"]):
      await com_dancefloor(self, user, message)

    if any(message.lower().startswith(prefix)
           for prefix in ["/loop", "!loop"]):
      await com_loop(self, user, message)

    if any(message.lower().startswith(prefix)
           for prefix in ["/welcome", "!welcome"]):
      await com_welcome(self, user, message)

    if any(message.lower().startswith(prefix) for prefix in [
        "/wallet", "!wallet", "/billetera", "!billetera", "/dinero", "!dinero"
    ]):
      await com_wallet(self, user, message)

    if any(message.lower().startswith(prefix) for prefix in ["/tip", "!tip"]):
      await com_tip(self, user, message)

    if message.lower().startswith("/autotip"):
      await com_autotip(self, user, message)

    if "/follow" in message.lower():
      await com_follow(self, user, message)

    if "/follow stop" in message.lower():
      await com_follow_stop(self, user, message)

    if any(message.lower().startswith(prefix)
           for prefix in ["/future", "!future"]):
      await com_future(self, user, message)

    if any(message.lower().startswith(prefix)
           for prefix in ["/bot emote", "!bot emote"]):
      await com_bot_emote(self, user, message)

    if any(message.lower().startswith(prefix)
           for prefix in ["/emote all", "!emote all"]):
      await com_emote_all(self, user, message)

    if any(message.lower().startswith(prefix)
           for prefix in ["/match", "!match"]):
      await com_match(self, user, message)

    if any(message.lower().startswith(prefix)
           for prefix in ["/battle", "!battle"]):
      await com_battle(self, user, message)

    if any(message.lower().startswith(prefix)
           for prefix in ["/joke", "!joke"]):
      await com_joke(self, user, message)

    if any(message.lower().startswith(prefix)
           for prefix in ["/death", "!death"]):
      await com_death(self, user, message)

    if any(message.lower().startswith(prefix)
           for prefix in ["/jail", "!jail"]):
      await com_jail(self, user, message)

    if any(message.lower().startswith(prefix)
           for prefix in ["/setjail", "!setjail"]):
      await com_setjail(self, user, message)

    if any(message.lower().startswith(prefix)
           for prefix in ["/bot spawn", "!bot spawn"]):
      await com_bot_spawn(self, user, message)

    if any(message.lower().startswith(prefix)
           for prefix in ["/tele", "!tele", "/tp", "!tp"]):
      await com_tele(self, user, message)

    if any(message.lower().startswith(prefix)
           for prefix in ["/admin", "!admin"]):
      await com_admin(self, user, message)

    if any(message.lower().startswith(prefix) for prefix in ["/vip", "!vip"]):
      await com_vip(self, user, message)

    if any(message.lower().startswith(prefix) for prefix in ["/mod", "!mod"]):
      await com_mod(self, user, message)

    if any(message.lower().startswith(prefix)
           for prefix in ["/kick", "!kick"]):
      await com_kick(self, user, message)

    if any(message.lower().startswith(prefix) for prefix in ["/ban", "!ban"]):
      await com_ban(self, user, message)

    if any(message.lower().startswith(prefix)
           for prefix in ["/mute", "!mute"]):
      await com_mute(self, user, message)

    if message.lower().startswith(("/invite", "!invite")):
      await com_invite(self, user, message)
      
    if message.lower().startswith(("/emote list", "!emote list")):
       await com_emote_list(self, user, message)

    if message.lower().startswith(("/heart", "!heart")):
       await com_heart(self, user, message)

    if message.lower().startswith(("/emote", "!emote")):
       await com_emote(self, user, message)

    if message.lower().startswith(("/summon", "!summon")):
       await com_summon(self, user, message)
      
    #enviar emotes
    if message in listReset:
      launch_info = listReset[message]
      emote_id = launch_info['id'].lower()
      enter_user_list(user.id, emote_id, 0)

    # Comando para detener el baile casual para el usuario actual
    if message.lower().startswith("stop"):
      if user.id in dancing_users and dancing_users[user.id]:
        del dancing_users[user.id]
        await self.highrise.send_emote("emote-hot", user.id)
    #-------
    if "besote" in message.lower() or "beso" in message.lower(
    ) or "besito" in message.lower() or "muak" in message.lower():

      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-kiss"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass

      await asyncio.sleep(2)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/no" in message.lower() or "no quiero" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-no"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass

      await asyncio.sleep(2)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "tristesa" in message.lower() or "estoy triste" in message.lower(
    ) or "toy triste" in message.lower() or "estoy sad" in message.lower(
    ) or "toy sad" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-sad"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass

      await asyncio.sleep(4)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "yes" in message.lower() or "si te creo" in message.lower(
    ) or "sisi" in message.lower() or "sii" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-yes"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass

      await asyncio.sleep(2)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/laughing" in message.lower() or "jaja" in message.lower(
    ) or "jask" in message.lower() or "jkj" in message.lower(
    ) or "ajaj" in message.lower() or "jsjs" in message.lower(
    ) or "jsk" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-laughing"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass

      await asyncio.sleep(2)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if (message.lower().startswith("/hello") or
        message.lower().startswith("hola") or message.lower().startswith("ola")
        or message.lower().startswith("o  li")) and not (
            "ola guap" in message.lower() or "oli guap" in message.lower()):
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-hello"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass

      await asyncio.sleep(2)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0

    #-------
    if "que verguenza" in message.lower() or "soy timido" in message.lower(
    ) or "soy timida" in message.lower() or "me da pena" in message.lower(
    ) or "me da penita" in message.lower() or "soy tímido" in message.lower(
    ) or "soy tímida" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-shy"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass

      await asyncio.sleep(4)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "que flojera" in message.lower() or "tengo sueño" in message.lower(
    ) or "tengo pereza" in message.lower() or "tengo flojera" in message.lower(
    ):
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-tired"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(4)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "malote" in message.lower() or "muy mal" in message.lower(
    ) or "que malo" in message.lower() or "que mala" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emoji-angry"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(5)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/sit" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "idle-loop-sitfloor"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(2)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "vale" in message.lower() or message.lower().startswith("ok"):
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emoji-thumbsup"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(2)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "ola hermoz" in message.lower() or "hola guap" in message.lower(
    ) or "ola guap" in message.lower() or "hola lind" in message.lower(
    ) or "ola lind" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-lust"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(4)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "ptm" in message.lower() or "rayos" in message.lower(
    ) or "mrd" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emoji-cursing"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(3)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "que raro" in message.lower() or "sospechoso" in message.lower(
    ) or "que extraño" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-greedy"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(5)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "asi es" in message.lower() or "así es" in message.lower(
    ) or "lo lograr" in message.lower() or "tu puedes" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emoji-flex"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(1)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "wakala" in message.lower() or "asco" in message.lower(
    ) or "asquero" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emoji-gagging"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(5)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "celebra" in message.lower() or "yupi" in message.lower(
    ) or "yey" in message.lower() or "estoy feliz" in message.lower(
    ) or "wujuu" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emoji-celebrate"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(3)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/model" in message.lower() or "soy guapo" in message.lower(
    ) or "soy guapa" in message.lower() or "que bello soy" in message.lower(
    ) or "que bella soy" in message.lower(
    ) or "que guapo soy" in message.lower(
    ) or "que guapa soy" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-model"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(6)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/penny" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "dance-pennywise"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(1)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "de nada" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-bow"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(2)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "el placer es" in message.lower() or "un placer" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-curtsy"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(2)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
        #-------
    if "/snowball" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-snowball"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(4)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "cansad" in message.lower() or "que calor" in message.lower(
    ) or "hace calor" in message.lower() or "tengo calor" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-hot"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(3)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/angel" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-snowangel"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(5)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "confundid" in message.lower() or "nose" in message.lower(
    ) or "nidea" in message.lower() or "que se yo" in message.lower(
    ) or "no lo se" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-confused"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(8)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/enth" in message.lower() or "encerio" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "idle-enthusiastic"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(9)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/teleport" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-teleporting"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(11)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/maniac" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-maniac"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(4)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if ("que lind" in message.lower() and "que hermo" not in message.lower()):
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-cute"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(6)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "entendido" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-pose1"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(2)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/pose3" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-pose3"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(4)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/pose5" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-pose5"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(4)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/cutey" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-cutey"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(3)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/zombie" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-zombierun"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(9)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/fashion" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-fashionista"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(5)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/gravity" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-gravity"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(7)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/uwu" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "idle-uwu"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(15)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0

    #FRASES RAPIDAS

    #insulto al bot
    if "bot feo" in message.lower():
      response = random.choice([
          f"tu cola {user.username} 😠",
          f"que dices {user.username} yo soy hermoso 😌",
          f"fe@ tu {user.username} 😠"
      ])
      await self.highrise.chat(response)

    if "bot lindo" in message.lower() or "bot guapo" in message.lower():
      response = random.choice([
          f"me sonrojas {user.username} 🥰",
          f"tu tambien lo eres {user.username} ❤️",
          f"gracias {user.username} lo se 🤗"
      ])
      await self.highrise.chat(response)

    if "bot gay" in message.lower() or "bot tonto" in message.lower(
    ) or "bot weon" in message.lower() or "pinche bot" in message.lower(
    ) or "bot pendejo" in message.lower() or "bot mamahuevo" in message.lower(
    ):
      response = random.choice([
          f"tu mismo {user.username} 😠", f"tu mama será {user.username}",
          f"no me cuentes tus verdades {user.username} "
      ])
      await self.highrise.chat(response)

  #insulto al bot 2
    if "te odio bot" in message.lower() or "bot te odio" in message.lower():
      response = random.choice([
          f"Yo te quiero mucho {user.username}",
          f"Yo tambien te odio {user.username}",
          f"Por que tanto odio {user.username}?"
      ])
      await self.highrise.chat(response)

      #te amo bot
    if "te amo bot" in message.lower() or "bot te amo" in message.lower(
    ) or "bot te quiero" in message.lower(
    ) or "te quiero bot" in message.lower():
      if user.username == "xMissJeanx":
        await self.highrise.chat(
            f"Yo tambien te amo {user.username} mi unica bebe ♥️")
      else:
        await self.highrise.chat(f"Yo tambien te amo {user.username} ♥️")

    #GAME
    if "/game" in message.lower():
      if not Game1Status:
        await self.highrise.chat("intenta adivinar el numero del 1 al 100!")
        Game1num = random.randint(1, 100)
        Game1Status = True
      else:
        await self.highrise.chat("Ya hay un juego en curso")

    if Game1Status == True and message.isdigit():

      respnump = int(message)
      cercania = abs(Game1num - respnump)
      if cercania <= 10:
        emoji = "🔥"
      else:
        emoji = "❄️"
      if Game1num == respnump:
        await self.highrise.chat(
            f"correcto @{user.username} el numero era {respnump} ✅")
        for i in range(3):
          await self.highrise.react("thumbs", user.id)
          await asyncio.sleep(0.4)

        Game1Status = False
      elif Game1num < respnump:
        await self.highrise.send_whisper(user.id, f"{respnump} 👇{emoji}")
      else:
        await self.highrise.send_whisper(user.id, f"{respnump} 👆{emoji}")

    if "/r" in message.lower():
      await self.highrise.chat(
          "para jugar envía 5g o 10g a uno de los anfitriones, di un numero del 1 al 6 y se lanzaran los 2 dados, si aparece tu numero ganas el doble!"
      )


   
  
  #CHISTES

    if "bot cuentame un chiste" in message.lower(
    ) or "bot dime un chiste" in message.lower(
    ) or "bot cuéntame un chiste" in message.lower(
    ) or "/chiste" in message.lower() or "bot hazme reir" in message.lower():
      response = random.choice([
          "- Mamá, mamá, los spaghetti se están pegando. 😳 - Déjalos que se maten 😈",
          "Un pez le pregunta a otro pez: ¿qué hace tu mamá? 😳 Este le contesta: Nada 😐 ¿y la tuya qué hace? Nada también.😂",
          "Si se muere una pulga, ¿a dónde va? 😳 Al pulgatorio.😂",
          "A Juanito le dice la maestra: Juanito, ¿qué harías si te estuvieses ahogando en la piscina? 😳 Juanito le responde: Llorar para desahogarme profe 😎",
          "Hijo, me veo gorda, fea y vieja. ¿qué tengo? 😔 Mamá, tienes toda la razón 😂",
          "Camarero, ese filete tiene muchos nervios 🤨 -Pues normal, es la primera vez que se lo comen 😂",
          "Mi humor es tan negro que le disparaba la policia 😳",
          "Un marido le dice a su mujer: Apuesto a que no puedes decirme algo que me haga feliz y triste al mismo tiempo 😌 -Claro que si! tu pilin es más grande que la de tus hermanos 😎",
          "¿Qué hay que hacer para ampliar la libertad de una mujer? 🤔 ampliar la cocina! 😂 ok no me funen 😔",
          "Doctor, ¿qué me dijo antes? 🥺 ¿Géminis, Libra? 🤔 -Cáncer Andy cancer",
          "Mamá, mamá, el gato está malo 😔 -bueno lo apartas y te comes las patatas 🤗",
          "Papá, papá, en el colegio me pegan 😭 -Lo sé hijo, ya me enviaron el video de youtube 😂",
          "Una mujer se arrodilla a Orar: -Señor, si no puedo adelgazar, bendice a mis amigas con mucha comida y haz que engorden. Amén 😇",
          "Me acaba de picar una serpiente! 😫 - ¿Cobra? - No, gratis 😅",
          "Hola, ¿tienen libros para el cansancio? 🥺 - Sí, pero están agotados 😔",
          "– Doctor, me dan mucho miedo las multiplicaciones.\n- ¿Por?\n– Ayyyy!! 😱😖😖",
          "– Lo sentimos, pero está usted despedido.😤\n-Pero, ¿por qué?😭\n-Porque tarda mucho en entender las cosas.😠\n-Vale. ¿Pero puedo seguir viniendo a trabajar? 🥺",
          "– Vengo a presentar mi tesis. Se titula “Apatía, desgana y pereza en el marco de la sociedad actual 😊”.\nMuy bien. Adelante. Puede comenzar.🙂\nNo me apetece.😔\nBrillante.😲🤯",
          "Que ironía fue aquella vez que me golpearon con una enciclopedia y perdí el conocimiento.😔",
          "– ¿Señor por qué no se detuvo al escuchar las sirenas?🤨\n- Porque su canto conduce a los hombres a la muerte.🥺🥺\n- Sople aquí, por favor.🤦‍♂️",
          "– ¿Y tú qué haces?\nSoy deportista de alto rendimiento.😎\n¿En serio?😲\nSí, me rindo fácilmente 😌",
          "– ¿Cuál es su destino?🙂\nMi destino no está escrito aún.. Mi destino es un lienzo en blanco que estoy pintando con cada elección y acción que tomo a lo largo de mi vida..😌\nSeñor ¿quiere un boleto de tren o no?😡"
      ])

      await self.highrise.chat(response)

  async def on_channel(self, sender_id: str, message: str,
                       tags: set[str]) -> None:
    await self.highrise.chat(message)
    """En un mensaje de canal oculto."""

  #USUARIO SE MUEVE A UNA POSICION
  async def on_user_move(self, user: User,
                         pos: Position | AnchorPosition) -> None:
    """Cuando un usuario se mueve en la habitación."""
    if user.username == owner_name or user.username in adminsList or user.username in modsList or user.username in vipList:
      if not vipstate:
        if not (user.username == owner_name or user.username in adminsList
                or user.username in modsList):
          return
      for userName, Apos in roomUsersGlobalVar.content:
        if userName.id == user.id:
          try:
            if isinstance(pos, Position):
              if isinstance(Apos, Position):
                if abs(Apos.y - pos.y) >= 4:
                  await self.highrise.teleport(
                      user.id, Position(pos.x,
                                        pos.y,
                                        pos.z,
                                        facing='FrontLeft'))
          except:
            pass

    if user.username == nombreParaSeguir:
      if isinstance(pos, Position):  # Verificar si pos es de tipo Position
        try:
          await self.highrise.walk_to(
              Position(pos.x - 1, pos.y, pos.z - 1, pos.facing))
        except:
          pass


#65b33f88449aa3006dcd6ac2 YOSK 17, 0, 6
#64b8b8b8687948e776bf90dc lola 7, 0, 11
#64b997ef387197bbedca3986   casa
#6477963ef8787721cd711bcd   casino
#64b9cbc2a20c4d5c6ee252d0   baño
#6529a9fc95b6e0782557a416 BAÑO cata
#64ad72cb1cd195ff48d8a58a eurus dragon
#6570b63088f31769aa73efbd casa hernan
#65879452025531dd793da4b1 casa hernan 2
#65de1ff75bd46d66746719a0



