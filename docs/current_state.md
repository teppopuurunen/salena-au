# Nykytila

**Päivitetty:** 01/2026  
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
- INA226 16-bit mittauspiirit (osoitteistus enintään 16 kpl / väylä)
- I2C-eristys (ISO1540 tai Si8600)

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
