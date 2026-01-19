# Salena AU – Architecture

**Versio:** v5.0.0  
**Projekti:** Integroitu veneautomaatio- ja navigointijärjestelmä (Amigo 40 “Salena”)  
**Periaate:** Vene toimii täysin ilman automaatiota. Automaatiokerros parantaa hallittavuutta ja näkyvyyttä, mutta ei ole kriittinen riippuvuus.

---

## 1. Kokonaiskuva

Salena AU on kerroksellinen järjestelmä, jossa navigointi, automaatio ja 12 V kuormat on erotettu toisistaan. Ohjauksen ensisijainen perusratkaisu on paikallinen ja deterministinen: kriittiset toiminnot eivät riipu Wi-Fi:stä, pilvestä tai Home Assistantista.

Järjestelmä jakautuu kolmeen tasoon:

- **Taso 1: Älytaso / Navigointi** – Raspberry Pi 5 (OpenPlotter, SignalK, OpenCPN)
- **Taso 2: Automaatiotaso** – ESP32-S3 Ethernet -moduulit (releet, I/O, mittaukset)
- **Taso 3: Kenttätaso** – 12 V kuormat, sulakkeet ja manuaalinen ohitus

---

## 2. Tavoitteet ja reunaehdot

### 2.1 Päätavoitteet
- Navigointi ja datakeruu yhdessä alustassa (RPi 5)
- Kuormien ohjaus modulaarisesti (ESP32-yksiköt)
- Vikasietoisuus ja huollettavuus
- Laajennettavuus ilman “uudelleenrakentamista”

### 2.2 Reunaehdot
- Veneen perustoiminnot eivät saa olla riippuvaisia:
  - Raspberry Pi:stä
  - Home Assistantista
  - Wi-Fi-yhteydestä
  - ulkoisesta verkosta / internetistä
- Kaikki kuormat suojataan sulakkeilla; ohjain ei suojaa kuormaa.

---

## 3. Looginen arkkitehtuuri

### 3.1 Taso 1 – Raspberry Pi 5 (Navigation & Integration Layer)

**Rooli**
- Navigointi (OpenCPN)
- Datan välitys ja aggregointi (SignalK)
- Dataloggaus ja integraatiot (myöhemmin HA-kontti)

**Laitteisto**
- Raspberry Pi 5
- WS-27709 PCIe → M.2 NVMe HAT+
- NVMe SSD
- WS-27966 UPS HAT (E)

**Rajapinnat**
- Ethernet ↔ ESP32-S3 (ohjaus/tilat)
- USB ↔ anturi-/mittaus-ESP (tankit, virrat)
- USB–RS422 ↔ Raymarine ST5000 (autopilotti)

**Kriittisyys**
- Ei kriittinen veneen perustoiminnalle

---

### 3.2 Taso 2 – ESP32-S3 (Automation Layer)

Automaatiotaso koostuu erillisistä, rajatuista ohjaimista. Jokaisella ohjaimella on selkeä vastuualue. Ohjainten logiikka ja fyysiset painikkeet toimivat paikallisesti, jolloin keskuskoneen tai verkon vika ei estä käyttöä.

#### 3.2.1 Rele-ESP (2 kpl)

**Rooli**
- 12 V kuormien on/off-ohjaus
- Paikallinen ohjaus fyysisillä painikkeilla
- Tilatietojen jakaminen Raspberry Pi:lle

**Liitännät**
- Ethernet ensisijaisena väylänä
- Digitaaliset inputit painikkeille
- Relelähtö (kuorman katkaisu / kytkentä)

**Kriittisyys**
- Kriittiset kuormat toteutetaan siten, että manuaalinen ohitus säilyy

#### 3.2.2 Anturi-/Mittaus-ESP (“Home-ESP”)

**Rooli**
- Tankkimittaukset
- Virta- ja jännitemittaukset
- Datan välitys Raspberry Pi:lle

**Liitännät**
- USB ↔ Raspberry Pi
- Anturiliitännät (analog/digitaalinen/I²C riippuen toteutuksesta)

**Kriittisyys**
- Ei kriittinen; mittaus tukee päätöksentekoa ja valvontaa

#### 3.2.3 Valaistus-ESP:t (tuleva)

**Rooli**
- PWM-himmennys
- Ei turvallisuuskriittisiä kuormia
- Paikallinen ohjaus painikkeilla

**Liitännät**
- Ethernet tai paikallinen ohjaus, toteutus päätetään myöhemmin

---

### 3.3 Taso 3 – Kenttätaso (12 V Loads & Protection)

**Rooli**
- Kuormat (valot, pumput, elektroniikka, ym.)
- Sulakkeet ja jakelu
- Manuaalinen ohitus kriittisille toiminnoille

**Periaate**
- Sulake suojaa johdotuksen ja kuorman
- Rele/MOSFET ohjaa, ei suojaa
- Kriittisissä kuormissa säilyy käsikäyttö

---

## 4. Fyysinen topologia (korkean tason)

Korkean tason kytkentälogiikka:

- Raspberry Pi 5 on navigointi- ja integraatiokeskus
- Rele-ESP:t hoitavat kuormien ohjauksen
- Anturi-ESP tuottaa mittausdatan
- Autopilotti liitetään erillisellä adapterilla

---

## 5. Tiedonsiirto ja protokollat

### 5.1 Ensisijaiset yhteydet
- **Ethernet:** ESP32-S3 ↔ Raspberry Pi
- **USB:** anturit/mittaukset + autopilotti-adapteri

### 5.2 Wi-Fi:n rooli
- Wi-Fi on käyttöliittymille (tablet/puhelin)
- Wi-Fi ei ole kriittinen ohjausväylä

### 5.3 Home Assistantin rooli
- Home Assistant toimii käyttöliittymänä ja ei-kriittisenä automaatiokerroksena
- Järjestelmä toimii ilman Home Assistantia

---

## 6. Vikasietoisuus ja turvallisuus

### 6.1 Periaatteet
- Ei yksittäistä kriittistä vikapistettä
- Manuaalinen ohitus kriittisille kuormille
- Verkko ja palvelut ovat “lisäkerros”

### 6.2 Käyttötilat (konseptitaso)
- **Manual:** kuormat käsin, automaatio sivussa
- **Local automation:** ESP-ohjaimet toimivat paikallisesti painikkeilla ja omalla logiikalla
- **Integrated:** Raspberry Pi + (valinnainen) HA tarjoaa käyttöliittymän, lokituksen ja integraatiot

---

## 7. Rajaukset (tässä versiossa)

- Ei pilvipalveluita
- Ei Wi-Fi-riippuvaista kuormaohjausta
- Ei keskitettyä monoliittista ohjainta
- Ei CAN/NMEA2000-ydinohjausta tässä vaiheessa

Nämä rajaukset ovat tietoisia suunnittelupäätöksiä: ensisijainen tavoite on determinismi ja huollettavuus.

---

## 8. Yhteenveto

Salena AU on kerroksellinen ja modulaarinen kokonaisuus, jossa:
- Raspberry Pi 5 hoitaa navigoinnin ja integraatiot
- ESP32-S3 -moduulit hoitavat kuormien ohjauksen ja mittaukset
- 12 V kenttätaso on suojattu sulakkein ja säilyttää manuaalisen käytettävyyden

Järjestelmän kehitys voidaan tehdä vaiheittain ilman, että veneen perustoimintoihin syntyy uusia riippuvuuksia.

---
