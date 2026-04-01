cat > docs/current_state.md <<'EOF'
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

**Ohjelmisto**
- OpenPlotter
- SignalK
- OpenCPN (Suomen merikartat)

**Tila**
- Navigointi toimii normaalisti
- SignalK jakaa dataa sisäverkossa
- Tallennus NVMe-levylle
- UPS HAT tukee hallittua sammutusta ja parantaa virrankatkokestävyyttä

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
  - syöttö 7–36 VDC
  - Ethernet ensisijaisena väylänä

**Suunniteltu käyttö**
- 12 V kuormien on/off-ohjaus
- fyysiset painikkeet suoraan inputteihin
- tilatiedot ja ohjaus Raspberry Pi:lle (ja myöhemmin valinnainen HA)

**Tila**
- Laitteisto olemassa
- Mekaaninen ja sähköinen asennus sekä firmware ovat seuraavat vaiheet

---

## Suunnitellut mutta ei vielä toteutetut osiot

### Hankkimatta olevat kuormat

Seuraavat [relay_map.md](../hardware/relay_map.md):ssä varatut kuormat ja laitteet eivät ole vielä hankittuja:
- Jääkaappi (Danfoss, FRIDGE / M2-R4)
- Bilssipumppu (BILGE / M2-R7)
- Lämmitin VEVOR 5kW Diesel (HEATER / M2-R6)

---

### Mittaus- ja anturi-ESP ("Home-ESP")

**Suunniteltu käyttö**
- tankkimittaukset
- virran- ja jänniteseuranta

**Tila**
- Ei hankittu – ks. [relay_map.md](../hardware/relay_map.md)

### PWM / älyvalaistus (varaus ja suunta)

**Nykyinen varaus**
- 2 × sulake
- 2 × relekanava

**Todennäköinen suunta**
- paikalliset ESP-ohjaukset Ethernet-väylällä
- pieni kosketusnäyttö (ESPHome) käyttöön ja himmennykseen
- äly-LED-nauhat lattiaan ja kattoon

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
4. Anturi-ESP pilotointi: 1–3 mittausta luotettavasti USB:n yli
5. Home Assistant käyttöliittymäksi (ei-kriittinen), kun dataa on mitä näyttää
EOF
