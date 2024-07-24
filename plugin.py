# Domoticz Kesser Plugin
#
# Author: jmichault
#
"""
<plugin key="kesser" name="Kesser (WiFi)" author="jmichault" version="0.0.1" wikilink="" externallink="https://github.com/jmichault/Kesser.git">
    <description>
        <br/>
        <h2>Kesser Plugin version 0.0.1</h2><br/>
    </description>
    <params>
        <param field="Address" label="IP Address" width="200px" required="true" default="192.168.1.15"/>
        <param field="Mode2" label="DeviceId" width="300px" required="true" default="" />
        <param field="Mode3" label="DeviceKey" width="300px" required="true" default="" password="true" />
    </params>
</plugin>
"""
try:
  import Domoticz
except ImportError:
  import fakeDomoticz as Domoticz
import tinytuya

class BasePlugin:
  enabled = False
  def __init__(self):
    return

  def onStart(self):
    Domoticz.Log('plugin Kesser ' + Parameters['Version'] + ' demarre.')
    Domoticz.Log('TinytuyaVersion:' + tinytuya.version )
    Domoticz.Debugging(0)
    Domoticz.Heartbeat(10)
    deviceIp = Parameters['Address']
    deviceId = Parameters['Mode2']
    deviceKey = Parameters['Mode3']
    # créer les device si nécessaire
    if ( len(Devices) == 0 ) :
      Domoticz.Device(Name="Kesser (Marche/Arret)", DeviceID=deviceId, Unit=1, TypeName="Switch",  Image=9, Used=1).Create()
      options={'ValueStep':0.5 , 'ValueMin':16 , 'ValueMax':88 , 'ValueUnit':'°C'}
      Domoticz.Device(Name='Kesser' + ' (Thermostat)', DeviceID=deviceId, Unit=2, Type=242, Subtype=1, Options=options, Used=1,Image=23).Create()
      Domoticz.Device(Name='Kesser' + ' (Temperature)', DeviceID=deviceId, Unit=3, Type=80, Subtype=5, Used=1).Create()
      options={'LevelOffHidden':'true' , 'LevelActions':'', 'SelectorStyle':'1'}
      mode= [ "0","cold","hot","wet","wind","auto"]
      options['LevelNames'] = '|'.join(mode)
      Domoticz.Device(Name='Kesser' + ' (Mode)', DeviceID=deviceId, Unit=4, Type=244, Subtype=62, Switchtype=18, Options=options, Image=23, Used=1).Create()
      options={'LevelOffHidden':'true' , 'LevelActions':'' , 'SelectorStyle':'1'}
      mode= [ "0", "auto" , "silencieux","très lent","lent","moyen","fort","très fort","max." ]
      options['LevelNames'] = '|'.join(mode)
      Domoticz.Device(Name='Kesser' + ' (Ventilateur)', DeviceID=deviceId, Unit=5, Type=244, Subtype=62, Switchtype=18, Options=options, Image=7, Used=1).Create()

  def onCommand(self, Unit, Command, Level, Color):
    Domoticz.Debug("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level) + "', Color: " + str(Color))
    deviceIp = Parameters['Address']
    deviceId = Parameters['Mode2']
    deviceKey = Parameters['Mode3']
    match Unit :
     case 1: # marche/arret
      if Command=='On':
        d = tinytuya.Device( dev_id=deviceId, address=deviceIp, local_key=deviceKey,version=3.3)
        d.set_value(1,True)
      elif Command=='Off':
        d = tinytuya.Device( dev_id=deviceId, address=deviceIp, local_key=deviceKey,version=3.3)
        d.set_value(1,False)
     case 2: # thermostat
        d = tinytuya.Device( dev_id=deviceId, address=deviceIp, local_key=deviceKey,version=3.3)
        Domoticz.Log("nouvelle température="+str(int(Level*10)))
        d.set_value(2,int(Level*10))
     # case 3: # temperature courante : pas de commande
     case 4: # mode
        mode = {10:"cold",20:"hot",30:"wet",40:"wind",50:"auto" }.get(Level,0)
        d = tinytuya.Device( dev_id=deviceId, address=deviceIp, local_key=deviceKey,version=3.3)
        d.set_value(4,mode)
     case 5: # vitesse du ventilateur
        windspeed = {10:"auto" , 20:"mute",30:"low",40:"mid_low",50:"mid",60:"mid_high",70:"high",80:"strong" }.get(Level,0)
        d = tinytuya.Device( dev_id=deviceId, address=deviceIp, local_key=deviceKey,version=3.3)
        d.set_value(5,windspeed)
    self.onHeartbeat()


  def onHeartbeat(self):
    Domoticz.Debug('onHeartbeat called')
    # mettre a jour les statuts
    deviceIp = Parameters['Address']
    deviceId = Parameters['Mode2']
    deviceKey = Parameters['Mode3']
    d = tinytuya.Device( dev_id=deviceId, address=deviceIp, local_key=deviceKey,version=3.3)
    data = d.status()
    Domoticz.Debug("onHeartbeat data=" + str(data) )
    if data['dps']['1'] == True :
      Power='On'
      nPower=1
    else:
      Power='Off'
      nPower=0
    if Devices[1].sValue != str(Power) :
      Devices[1].Update(nValue=nPower,sValue = str(Power))
    temp_set = data['dps']['2'] 
    if Devices[2].sValue != str(temp_set/10) :
      Devices[2].Update(nValue=int(temp_set/10),sValue=str(temp_set/10))
    current_temp= data['dps']['3']
    if str(Devices[3].sValue) != str(current_temp) :
      Devices[3].Update(nValue=int(current_temp),sValue = str(current_temp))
    mode = { "cold":10 , "hot":20,"wet":30, "wind":40,"auto":50 }.get(data['dps']['4'],0)
    if Devices[4].nValue != mode :
      Devices[4].Update(nValue=int(mode),sValue=str(mode))
    windspeed = { "auto":10 , "mute":20,"low":30, "mid_low":40,"mid":50,"mid_high":60,"high":70,"strong":80 }.get(data['dps']['5'],0)
    if Devices[5].nValue != windspeed :
      Devices[5].Update(nValue=int(windspeed),sValue=str(windspeed))

global _plugin
_plugin = BasePlugin()
        
    
def onStart():
    global _plugin
    _plugin.onStart()

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

