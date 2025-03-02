# requêtes possibles
## demander le modèle des données :
* script python :
```
import tinytuya
import json
deviceId='********' # mettre l'id obtenu avec tinytuya
deviceIp='192.168.0.15' # mettre l'IP
deviceKey='********' # mettre la clé obtenue avec tinytuya
d = tinytuya.Device( dev_id=deviceId, address=deviceIp, local_key=deviceKey,version=3.3)
result = c._tuyaplatform('cloud/thing/'+d["id"]+'/model',ver='v2.0')
model = json.loads(result['result']['model'])
print("\nModel of device: " + d["id"] + "\n", json.dumps(model, indent=2))
```

# infos de statut
* 1 = switch (False ou True)
* 2 = temp_set (thermostat, en dixièmes de °C, 160 à 880 par pas de 5)
* 3 = temp_current (températures mesurée, en °C, -20 à 100 par pas de 1)
* 4 = mode ( "cold", "hot", "wet", "wind", "auto")
* 5 = ventilateur (auto,mute,low,…)
* 18 = humidity_current (toujours à 0 --> pas disponible)
* 20 = code erreur (0)
* 101 = capteur de poussières (0)
* 105 = sleep (off)
* 110 = fonctions disponibles (131644)
    2,3,4,5,9,17
* 113 = balayage vertical (1)
* 114 = balayage horizontal (1)
* 119 = mode éco (0,1,2,3)
* 120 (off)
* 123 (0008)
* 125 = qualité de l'air (great)
* 126 (0)
* 127 (0)
* 128 (0)
* 129 (1)
* 130 (26)
* 131 = filtre sale (False)
* 132 (False)
* 133 (3)
* 134 ({"t":1720816115,"s":false,"clr":true})

# liste complète des 30 dsp
| Id  |    | code             | Type   | description |
+-----+----+------------------+--------+-------------+
|   1 | rw | Power            | bool   | on/off (True=on, False=off)
|   2 | rw | temp\_set        | value  | température cible de 16 à 88 °C (en 1/10 de degré),scale=1,step=5
|   3 | ro | temp\_current    | value  | température mesurée de -20 à 100 °C
|   4 | rw | mode             | enum   | "cold","hot","wet","wind","auto"
|   5 | rw | windspeed        | enum   | "strong","high","mid\_high","mid","mid\_low","low","mute","auto"
|  18 | rw | humidity_current | value  | humidité 0-100 %
|  20 | ro | Fault            | bitmap | code d'erreur (E0,E1,…) sur 30 bits
| 101 | ro | pm25             | value  | capteur de poussière
| 105 | rw | sleep            | enum   | "off","normal","old","child"
| 110 | ro | markbit          | bitmap | fonctionnalités disponibles, sur 24 bits
| | | | |  0. Si la température est réglable en mode déshumidification
| | | | |  1. Si la température est réglable en mode ventilation
| | | | | +2. Si la température est réglable en mode automatique
| | | | | +3. Alimentation en air (Ventilation ?)
| | | | | +4. Alimentation en air vectoriel (Balayage vertical ?)
| | | | | +5. Air de balayage gauche et droit (Balayage horizontal)
| | | | |  6. Photosensible
| | | | |  7. Déshumidification intelligente et prévention de la moisissure
| | | | |  8. Capteur d'humidité
| | | | | +9. Nettoyage de l'évaporateur
| | | | |  10. Économisez de l'argent et voyez-le
| | | | |  11. Statistiques de puissance
| | | | |  12. Mode générateur
| | | | |  13. Élevé > vent chaud/vent frais
| | | | |  14. Fonction de détection de la qualité de l'air
| | | | |  15. Mis à vide (anciennement : fonction humidité)
| | | | |  16. Réglé sur vide (original : Le fonctionnement de l'équipement permet d'économiser de l'argent, visible, affichage de la courbe de température)
| | | | | +17. Chauffage à 8 ℃
| | | | |  18. Fonction filtre sale et bouché
| | | | |  20. Présence ou absence de PM2,5
| | | | |  21. , 1 correspond à Fahrenheit, 0 pour Celsius
| | | | |  22. vent doux
| | | | |  23. alimentation en air grand angle gauche et droite
| 113 | rw | up\_down\_sweep  | enum   | balayage vertical : 0-3 (Aucun, haut-bas, haut, bas)
| 114 | rw |left\_right\_sweep| enum   | balayage horizontal : 0-7 (Aucun, gauche-droite, gauche, central, droite, gauche, droit, grand-angle)
| 115 | ro | totalN           | value  | Entier d’électricité : 0-1000000
| 116 | ro | totalP           | value  | Puissance décimale : 0-1000000
| 119 | rw | money            | enum   | Économie d'énergie : 0-3
| 120 | rw | energy           | enum   | Mode moteur : "off","L1","L2","L3"
| 122 | ro | fault2           | enum   | code erreur (suite) : "P6","P7",…
| 123 | rw | boolCode         | string | booléen, 2 octets
| | | | |  bit0 : éco
| | | | |  bit1 : Déshumidification intelligente et prévention de la moisissure
| | | | |  bit2 : Nettoyage de l'évaporateur
| | | | |  bit3 : lumière
| | | | |  bit4 : bip (si 1 : l'appareil bip à chaque commande)
| | | | |  bit5 : en bonne santé
|125 | ro | airquality        | enum   | qualité de l'air ;["great,"good","middle","bad","verybad","veryverybad"]
|126 | rw | up_down_freeze    | enum   | balayage haut/bas ; 0-5 (Aucun, haut-bas, haut, bas
|127 | rw | left_right_freeze | enum   | balayage gauche/droite ; 0-7 (Aucun, gauche-droite, gauche, central, droite, gauche, droit, grand-angle)
|128 | ro | style             | enum   |  ; 0-1
|129 | rw | kwh               | enum   | puissance ; 1-5
|130 | rw | savemoney_temp    | value  | Température d'économie ; 26-31 °C step=1
|131 | ro | dirty_filter      | bool   | Le filtre est sale et bouché ; 
|132 | rw | hot_cold_wind     | bool   | Température élevée/vent frais ; hot_cold_wind
|133 | rw | wind              | enum   | Balançoire horizontale/balançoire verticale ; wind
|134 | ro | work_time         | string | Durée de fonctionnement ; work_time
|135 | ro | run_time          | value  | heures d'ouverture ; run_time
|136 | rw | temp_set_f        | value  | title="Temp Set F"> ; temp_set_f


