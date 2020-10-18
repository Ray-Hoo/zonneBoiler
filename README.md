# zonneBoiler
Meet de temperatuur van je zonneBoiler en zet dit in een MariaDB/mySQL database.

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
Nu de waarden gelezen kunnen worden, willen we dit natuurlijk iedere 5 minuten doen en deze opslaan in een database en deze tonen op een web-pagina, zodat we er vanaf een Toon thermostaat bij kunnen. Hiervoor gaan we nu eerst diverse packages installeren op de Raspberry Pi:
```
sudo apt-get install apache2 php libapache2-mod-php
sudo apt-get install mariadb-server mariadb-client php-mysql
sudo apt-get install python-mysqldb
```
Nu moet eerst in mysql een database gemaakt worden en een user zodat we deze kunnen gaan vullen:
```
sudo mysql -u root
CREATE DATABASE temperatuur_database;
USE temperatuur_database;
CREATE TABLE temperatuurLog(date DATE NOT NULL, time TIME NOT NULL, temperature FLOAT(5,2) NOT NULL);
CREATE USER 'gebruiker'@'localhost' IDENTIFIED BY 'wachtwoord';
GRANT ALL PRIVILEGES ON temperatuur_database . * TO 'gebruiker'@'localhost';
```
Nu de database er is moet deze natuurlijk gevuld gaan worden. Dit kan met het script:
```
read-temperature.py
```
Hierin moeten de volgende wijzigingen gemaakt worden:
```
- Wijzig bij temperature_sensor deze waarde: 28-0517c026dbff , naar de waarde van jouw sensor
- Wijzig bij # MySQL/MariaDB variables de volgende waardes:
  - localhost (als de MariaDB niet lokaal staat)
  - gebruiker
  - wachtwoord
  - temperatuur_database (als je een andere naam gekozen hebt voor de database)
```
Voer het script handmatig uit om te kijken of het werkt:
```
./read-temperature.py
```
Als deze succesvol is dan kun je dit automatisch elke x minuten laten lopen. Pas hiervoor de crontab aan met crontab -e en voeg hierin de volgende regel toe (voor elke 5 minuten). Zorg wel dat het pad klopt naar read-temperature.py.
```
*/5 * * * * /pad/naar/read-temperature.py
```
Om de data zichtbaar en bruikbaar te maken zetten we het bestand get-temperature.php in de directory /var/www/html Pas hierin de volgende variabele aan naar de door jou gebruikte waarden:
```
$serverip="ip-adres";
$portnumber="port-number";
$username="username";
$password="password";
$database="temperatuur_database";

```
Door nu naar het ip-adres van je raspberry te gaan kun je de waarde zien:
```
http://ip-adres-raspberry-pi/get-temperature.php
```
Dit geeft dan bijvoorbeeld het volgende resultaat:
```
raw data:
{"Date":"24\/05\/2020","Time":"15:40","Temperature":"28.94"}

Of als JSON opgemaakt door de browser:
Date	"24/05/2020"
Time	"15:40"
Temperature	"28.94"
```
Deze data kan nu gebruikt worden voor andere doeleinden zoals bijvoorbeeld de zonneboilerStat app voor op de Toon. Zie: https://github.com/Ray-Hoo/zonneboilerStats
