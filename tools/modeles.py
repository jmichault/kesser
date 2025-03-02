#!/usr/bin/env python3

# script de découverte des périphériques tuya
import tinytuya
import json
import os
import sys
import time

REGION=input("Région de votre compte tuya (eu pour europe, cn pour chine, ... ) : ")
APIKEY=input("votre ID tuya (Access ID) : ")
APISECRET=input("votre secret tuya (Access Secret) : ")
# Connexion au cloud tuya
try:
  c = tinytuya.Cloud(
                apiRegion=REGION,
                apiKey=APIKEY,
                apiSecret=APISECRET,
                )
  c.use_old_device_list = True
  c.new_sign_algorithm = True
  if c.error is not None:
    raise Exception(c.error['Payload'])
  token = c.token
  if token == None:
    raise Exception('Informations de connexion incorrecte !')

  # Affichage de la liste
  devices = c.getdevices()
  while len(devices) == 0:
    print('Pas de périphérique trouvé, on essaie encore !')
    time.sleep(10)
    devices = c.getdevices()

  print("Liste des périphériques : \n", json.dumps(devices, indent=2))
  for d in devices:
    result = c._tuyaplatform('cloud/thing/'+d["id"]+'/model',ver='v2.0')
    model = json.loads(result['result']['model'])
    print("\nModèle de données: " + d["id"] + "\n", json.dumps(model, indent=2))

except Exception as err:
  print('inventaro: ' + str(err) + ' line ' + format(sys.exc_info()[-1].tb_lineno))

