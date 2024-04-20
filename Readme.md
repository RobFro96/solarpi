# SolarPi

## Programm aktualisieren
```
cd ~/solarpi
git reset --hard HEAD
git clean -f -d
git pull
sudo pip install -r requirements.txt
sudo systemctl restart solarpi_sammler.service
sudo systemctl restart solarpi_server.service
```

## Kalkulation des Speicherbedarfs
- circa 2 KB für alle drei Geräte pro Anfrage
- Anfrage alle 1 min = 1440 Anfragen / Tag
- ≈ 3 MB pro Datei
- Verfügbarer Speicherplatz abfragen mit `df -h`
```
Filesystem      Size  Used Avail Use% Mounted on
/dev/root       7.1G  1.5G  5.3G  22% /
```
- hier 5.3 GB frei (available)
- 1700 Tage = 4.8 Jahre


## Erstinstallation

### OS Image auf SD brennen
- Raspberry Pi Imager:  <https://www.raspberrypi.com/software/>
- Betriebssystem: Raspberry Pi OS (other) → Raspberry Pi OS Lite (32bit)
- SD-Karte auswählen
- Zusätzliche Optionen:
  - Hostname: solarpi.local
  - SSH aktivieren, Passwortauthentifizierung
  - Set username and password: pi, XXXXX
- SD-Karte brennen

### Über SSH verbinden
- `ping solarpi.local`
- Verbindung herstellen über Putty oder `ssh pi@solarpi.local`
- `sudo apt update`
- `sudo apt -y upgrade`
- `sudo raspi-config`
  - 5 Localisation Options
    - L1 Locale → de_DE (Leertaste drücken zum Auswählen)
    - L2 Timezone → Berlin
  - 6 Advanced → A1 Expand Filesystem
- Finish → Reboot

### WLAN konfigurieren
- `ip a` → wlan0 hat keine IP-Adresse
- `sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`
```
network={
   ssid="WLAN-SSID"
   psk="WLAN-PASSWORT"
}
```
- `sudo reboot`
- `ip a` → wlan0 hat eine IP-Adresse

### Git einrichten
- Mit Git kann die aktuellste Programmversion mit nur einem Befehl von GitHub heruntergeladen werden
- `sudo apt install git`
- `git clone git@github.com:RobFro96/solarpi.git`
- `cd solarpi`

### Python vollständig installieren
- `python --version` →  sollte >3.8 liefern
- `sudo apt install python3-pip python3-numpy python3-matplotlib`
- `sudo pip install --upgrade pip`
- `sudo pip install -r requirements.txt`
- `python solarpi.py` sollte das Programm starten
- Beenden mit Strg+C

### Service installieren
```
sudo cp solarpi_sammler.service /etc/systemd/system/
sudo cp solarpi_server.service /etc/systemd/system/

sudo systemctl enable solarpi_sammler.service
sudo systemctl enable solarpi_server.service

sudo systemctl start solarpi_sammler.service
sudo systemctl start solarpi_server.service
```

- Anzeige von Status und Logs:
```
sudo systemctl status solarpi_sammler.service
journalctl -u solarpi_sammler.service -n 20
```