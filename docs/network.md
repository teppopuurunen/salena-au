cat > docs/network.md <<'EOF'
# Verkko ja väylät

Tämä dokumentti kuvaa Salena AU -järjestelmän tiedonsiirron periaatteet ja rajaukset.

---

## Periaate

- Ethernet on ensisijainen väylä automaatiolle (ESP ↔ RPi)
- Wi-Fi on käyttöliittymille (tabletti/puhelin), ei kriittiselle ohjaukselle
- USB:llä hoidetaan erikoisliitännät (esim. RS422)

---

## Yhteydet

### Ethernet
- ESP32-S3 relemoduulit ja mahdolliset muut ohjaimet
- Tavoite: deterministinen ja helposti debugattava liikenne

### Wi-Fi
- Käyttöliittymät (esim. selain/HA-näkymä)
- Ei oleteta toimivaksi ohjauspoluksi

### USB
- Autopilotti (USB–RS422-adapteri)

---

## Home Assistant
- HA on ei-kriittinen käyttöliittymäkerros
- HA:n vika ei saa estää paikallista ohjausta tai perustoimintoja

---

## Rajaukset tässä vaiheessa
- Ei pilvipalveluriippuvuuksia
- Ei Wi-Fi-riippuvaista kuormaohjausta
- Autopilotti-integraatio ensin read-only

---

## NMEA 0183 – Autopilotin käyttö (Autohelm ST5000)

Autohelm ST5000 -autopilotti käyttää NMEA 0183 -navigointidataa Track Control
-toiminnossa. Viestintä on yksisuuntainen: data kulkee plotterilta /
Raspberry Pi:ltä autopilotille.

ST5000 ei lähetä NMEA 0183 -dataa takaisin.

---

### Tuetut ja käytettävät NMEA-lauseet

#### Minimisetti (riittää Track Controliin)

- **APB**  
  Autopilot sentence. Sisältää poikkeamatiedon (XTE), ohjaussuunnan sekä
  waypointin suuntatiedon.  
  Riittää yksinään reittipisteohjaukseen.

---

#### Suositeltu käyttökelpoinen setti

- **APB** – varsinainen reittiohjaus  
- **RMB** – waypointin suunta ja etäisyys  
- **RMC** – COG/SOG ja aika (tukitieto)

Tämä yhdistelmä vastaa tyypillistä käytäntöä vanhojen plottereiden ja
autopilottien yhteiskäytössä.

---

#### Valinnaiset lisälauseet

- **XTE** – Cross Track Error erillisenä  
- **BWC / BWR** – bearing ja distance to waypoint  
- **VTG** – course & speed over ground  

---

### Kompassiin liittyvä huomio

ST5000:n sisäinen kompassi on rakenteeltaan yksinkertainen eikä erityisen
tarkka.

Tarvittaessa autopilotille voidaan syöttää ulkoinen suuntatieto:
- **HDG** – magneettinen suunta  
- **HDT** – tosi suunta  

Ulkoinen suuntatieto ei ole edellytys Track Control -toiminnalle, mutta se voi
parantaa ohjauskäyttäytymistä, mikäli käytössä on luotettava ulkoinen
kompassi- tai IMU-lähde.

---

### Rajaukset

- Autopilotin tilaa tai telemetriaa ei saada luettua takaisin
  NMEA 0183 -muodossa.
- Useiden päällekkäisten reittilauseiden samanaikaista lähettämistä ei
  suositella.
- Paikkalauseet (esim. GGA, GLL) eivät ole tarpeellisia Track Control -käytössä.
EOF
