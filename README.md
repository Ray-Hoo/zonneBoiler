# zonneBoiler
Meet de temperatuur van je zonneBoiler en toon dit op de Toon thermostaat.

Benodigdheden:

- Raspberry Pi
- DS18B20 sensor (aan kabel)
- Zonneboiler

Stel op de Raspberry Pi het gebruik van het 1-wire protocol in.

```
sudo modprobe w1-gpio
sudo modprobe w1-therm
```

Om te zorgen dat deze modules automatisch geladen worden tijdens het booten, moet je het volgende doen:
```
sudo raspi-config
```
Menu optie *"5 Interfacing Options"* en dan optie *"P7 1-wire"*. Kies hier *"Ja"* (Yes) om aan te zetten.

Het 1-wire protocol staat nu standaard aan voor pin 4, wil je echter een andere pin gebruiken dan moet je deze aanzetten voor de gewenste pin. Met het volgende commando zet je het aan voor GPIO pin 25:
```
sudo dtoverlay w1-gpio gpiopin=25 pullup=0
```
Om nu te zorgen dat je niet iedere keer na het herstarten van de Raspberry Pi opnieuw dit commando moet ingeven, kun je dit opnemen in: 
```
sudo nano /etc/rc.local
```
Voeg hieraan net voor *"exit 0"* het volgende toe:
```
# start one wire protocol on gpiopin 25
sudo dtoverlay w1-gpio gpiopin=25 pullup=0
```
