# Salena AU – Current Status

**Päivitetty:** 01 / 2026  
**Projekti:** Salena AU – Integroitu veneautomaatio- ja navigointijärjestelmä  
**Vene:** Amigo 40 “Salena”

Tämä dokumentti kuvaa projektin **todellisen nykytilan**: mikä on käytössä, mikä on rakennettu mutta ei vielä ohjelmoitu, ja mitkä kokonaisuudet on jätetty tarkoituksella myöhempään vaiheeseen.

---

## 1. Käytössä oleva järjestelmä

### 1.1 Raspberry Pi 5 – Navigointi ja datakerros

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
- Järjestelmä käynnissä ja vakaa
- Navigointi toimii normaalisti
- SignalK jakaa dataa sisäverkossa
- Tallennus NVMe-levylle
- UPS HAT antaa hallitun sammutuksen ja suojaa virtakatkoilta

---

### 1.2 Autopilotti

**Laite**
- Raymarine ST5000

**Integraatio**
- USB–RS422-adapteri Raspberry Pi:hin

**Tila**
- Autopilotti toimii itsenäisesti kuten alkuperäisessä kokoonpanossa
- Digitaalinen liitäntä Raspberry Pi:hin valmisteilla
- Ei muutoksia ST5000:n perustoimintaan

---

## 2. Hankittu ja asennusvalmis laitteisto

### 2.1 Rele-ESP:t (Automaatiotaso)

**Laitteet**
- 2 × ESP32-S3 Ethernet -relemoduuli
  - 8 IO-kanavaa / moduuli
  - Galvaaninen erotus
  - Syöttö 7–36 VDC
  - Ethernet ensisijaisena väylänä

**Suunniteltu käyttö**
- 12 V kuormien on/off-ohjaus
- Fyysiset painikkeet suoraan ESP:n inputteihin
- Ethernet-yhteys Raspberry Pi:hin

**Tila**
- Laitteet hankittu
- Mekaaninen ja sähköinen asennus seuraava vaihe
- Firmware vielä tekemättä / viimeistelemättä

---

### 2.2 Mittaus- ja anturi-ESP (“Home-ESP”)

**Laite**
- ESP32-S3 dev board (USB)

**Suunniteltu käyttö**
- Tankkimittaukset
- Virran- ja jänniteseuranta

**Tila**
- Laitteisto olemassa
- Kytkentä Raspberry Pi:hin USB:n kautta
- Firmware kokonaan tekemättä
- Odottaa ohjelmistovaihetta

---

## 3. Suunnitellut mutta ei vielä toteutetut osiot

### 3.1 PWM-valaistus

**Periaate**
- 1–3 erillistä ESP32-moduulia
- PWM-himmennys
- Ei turvallisuuskriittisiä kuormia

**Ohjaus**
- Fyysiset painikkeet ensisijaisena
- Home Assistant vain lisäkäyttöliittymänä

**Tila**
- Arkkitehtuuri päätetty
- Laitteita ei vielä hankittu
- Toteutus ajoittuu myöhempään vaiheeseen

---

### 3.2 Home Assistant

**Toteutus**
- Home Assistant konttina Raspberry Pi:ssä

**Rooli**
- Käyttöliittymä
- Tilatiedot
- Automaatiot (ei kriittiset)

**Tila**
- Ei vielä tuotantokäytössä
- Ei riippuvuutta veneen perustoimintoihin
- Otetaan käyttöön vasta rele- ja mittaus-ESP:ien jälkeen

---

## 4. Tietoisesti tekemättä jätetyt asiat (tässä vaiheessa)

- Ei pilvipalveluita
- Ei Wi-Fi-riippuvaista kuormaohjausta
- Ei CAN/NMEA2000-suoraa ohjauslogiikkaa
- Ei keskitettyä “kaikki yhdessä” -ohjainta

Nämä rajaukset ovat **tietoisia suunnittelupäätöksiä**, eivät puutteita.

---

## 5. Seuraavat loogiset työvaiheet

1. Rele-ESP:ien mekaaninen asennus ja johdotus
2. Rele-ESP firmware:
   - paikallinen ohjaus
   - Ethernet-rajapinta
3. Anturi-ESP firmware:
   - tankit
   - virrat
4. Autopilotin RS422-datan lukeminen Raspberry Pi:ssä
5. Home Assistantin käyttöönotto ei-kriittisenä käyttöliittymänä

---

## 6. Yhteenveto

Tällä hetkellä Salena AU -projekti on selkeästi kahdessa tilassa:

- **Navigointi ja datakerros:** käytössä ja vakaa  
- **Automaatiokerros:** laitteet hankittu, ohjelmistotyö edessä  

Perusrakenne on valmis ja testattu käytännössä. Jatkokehitys keskittyy hallitusti automaatioon ilman, että veneen toiminnallisuus missään vaiheessa heikkenee.

---
