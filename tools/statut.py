
import sys
import tinytuya
import json

#deviceId='********' # mettre l'id obtenu avec tinytuya
#deviceIp='192.168.0.15' # mettre l'IP
#deviceKey='********' # mettre la clé obtenue avec tinytuya
deviceId=sys.argv[1]
deviceIp=sys.argv[2]
deviceKey=sys.argv[3]
d = tinytuya.Device( dev_id=deviceId, address=deviceIp, local_key=deviceKey,version=3.3)
data = d.status()
print("Données de statut : \n", json.dumps(data, indent=2))
