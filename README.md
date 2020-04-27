# zonneBoiler
Meet de temperatuur van je zonneBoiler en toon dit op de Toon thermostaat.

Benodigdheden:

- Raspberry Pi
- DS18B20 sensor (aan kabel)
- Zonneboiler
- Toon thermostaat (rooted)

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
Nu de waarden gelezen kunnen worden, willen we dit natuurlijk iedere 5 minuten doen en deze opslaan in een database en deze tonen op een web-pagina. Hiervoor gaan we nu eerst diverse packages installeren:
```
sudo apt-get install apache2 php libapache2-mod-php
sudo apt-get install mysql-server mysql-client php-mysql
sudo apt-get install python-mysqldb
```
Nu moet eerst in mysql een database gemaakt worden en een user om deze te vullen:
```
sudo mysql -u root
CREATE DATABASE temperatuur_database;
USE temperatuur_database;
CREATE TABLE temperatuurLog(datetime DATETIME NOT NULL, temperatuur FLOAT(5,2) NOT NULL);
CREATE USER 'gebruiker'@'localhost' IDENTIFIED BY 'wachtwoord';
GRANT ALL PRIVILEGES ON temperatuur_database . * TO 'gebruiker'@'localhost';
```

