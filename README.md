# Salena AU - Järjestelmämäärittely v5.1.0

Salena AU modernisoi klassisen Amigo 40 Salenan sähkö- ja automaatiojärjestelmät vaiheittain ja turvallisesti niin, että veneen alkuperäinen ilme säilyy, manuaalinen käyttö toimii aina, ja digitaaliset työkalut tuovat näkyvyyttä sekä hallintaa ilman pilviriippuvuutta.

## Salena

<img src="docs/images/Salena.jpg" alt="Salena laiturissa" width="420">

Salena on mahongista valmistettu Amigo 40, rakennettu vuonna 1977
prototyypiksi lasikuitusarjalle. Linjoiltaan se edustaa klassista
skandinaavista purjeveneperinnettä ja muistuttaa Colin Archerin tai
Arvid Laurinin kosterien siluettia.

Valmis ja hyvaksi havaittu mahonkiprototyyppi toimi muottina koko
lasikuitusarjalle. Kaikki Amigo 40 -veneet pohjautuvat Salenan linjoihin.

Sähköjärjestelmä on lähes alkuperäinen. 2000-luvulla on uusittu akut,
erotuskytkentä ja lisätty CTEK-lataus. Volvo Penta vaihdettiin vuonna 1993.

Salena AU -projekti tuo veneen sähkö- ja automaatiojärjestelmät 2020-luvulle.
Automaatio piilotetaan mahdollisuuksien mukaan, ja veneen alkuperäistä ilmettä
sekä klassista luonnetta kunnioitetaan kaikissa ratkaisuissa.

---

**Projekti:** Integroitu veneautomaatio- ja navigointijärjestelmä (Amigo 40 “Salena”)  
**Tavoite:** Luotettava, huollettava ja vaiheittain laajennettava kokonaisuus, jossa automaatio täydentää veneen perustoimintoja mutta ei koskaan ole niiden edellytys.

---

## 1. Yleiskuvaus

Salena AU yhdistää navigoinnin (OpenPlotter/SignalK/OpenCPN) ja veneen 12 V kuormien ohjauksen (ESP32-S3 Ethernet -moduulit) yhdeksi hallittavaksi järjestelmäksi. Järjestelmä on suunniteltu teollisen automaation periaatteilla: kerroksellisuus, selkeät rajapinnat, vikasietoisuus ja manuaalinen fallback.

Keskeinen periaate: **vene toimii täysin ilman automaatiota**. Kaikki kriittiset toiminnot säilyvät käytettävissä riippumatta verkosta, Home Assistantista tai Raspberry Pi:stä.

---

## 2. Suunnitteluperiaatteet

- **Mechanical fallback / manuaalinen ohitus:** kriittiset toiminnot ovat käytettävissä myös ilman automaatiota.
- **Ei pilviriippuvuutta:** järjestelmä toimii paikallisesti.
- **Kerroksellinen arkkitehtuuri:** navigointi, automaatio ja kuormat on erotettu.
- **Ethernet ensisijaisena ohjausväylänä:** Wi-Fi on käyttöliittymille, ei kriittiseen ohjaukseen.
- **Huollettavuus ja dokumentoitavuus:** selkeät kytkennät, sulakkeet, nimeäminen ja lokitus.
- **Vaiheittainen laajennus:** valaistus (PWM) ja lisäautomaatio voidaan lisätä ilman uudelleensuunnittelua.

---

## 3. Järjestelmäarkkitehtuuri

### 3.1 Tasot

1) **Älytaso / Navigointi (Raspberry Pi 5)**
- OpenPlotter
- SignalK
- OpenCPN (Suomen merikartat)
- Tallennus NVMe:lle
- UPS-varmistus

2) **Automaatiotaso (ESP32-S3 Ethernet + RS485 Modbus)**
- 2 × rele-ESP (8 relelähtöä / moduuli, Rele-ESP 1 = RS485 master)
- 3 × Waveshare SKU:26244 (Modbus RTU IO −tilatiedot ja ulkoinen releohjaus)
- 30A/40A ulkoiset releet SKU:26244-kanaville (keskisuuret kuormat)
- Painikkeet suoraan inputeihin (paikallinen ohjaus)
- Ethernet-yhteys RPi:hin

