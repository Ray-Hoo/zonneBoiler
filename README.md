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

Nu kun je de temperatuur uitlezen op de volgende locatie:
```
cd /sys/bus/w1/devices
```
Ga dan naar het adres van jouw sensor bijvoorbeeld:
```
cd 28-0517c026dbff
```
Voer hier:
```
cat w1_slave
```
uit om de ruwe waarde te zien:
```
f4 01 4b 46 7f ff 0c 10 c7 : crc=c7 YES
f4 01 4b 46 7f ff 0c 10 c7 t=31250
```
