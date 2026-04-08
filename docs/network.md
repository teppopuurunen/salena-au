# Verkko ja väylät

Tämä dokumentti kuvaa Salena AU -järjestelmän tiedonsiirron periaatteet ja rajaukset.

---

## Periaate

- **Ethernet** on ensisijainen väylä automaatiolle ja mittaukselle (ESP32 ↔ RPi)
- **RS485 Modbus RTU** hoitaa tilatiedot ja releohjauksen kenttä-I/O-moduuleille
- **I2C (eristetty)** varaa tarkan virranmittauslinjan (ISO1540-erotuksella)
- **Wi-Fi** on käyttöliittymille (tabletti/puhelin), ei kriittiselle ohjaukselle
- **USB** hoidetaan erikoisliitännät (esim. RS422 autopilotille)

---

## Yhteydet

### Ethernet
- **ESP32-S3 rele-ESP:t** ↔ Raspberry Pi (ohjaus- ja tilaväylä)
- **Mittaus-ESP** → Raspberry Pi (PoE, virran ja tankkidatan toimitus)
- Tavoite: deterministinen ja helposti debugattava liikenne
- Reititin: Huawei B818-263 4G LTE
- Kytkin: Teltonika TSW101 (hankkimatta)

### RS485 Modbus RTU
- **Rele-ESP 1 (master)** ↔ Modbus I/O -moduulit (SKU:26244)
- Tilatiedot: 24 optoeristettyä tuloa (DI) kohokytkimille, 1-0-Auto-asennoille ja releiden todellisille tiloille
- Releohjaus: 24 transistorilähtöä (DO, Darlington sinking 500mA) ulkoisille HV- ja DIN-releille
- Keskisuuret kuormat (10A–20A): ulkoiset autorele/DIN-kiskokannalliset releet SKU:26244-lähtöjen perään
- Häiriönkestävyys: RS485-väylä sopii sähkökeskukseen ja veneen häiriöympäristöön

### I2C (eristetty)
- **Mittaus-ESP** ↔ Mittausmoduulit (INA228 + INA3221)
- Galvaaninen erotus: ISO1540-erottimet (MIKROE-1878)
- Pääakku: INA228 (MIKROE-4810, 20-bit, shuntti 5705-HoFL2-250A)
- Pienkuormat: INA3221 (MIKROE-4126, 3-kanavainen, 3× shuntti HoFL2-20A)
- Eristys estää hupiakun miinuksen kytkeytymisen mittausväylän kautta Brain-elektroniikan maahan

### Wi-Fi
- Käyttöliittymät (esim. selain/HA-näkymä)
- Ei oleteta toimivaksi ohjauspoluksi
- Häiriöt eivät vaikuta paikalliseen ohjaukseen

### USB
- Autopilotti (USB–RS422-adapteri Raymarine ST5000:lle)

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