3) **Kenttätaso (12 V kuormat)**
- Kuormat sulakkeilla
- Releet ohjaavat (eivät suojaa)
- Manuaaliset ohitukset säilyvät

### 3.2 Ydinperiaate

- Raspberry Pi tarjoaa navigoinnin, datakeruun ja käyttöliittymät.
- ESP32-moduulit hoitavat kuormien ohjauksen ja paikallisen I/O:n.
- Kuormat ovat aina käsin hallittavissa ja suojattu sulakkeilla.

---

## 4. Raspberry Pi 5 -kokoonpano (Navigointi ja “Intelligence Layer”)

**Laitteisto**
- Raspberry Pi 5
- WS-27709: PCIe → M.2 NVMe HAT+
- WS-27966: UPS HAT (E)
- Syöttö: Lenovo 65W USB-C DC Travel Adapter

**Ohjelmisto**
- OpenPlotter
- SignalK
- OpenCPN (Suomen merikartat)

**Rajapinnat**
- Ethernet → rele-ESP:t (ENSISIJAINEN ohjaus- ja tilaväylä)
- Ethernet → Mittaus-ESP (PoE)
- USB–RS422 → autopilotti (Raymarine ST5000)

**Hallinta ja resetointi**
- Hard Reset toteutetaan optoerottimella (PC817) RPi 5:n J2-virtapainikeliitäntään.
- Ratkaisu säästää relekanavia ja pitää äly- ja automaatiotason maat erotettuina.

**Rooli**
- Navigointi, dataloggaus, integraatiot ja käyttöliittymät.
- Ei kriittinen veneen perustoimintojen kannalta.

---

## 5. ESP32-S3 -moduulit (Automaatiotaso)

### 5.1 Rele-ESP (2 kpl)

**Tyyppi**
- ESP32-S3-ETH-8DI-8RO
- 8 IO-kanavaa / moduuli
- Ethernet, RS485, galvaaninen erotus
- Syöttö: PoE

**Käyttö**
- 12 V kuormien ohjaus (on/off)
- Jokaiselle releelle liitetään oma painike suoraan rele-ESP:n inputtiin.
- Lisäksi 8 lisäpainiketta luetaan MCP23017 I2C-laajentimen kautta GPIO:lla.
- Tilatiedot ja ohjaus verkon yli (RPi / HA)
- **Rele-ESP 1:** RS485 Modbus -master kenttä-I/O-moduuleille
- **Rele-ESP 2:** paikallinen I/O- ja releohjain

**Periaate**
- Toimii itsenäisesti myös ilman RPi:tä ja HA:ta.
- Ohjaus ei ole Wi-Fi-riippuvainen.

### 5.1b Modbus RTU I/O -moduulit (3 × SKU:26244)

**Tyyppi**
- Waveshare SKU:26244 (Modbus RTU IO 8CH)
- 8 DI (optoeristetty) ja 8 DO (Darlington sinking, 500mA) per moduuli

**Käyttö**
- Tilatiedot: optoeristetyt tulot (kohokytkimet, 1-0-Auto-asennot, releiden todelliset tilat)
- Ulkoinen releohjaus: DO-lähdöt ulkoisille DIN/Motonet-releille (10A-20A kuormat)
- 30A/40A ulkoiset releet tarpeen mukaan

### 5.2 Mittaus-ESP

**Tyyppi**
- SKU: 28771
- Part No.: ESP32-S3-POE-ETH
- Yhteys Raspberry Pi:hin Ethernetin kautta (PoE)

**Käyttö**
- Tankkien mittaukset
- Virran- ja jänniteseuranta

**Mittausperiaate**
- Pääakku: INA228 (MIKROE-4810, 20-bit) + 5705-HoFL2-250A-50mV-0.1% shuntti
- Pienkuormat (3 kpl pilssipumppuja): INA3221 (MIKROE-4126, 3-kanavainen) + 3 × HoFL2-20A-75mV-0.1% shuntit
- I2C-väylä erotetaan ISO1540-erottimella (MIKROE-1878).
- Eristys estää hupiakun miinuksen kytkeytymisen mittausväylän kautta Brain-elektroniikan maahan.

