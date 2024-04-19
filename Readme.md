# SolarPi

## Programm aktualisieren
```
cd ~/solarpi
git pull
sudo pip install -r requirements.txt
sudo systemctl restart solarpi.service
```

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
- `sudo apt install python3-pip`
- `sudo pip install --upgrade pip`
- `sudo pip install -r requirements.txt`
- `python solarpi.py` sollte das Programm starten
- Beenden mit Strg+C

### Service installieren
```
sudo cp solarpi.service /etc/systemd/system/
sudo systemctl enable solarpi.service
sudo systemctl start solarpi.service
sudo systemctl status solarpi.service
journalctl -u solarpi.service -n 20
```