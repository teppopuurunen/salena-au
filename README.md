# Salena AU - Järjestelmämäärittely v5.0.0
**Projekti:** Integroitu veneautomaatio- ja navigointijärjestelmä  
**Alusta:** Amigo 40 (S/Y Salena, 1977)  
**Tila:** Integraatiovaihe  

## 1. Yleiskuvaus
Salena AU v5.0 on hybridimallinen ohjausjärjestelmä, joka yhdistää perinteisen analogisen sähköjärjestelmän hajautettuun tietotekniseen hallintaan. Arkkitehtuuri noudattaa "Mechanical Fallback" -periaatetta, jossa kriittinen I/O-ohjaus (1-0-Auto) on varmistettu mekaanisilla ohituskytkennöillä automaatiokerroksesta riippumatta.

## 2. Laitteistoarkkitehtuuri
### 2.1 Keskusyksikkö (Master Node)
- **Isäntä:** Raspberry Pi 5 (8GB RAM)
- **Tallennus:** NVMe SSD (PCIe Gen 2.0 -väylä Waveshare HAT+ kautta)
- **Käyttöjärjestelmä:** OpenPlotter (Debian-pohjainen)
- **Virransyöttö:** Waveshare UPS HAT (E), 12VDC vakioitu syöttö

### 2.2 Hajautetut I/O-solmut (Peripheral Nodes)
- **Moduulit:** 2x Waveshare WS-31130 (ESP32-S3)
- **Tiedonsiirto:** 10/100 Mbps kiinteä Ethernet (IEEE 802.3)
- **Kapasiteetti:** 16x SPDT-relelähtöä, 16x optoerotettua digitaalituloa
- **Protokolla:** MQTT yli TCP/IP

### 2.3 Virranhallinta ja navigointi-integraatio
- **Aurinkoenergia:** Victron SmartSolar MPPT (VE.Direct - USB-Serial)
- **Akku- ja tankkitulot:** Kustomoitu ESP32-S3 (Home ESP) USB-väylän kautta
- **Autopilotti:** Raymarine ST5000 (NMEA 0183 / RS422 -> USB -muunnos)

## 3. Ohjelmistopino
- **Dataväylä:** Signal K Server (Yleinen meridatan vaihtoalusta)
- **Automaatiomoottori:** Home Assistant (Docker-kontti)
- **Navigointi:** OpenCPN (Kartanluku ja reitinsuunnittelu)
- **Viestinvälitys:** Mosquitto MQTT (Solmujen välinen telemetria)

## 4. Vikatila- ja turvallisuuslogiikka
Järjestelmä on jaettu kolmeen toimintatasoon:
1. **Taso 1 (Analoginen):** Fyysiset 1-0-Auto-kytkimet valaistukselle ja pumpuille.
2. **Taso 2 (Solmu):** ESP32-S3-laiteohjelmisto käsittelee paikallisen I/O-logiikan ilman keskusyksikköä.
3. **Taso 3 (Logiikka):** Home Assistant hoitaa monimutkaiset automaatiot ja etähallinnan.

## 5. Arkiston rakenne
- `/core-rpi5`: Docker-asetukset, HA-konfiguraatiot ja Signal K -asetukset.
- `/nodes`: WS-31130- ja Home-ESP-moduulien laiteohjelmistot.
- `/hardware`: Kytkentäkaaviot, sulakekartat ja [SPECIFICATION.md](hardware/SPECIFICATION.md).
- `/docs`: Vanha dokumentaatio (v4.2) ja hankintaloki.

## 6. Lisenssi
Tämä projekti on lisensoitu MIT-lisenssillä.