**Tila**
- Laitteisto hankkimatta
- Firmware odottaa toteutusta

## 6. Autopilotin NMEA-integraatio (tiivistetty)

Autohelm ST5000 käyttää NMEA 0183 -dataa Track Control -ohjaukseen.
Viestintä on yksisuuntainen: Raspberry Pi / plotteri → autopilotti.

Minimisetti:
- APB

Suositeltu setti:
- APB, RMB, RMC

ST5000 ei lähetä NMEA 0183 -dataa takaisin. Sisäinen kompassi on rajallinen,
ja tarvittaessa voidaan käyttää ulkoista suuntatietoa (HDG/HDT).

---

## 7. Väylät ja tietoliikenne

- **Ethernet**
  - ESP32-S3 ↔ Raspberry Pi (ohjaus ja tilat)
  - Mittaus-ESP → Raspberry Pi (PoE)
  - Reititin: Huawei B818-263 4G LTE
  - Kytkin: Teltonika TSW101 (hankkimatta)
- **RS485 Modbus RTU**
  - Rele-ESP 1 (master) ↔ Modbus I/O -moduulit (SKU:26244)
  - Tilatiedot ja ulkoisen releohjauksen väylä
- **I2C (eristetty)**
  - Mittaus-ESP ↔ INA228 + INA3221 mittausmoduulit
  - ISO1540-erottimella erotettu
- **USB**
  - autopilotti NMEA 0183 (RS422)
- **Wi-Fi**
  - käyttöliittymät (tablet/puhelin), ei kriittinen ohjaus
- **Home Assistant**
  - konttina Raspberry Pi:ssä
  - käyttöliittymä ja automaatio (valinnainen)
  - ei kriittinen riippuvuus

---

## 8. Sähkö ja turvallisuus

- Kaikki kuormat sulakkeilla.
- Rele ohjaa, sulake suojaa.
- Kriittisissä toiminnoissa säilyy manuaalinen ohitus.
- IT-verkko syötetään releen NC-koskettimen kautta, jolloin verkko jää oletuksena päälle myös rele-ESP-vikatilanteessa.
- AUTO_PL, FRIDGE, HEATER ja BILGE eivät ole rele-ESP:n kuormia (relekeston raja 10A).
- Järjestelmä voidaan eristää huoltotilaan ilman että veneen perustoiminnot menetetään.

---

## 9. Projektin nykytila (04/2026)

- Raspberry Pi 5: OpenPlotter, SignalK ja OpenCPN käytössä
- NVMe toiminnassa (SSD käytössä)
- Syöttö: Lenovo 65W USB-C DC Travel Adapter
- UPS HAT (WS-27966): hankkimatta
- Kytkin: Teltonika TSW101 hankkimatta
- 2 × ESP32-S3-ETH-8DI-8RO rele-ESP:tä (PoE, hankittu)
- 3 × Waveshare SKU:26244 (Modbus RTU IO): hankkimatta
- Mittaus-ESP (SKU: 28771): hankkimatta, firmware tekemättä
- Mittauskomponentit (INA228, INA3221, shuntit, ISO1540): hankkimatta
- PWM-valaistuksen suunnitelu ja toteutus tehdään myöhemmin

---

## 10. Yhteenveto

Salena AU on vikasietoinen ja selkeästi kerrostettu venejärjestelmä, jossa:
- navigointi ja käyttöliittymät sijaitsevat Raspberry Pi:ssä,
- kuormien ohjaus ja indikointi toteutetaan kaksiväylien (RS485 Modbus + Ethernet) kautta,
- tarkka virranmittaus hoituu erillisellä I2C-mittauslinjalla (INA228 + INA3221, eristetty ISO1540:lla),
- 2× rele-ESP (Rele-ESP 1 = RS485 master, Rele-ESP 2 = paikallinen I/O) ja 3× Modbus I/O -moduuli (SKU:26244) muodostavat ohjaus- ja tilatietojen väylän,
- manuaalinen käyttö ja sulakesuojaus säilyvät aina.

Järjestelmän päätavoite ei ole “älykäs vene”, vaan hallittava, dokumentoitu ja luotettava vene-elektroniikka.

---
