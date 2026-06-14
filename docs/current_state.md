# Nykytila

**Päivitetty:** 07.06.2026  
**Projekti:** Salena AU – integroitu veneautomaatio- ja navigointijärjestelmä  
**Vene:** Amigo 40 “Salena”

Tämä dokumentti kuvaa projektin todellisen nykytilan: mikä on käytössä, mikä on hankittu mutta ei vielä ohjelmoitu, ja mitkä kokonaisuudet on jätetty tarkoituksella myöhempään vaiheeseen.

---

## Käytössä oleva järjestelmä

### Raspberry Pi 5 – navigointi ja datakerros

**Laitteisto**
- Raspberry Pi 5
- WS-27709 PCIe → M.2 NVMe HAT+
- NVMe SSD
- Syöttö: Lenovo 65W USB-C DC Travel Adapter

**Ohjelmisto**
- OpenPlotter
- SignalK
- OpenCPN (Suomen merikartat)

**Tila**
- Navigointi toimii normaalisti
- SignalK jakaa dataa sisäverkossa
- Tallennus NVMe-levylle
- UPS HAT (WS-27966): hankkimatta
- Reititin: Huawei B818-263 4G LTE
- Perässä kytkin: Teltonika TSW101 (hankittu)

### Salonkinaytto ja yhteiskaytto

**Laite**
- Blackstorm 24.5" Full HD -naytto (M245BN, 12V DC)
- Liitannat: HDMI x2, DisplayPort, USB, audio out

**Suunniteltu asennus**
- HDMI-kaapeli Raspberry Pi 5:lta naytolle
- kaantyva mahonkinen seinateline salongin seinalle
- suuntaus karttapoydalle, kipparille tai matkustajille tilanteen mukaan

**Suunniteltu kaytto**
- plotteri- ja mittarinakymat sisatiloihin
- mastokameran kuvan katselu salongista
- kaynnistyksen tervetulotoivotus
- Salena-logo tai sponsorimainos
- naytonsaastaja: videokooste purjehdus- ja veneilyhetkista

**Kayttolaitteet karttapoydalla**
- Bluetooth-nappaimisto
- Bluetooth-hiiri

**Tila**
- Naytto on hankittu
- Mekaaninen asennus ja kaantotelineen toteutus seuraavana vaiheena
- Sisaltoprofiilit toteutetaan osana UI/kioski-kayttoonottoa

### Audiosysteemi (salonki)

**Vahvistin**
- NÖRDIC SGM-197 (12V D-luokan digitaalivahvistin, 2×40W RMS, Bluetooth 5.0, AUX)
- Syöttö: UPS-akusta (LiFePO4) Cloudberry USB-PD laturin kautta

**Kaiuttimet**
- Yamaha NS-AW194 (IPX3 säänkestävät)
- Asennus: salongin seinille U-telineillä

**USB-lataus ja Virta (Cloudberry-laturit)**
- 3 × Cloudberry 120W USB-PD -autolaturit (6.0A)
- Liitännät: USB-C + USB-A
- Sijainti: sähköjakelukeskus
- Varaus per laturi: oma sulake + tupakansytytin-adapteri

**Laajennus**
- Mahdollisuus 12V aktiiviselle penkinalussubwooferille

**Tila**
- Vahvistin ja kaiuttimet hankittu
- Cloudberry-laturit hankittu (3 kpl)
- Mekaaninen asennus ja kaapelointi seuraavana vaiheena

---

## Autopilotti

**Laite**
- Raymarine ST5000

**Integraatio**
- Liitäntä Raspberry Pi:hin USB–RS422-adapterilla (valmistelussa)

**Tila**
- Autopilotti toimii itsenäisesti kuten alkuperäisessä kokoonpanossa
- Digitaalinen integraatio etenee read-only -periaatteella (ensin datan lukeminen ja lokitus)

---

## Hankittu ja asennusvalmis laitteisto

### Rele-ESP:t (automaatiotaso)

