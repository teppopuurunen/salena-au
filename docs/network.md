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
- **Mittaus-ESP / Akku-ESP / Valo-ESP** → Raspberry Pi (PoE)
- **Topologia:** Huawei B818-263 reititin (master) → 2x Teltonika TSW101 kytkin (PoE)
  - Teltonika 1: Pääkytkin (uplink Huaweihin, PoE-portit 1-4 ESPille)
  - Teltonika 2: Varalla (daisy-chain Teltonika 1:een tai suoraan Huaweihin)
- Tavoite: deterministinen ja helposti debugattava liikenne
- Reititin: Huawei B818-263 4G LTE
- Kytkin: Teltonika TSW101 (hankittu)

**PoE-topologia (5 × ESP32-S3-POE-ETH)**
- Rele-ESP 1 ja 2: Teltonika TSW101 PoE-portteihin (etusijalla 1-4)
- Mittaus-ESP, Akku-ESP, Valo-ESP: Teltonika TSW101 PoE-portteihin
- Kunkin ESP32 saa syöttönsä PoE-kaapelista (RJ45), mikä takaa nollalatenssin ja häiriöttömyyden

**Failover-periaate (Modbus RTU)**
- Rele-ESP 1: Aktiivinen Modbus RTU Master (RS-portti valmiina, rele-ESP 2:n ohjaus)
- Rele-ESP 2: Varalla-Master (ottaa roolin välittömästi, jos Rele-ESP 1 tai sen RS485-portti kaatuu)
- Vikatilanteessa: Rele-ESP 2 muuntautuu Master-tilaan ja jatkaa Modbus-väylän hallintaa katkeamattomasti

### RS485 Modbus RTU
- **Rele-ESP 1 (master)** ↔ Modbus I/O -moduulit (SKU:26244)
- Tilatiedot: 24 optoeristettyä tuloa (DI) kohokytkimille, 1-0-Auto-asennoille ja releiden todellisille tiloille
- Releohjaus: 24 transistorilähtöä (DO, Darlington sinking 500mA) ulkoisille HV- ja DIN-releille
- Keskisuuret kuormat (10A–20A): ulkoiset autorele/DIN-kiskokannalliset releet SKU:26244-lähtöjen perään
- Häiriönkestävyys: RS485-väylä sopii sähkökeskukseen ja veneen häiriöympäristöön

### I2C (eristetty)
- **Akku-ESP** ↔ Mittausmoduulit (INA228 + INA3221)
- Galvaaninen erotus: 1 × ISO1540-erotin (MIKROE-1878)
- INA228-kanavat (high-side):
  - Hupiakku `0.00025` ohm (300A/75mV)
  - Startti/VSR `0.00075` ohm (100A/75mV)
  - UPS `0.00075` ohm (100A/75mV)
- INA3221-kanavat (2 korttia, 6 kanavaa, The Shunt Hack):
  - Bilssi 1-2 `0.0015` ohm (50A/75mV)
  - Laajennus 1-4 `0.00375` ohm (20A/75mV)
- Toisen INA3221-kortin osoite muutetaan juotospadilla (0x42 + 0x43)
- Kaikkien mittauspiirien GND ankkuroituu yhteiseen maapulttiin

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

## Moottorin reaaliaikaiset turvalukitukset
- Volvo öljynpaine- ja jäähdytysvesihälytykset luetaan optoerotettuna keskeytyksillä.
- D+ optokanava toimii käyntitietona ja hard interlockina starttireleelle.
- Optokanavien etuvastukset:
  - 12V tilatiedot (öljy, lämpö, pilssikellukkeet, D+): 1k ohm / 2W
  - PoE 48V valvonta: 4.7k ohm / 2W

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

### Moottorin reaaliaikaiset turvalukitukset (optokanavat)

Volvo Penta 2003 -moottorin kriittiset signaalit luetaan optoerottetuina GPIO-keskeytyksillä:

| Kanava | Signaali | Etuvastus | Logiikka | Laitteisto |
|---|---|---|---|---|
| Opto 1 | Volvo öljynpainehälytys | 1kΩ / 2W | Anturin maadoitus aktivoi summerin + ESP32 keskeytyksen | Volvo alkuperäinen anturi |
| Opto 2 | Volvo jäähdytysvesihälytys | 1kΩ / 2W | Anturin maadoitus aktivoi summerin + ESP32 keskeytyksen | Volvo alkuperäinen anturi |
| Opto 3 | D+ käyntitieto | 1kΩ / 2W | D+ aktiivinen estää starttireleen (hard interlock) | Laturin D+-napa |
| Opto 4 | Pilssi kohokytkin 1 (12V) | 1kΩ / 2W | Tilatieto | Paikallinen kelluke |
| Opto 5 | Pilssi kohokytkin 2 (12V) | 1kΩ / 2W | Tilatieto | Paikallinen kelluke |
| Opto 6 | PoE 48V valvonta | 4.7kΩ / 2W | Tilatieto | Verkon valvonta |
| Opto 7-8 | Varaus | - | - | - |

**Hard Interlock -logiikka**
- Kun D+ (opto 3) on aktiivinen, moottorin laturin lähtöjännite osoittaa, että moottori käy
- Ohjelmisto estää starttireleen aktivoinnin välittömästi (ei saa käynnistää käynnissä olevaa moottoria)

**Kierrosluku (RPM) -luenta**
- Luetaan laturin W-navasta tai induktiivisen anturin pulsseista
- ESP32:n hardware-laskuri (PCNT) lukee pulssit suoraan (ei ohjelmallista pollaamista)

---

## Merenkulkudata (NMEA)

NMEA 2000 ja NMEA 0183 -liikenne tuodaan Raspberry Pi:lle erillisten USB-sovittimien (esim. Canable, Waveshare RS485/422) kautta, joista Signal K kääntää ne MQTT- ja web-muotoon.
