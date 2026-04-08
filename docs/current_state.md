# Nykytila

**Päivitetty:** 04/2026  
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
- WS-27966 UPS HAT (E)
- Syöttö: Lenovo 65W USB-C DC Travel Adapter

**Ohjelmisto**
- OpenPlotter
- SignalK
- OpenCPN (Suomen merikartat)

**Tila**
- Navigointi toimii normaalisti
- SignalK jakaa dataa sisäverkossa
- Tallennus NVMe-levylle
- UPS HAT tukee hallittua sammutusta ja parantaa virrankatkokestävyyttä
- Reititin: Huawei B818-263 4G LTE
- Perässä kytkin: Teltonika TSW101

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

### 1. Tarkka virranmittaus (I2C-väylä)

Mittaus-ESP hoitaa INA-piirien lukemisen, aggregoinnin ja datan viennin Ethernetin yli.

**Pääakku (hupiakun SOC-seuranta)**
- Shuntti: 5705-HoFL2-250A-50mV-0.1% (250A, 0.1 %)
- Mittausmoduuli: MIKROE-4810 (INA228, 20-bit)

**Pienkuormat (3 kpl pilssipumppuja)**
- Shuntit: 3 x HoFL2-20A-75mV-0.1% (20A per pumppu)
- Mittausmoduuli: MIKROE-4126 (INA3221, 3 kanavaa)

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

### 3. Täydentävät asennusosat

- Ulkoiset releet SKU:26244-kanaville, joissa kuormat ovat 10A-20A
- 12V -> 5V DC/DC-muunnin I2C-mittauspuolen eristettyyn syöttöön

---

## Suunnitellut mutta ei vielä toteutetut osiot

### Hankkimatta olevat kuormat

Seuraavat [relay_map.md](../hardware/relay_map.md):ssä varatut kuormat ja laitteet eivät ole vielä hankittuja:
- Jääkaappi (Danfoss, FRIDGE)
- Bilssipumppu (BILGE)
- Lämmitin VEVOR 5kW Diesel (HEATER)

### Releiden ulkopuoliset kuormat (kenttätaso)

- AUTO_PL (autopilotti, ST5000) - käytössä
- FRIDGE (jääkaappi) - hankkimatta
- HEATER (lämmitin) - hankkimatta
- BILGE (bilssipumppu) - hankkimatta

Peruste: kuormat ylittävät rele-ESP:n 10A kuormitusrajan.

---

### Mittaus-ESP

**Laitetiedot**
- SKU: 28771
- Part No.: ESP32-S3-POE-ETH

**Suunniteltu käyttö**
- tankkimittaukset
- virran- ja jänniteseuranta
- INA228 (MIKROE-4810) pääakun tarkkaan mittaukseen
- INA3221 (MIKROE-4126) 3-kanavaiseen pienkuormamittaukseen
- I2C-eristys ISO1540:lla (MIKROE-1878)

**Tila**
- Ei hankittu – ks. [relay_map.md](../hardware/relay_map.md)

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
4. Mittaus-ESP pilotointi: 1–3 mittausta luotettavasti Ethernet/PoE:n yli
5. Home Assistant käyttöliittymäksi (ei-kriittinen), kun dataa on mitä näyttää