**Laitteet**
- 2 × ESP32-S3-ETH-8DI-8RO
  - 8 relelähtöä / moduuli
  - galvaanisesti erotetut I/O:t
  - syöttö PoE
  - Ethernet ensisijaisena väylänä

**Suunniteltu käyttö**
- 12 V kuormien on/off-ohjaus
- jokaiselle releelle oma painike suoraan rele-ESP:n inputtiin
- lisäksi 8 lisäpainiketta MCP23017 I2C-laajentimen GPIO-linjoissa
- tilatiedot ja ohjaus Raspberry Pi:lle (ja myöhemmin valinnainen HA)

**Tila**
- Laitteisto olemassa
- Mekaaninen ja sähköinen asennus sekä firmware ovat seuraavat vaiheet

---

## Päivitetty kokonaisuus: kaksiväyläarkkitehtuuri

Kokonaisuus on jaettu kahteen väylään:
- I2C: tarkka virranmittaus (galvaanisesti erotettu)
- RS485 Modbus: tilatiedot ja releohjaus

### 1. Akku-ESP: tarkka virranmittaus (I2C-väylä)

Akku-ESP hoitaa INA-piirien lukemisen, aggregoinnin ja datan viennin Ethernetin yli.

**Päämittaukset (3 x INA228, high-side)**
- Hupiakku: 300A/75mV shuntti (`0.00025` ohm)
- Starttiakku/VSR-latauslinja: 100A/75mV (`0.00075` ohm)
- UPS-akku: 100A/75mV (`0.00075` ohm)

**Pienkuormat ja pilssit (2 x INA3221, 6 kanavaa)**
- Bilssi 1-2: 50A/75mV (`0.0015` ohm)
- Laajennuskanavat 1-4: 20A/75mV (`0.00375` ohm)
- Toisen INA3221-kortin osoite muutetaan juotospadilla (0x42 + 0x43)

**Väylän suojaus (kriittinen)**
- Erotin: MIKROE-1878 (ISO1540)
- Tehtävä: erottaa veneen 12V-puolen ja ESP32/Brain-puolen (GND + VCC)

### 2. Tilatiedot ja ohjaus (RS485 Modbus -väylä)

**Master ja reititys**
- RS485-master: Rele-ESP 1 (RS-portti valmiina)
- Rele-ESP 2 toimii paikallisena I/O- ja releohjaimena Ethernetin yli

**Tilatiedot ja ulkoinen releohjaus (indikointi)**
- Moduulit: 3 x Waveshare SKU:26244 (Modbus RTU IO 8CH)
- Tulot: 24 DI (optoeristetty) kohokytkimille, 1-0-Auto-asennoille ja releiden todellisille tiloille
- Lähdöt: 24 DO (Darlington sinking, 500mA) ulkoisten DIN/Motonet-releiden ohjaukseen

**30A/40A ulkoiset releet (tarpeen mukaan)**
- Autoreleitä tai DIN-kiskokannoilla niille SKU:26244-kanaville, joilla halutaan ohjata keskisuuria kuormia (10A-20A)

**Moottorin turvalukitukset**
- D+ käyntitieto luetaan optokanavasta suoraan ESP32-keskeytyksellä.
- Starttireleen hard interlock on ohjelmistossa: D+ aktiivisena startti estetään.
- Starttimoottorin kulutus seurataan virtuaalishunttina starttikäskyn keston perusteella.

### 3. Täydentävät asennusosat

- Ulkoiset releet SKU:26244-kanaville, joissa kuormat ovat 10A-20A
- 12V -> 5V DC/DC-muunnin I2C-mittauspuolen eristettyyn syöttöön

### 4. 3 x ESP32-S3-POE-ETH työnjako

- Mittaus-ESP: lämpötilat, kosteudet, tankit, pilssipumppuihin liittyvät mittaukset/tilat
- Akku-ESP: akkujen ja latureiden virta- ja jännitemittaukset
- Valo-ESP: älyvalojen ohjaus (suunnitteilla)

---

## Suunnitellut mutta ei vielä toteutetut osiot

