from yoctopuce.yocto_api import YAPI, YRefParam
from yoctopuce.yocto_power import YPower

errmsg = YRefParam()
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    print("Échec de connexion au hub Yoctopuce :", errmsg.value)
    exit()
else:
    print("Connexion réussie au hub Yoctopuce")

sensor = YPower.FirstPower()
if sensor is None:
    print("Aucun capteur détecté")
    YAPI.FreeAPI()
    exit()

print("Capteur détecté :", sensor.get_friendlyName())

# Lecture de la puissance toutes les 2 secondes pendant 10 secondes
for i in range(5):
    valeur = sensor.get_currentValue() 
    print(f"Consommation actuelle : {valeur} W")
    YAPI.Sleep(1000)

YAPI.FreeAPI()