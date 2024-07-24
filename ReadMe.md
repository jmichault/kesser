

plugin domoticz pour les climatiseurs de marque Kesser munis d'un module WiFi.

# Préparation
 * Vous devez enregistrer le climatiseur dans l'application «tuya Smart» sur votre téléphone portable
 * Vous devez fixer l'adresse IP du climatiseur dans votre serveur DHCP (en général votre box internet)
 * Vous devez créer un compte développeur sur tuya.com, et créer un projet dans lequel vous enregistrez le climatiseur
    voir : https://github.com/jasonacox/tinytuya/files/12836816/Tuya.IoT.API.Setup.v2.pdf

# installation
Note : on va aussi installer :
 * tinytuya
 * la version 43.0.0 de cryptography car certaines versions sont incompatibles avec domoticz.
```
cd domoticz/plugins
sudo pip3 install cryptography==43.0.0 --break-system-packages
sudo pip3 install tinytuya --break-system-packages
git clone https://github.com/jmichault/kesser
sudo systemctl restart domoticz
python3 kesser/tools/inventaro.py
```
 Rentrez le code région, l'ID et le secret obtenus sur tuya.com. Le script va alors afficher les périphériques de vos projets.
 Notez le champ id et le champ key de votre climatiseur.

 Il ne vous reste plus qu'à créer un matériel de type «Kesser (WiFi)» dans domoticz.