### Hankkimatta olevat kuormat

Seuraavat [relay_map.md](../hardware/relay_map.md):ssä varatut kuormat ja laitteet ovat hankkimatta:
- Jääkaappi (Danfoss, FRIDGE)
- Bilssipumput (BILGE_SMALL, BILGE_MID, BILGE_LARGE)
- Lämmitin VEVOR 5kW Diesel (HEATER)

### Releiden ulkopuoliset kuormat (kenttätaso)

- AUTO_PL (autopilotti, ST5000) - käytössä
- FRIDGE (jääkaappi) - hankkimatta
- HEATER (lämmitin) - hankkimatta
- BILGE_SMALL (bilssipumppu pieni) - hankkimatta, ohjaus Rele-ESP 2 + kelluke (DI)
- BILGE_MID (bilssipumppu keski) - hankkimatta, sahkomekaaninen kelluke + sulake
- BILGE_LARGE (bilssipumppu suuri) - hankkimatta, sahkomekaaninen kelluke + sulake

Peruste: vain BILGE_SMALL (<10A) ohjataan rele-ESP:lta; BILGE_MID ja BILGE_LARGE pysyvat kenttatasolla.

---

### 3 x ESP32-S3-POE-ETH (Mittaus-ESP, Akku-ESP, Valo-ESP)

**Laitetiedot**
- SKU: 28771
- Part No.: ESP32-S3-POE-ETH

**Suunniteltu käyttö**
- Mittaus-ESP: lämpötilat, kosteudet, tankit ja pilssipumppuihin liittyvät mittaukset/tilat
- Akku-ESP: virran- ja jänniteseuranta (akut + laturit), 3 x INA228 + 2 x INA3221
- Valo-ESP: älyvalojen ohjaus (suunnitteilla)

**Tila**
- 3 kpl hankittu
- Firmwaret toteutetaan vaiheittain työnjaon mukaisessa järjestyksessä

### RPi 5 hallinta ja resetointi

- Hard Reset toteutetaan PC817-optoerottimella RPi 5:n J2-virtapainikeliitäntään.
- Ratkaisu pitää äly- ja automaatiotason maat erotettuina.

### Painikkeiden I/O-laajennus

- 8 lisäpainiketta luetaan MCP23017 I2C-laajentimen kautta.

### PWM / älyvalaistus (varaus ja suunta)

**Nykyinen varaus**
- 2 × sulake
- 2 × relekanava

**Tila**
- toteutus tehdään myöhemmin

**Rajaus**
- valaistus ei ole turvallisuuskriittinen
- toteutus ei saa luoda uusia kriittisiä riippuvuuksia

---

### Home Assistant

**Toteutus**
- Home Assistant konttina Raspberry Pi:ssä

**Rooli**
- käyttöliittymä ja ei-kriittinen automaatio

**Tila**
- ei vielä tuotantokäytössä
- otetaan käyttöön vasta, kun rele- ja mittausdata on järkevästi saatavilla

---

## Tietoiset rajaukset tässä vaiheessa

- ei pilvipalveluita
- ei Wi-Fi-riippuvaista kuormaohjausta
- ei monoliittista “kaikki yhdessä” -ohjainta
- autopilotti-integraatio ensin read-only

---

## Seuraavat loogiset työvaiheet

1. Sähkökeskuksen mitoitus ja layout (mitat, sijoitteluperiaatteet)
2. Autopilotin testipenkki: RS422-datan kaappaus ja lokitus
3. Rele-ESP pilotointi: 1 painike → 1 rele → 1 kuorma (paikallinen logiikka)
4. Mittaus-ESP pilotointi: lämpötilat, kosteudet, tankit ja pilssipumppujen tilat
5. Akku-ESP pilotointi: akkujen ja latureiden virta- ja jännitemittaukset
6. Valo-ESP suunnittelu: älyvalojen ohjaus ja rajapinnat
7. Home Assistant käyttöliittymäksi (ei-kriittinen), kun dataa on mitä näyttää
