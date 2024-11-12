
import sys
import tinytuya
import json

#deviceId='********' # mettre l'id obtenu avec tinytuya
#deviceIp='192.168.0.15' # mettre l'IP
#deviceKey='********' # mettre la clé obtenue avec tinytuya
deviceId=sys.argv[1]
deviceIp=sys.argv[2]
deviceKey=sys.argv[3]
clef=sys.argv[4]
valeur=sys.argv[5]
d = tinytuya.Device( dev_id=deviceId, address=deviceIp, local_key=deviceKey,version=3.3)

d.set_value(clef,valeur)

