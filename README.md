# Salena AU - Järjestelmämäärittely v5.0.0

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

2) **Automaatiotaso (ESP32-S3 Ethernet)**
- 2 × rele-ESP (8 relelähtöä / moduuli)
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

**Ohjelmisto**
- OpenPlotter
- SignalK
- OpenCPN (Suomen merikartat)

**Rajapinnat**
- Ethernet → rele-ESP:t (ENSISIJAINEN ohjaus- ja tilaväylä)
- USB → mittaus-/anturimoduuli
- USB–RS422 → autopilotti (Raymarine ST5000)

**Rooli**
- Navigointi, dataloggaus, integraatiot ja käyttöliittymät.
- Ei kriittinen veneen perustoimintojen kannalta.

---

## 5. ESP32-S3 -moduulit (Automaatiotaso)

### 5.1 Rele-ESP (2 kpl)

**Tyyppi**
- ESP32-S3 Ethernet -relemoduuli
- 8 IO-kanavaa / moduuli
- Ethernet, RS485 (varaus), galvaaninen erotus
- Syöttö 7–36 VDC

**Käyttö**
- 12 V kuormien ohjaus (on/off)
- Painikkeet inputteihin kuormien paikallista ohjausta varten
- Tilatiedot ja ohjaus verkon yli (RPi / HA)

**Periaate**
- Toimii itsenäisesti myös ilman RPi:tä ja HA:ta.
- Ohjaus ei ole Wi-Fi-riippuvainen.

### 5.2 Mittaus-/Anturi-ESP (“Home-ESP”)

**Tyyppi**
- ESP32-S3 dev board (USB)
- Yhteys Raspberry Pi:hin USB:n kautta

**Käyttö**
- Tankkien mittaukset
- Virran- ja jänniteseuranta

**Tila**
- Laitteisto valmiina
- Firmware odottaa toteutusta

### 5.3 Tuleva PWM-valaistus

- 1–3 × ESP32 (valaistusmoduulit)
- Himmennys (PWM)
- Ei turvallisuuskriittisiä kuormia
- Painikkeet ensisijaisena ohjauksena

---

## 6. Autopilotti-integraatio

**Autopilotti**
- Raymarine ST5000 (säilytetään)

**Integraatio**
- USB–RS422-adapteri Raspberry Pi:hin
- Tavoite: tilatieto ja mahdollinen ohjaus rajapinnan yli
- Ei muutoksia alkuperäiseen toimintalogiikkaan

**Periaate**
- Digitaalinen integraatio ei saa heikentää manuaalista toimintaa tai autopilotin perusluotettavuutta.

---

## 7. Väylät ja tietoliikenne

- **Ethernet**
  - ESP32-S3 ↔ Raspberry Pi
  - ohjaus ja tilat ensisijaisesti tätä kautta
- **USB**
  - mittaukset, anturit, autopilotti (RS422)
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
- Järjestelmä voidaan eristää huoltotilaan ilman että veneen perustoiminnot menetetään.

---

## 9. Projektin nykytila (01/2026)

- Raspberry Pi 5: OpenPlotter, SignalK ja OpenCPN käytössä
- NVMe ja UPS HAT toiminnassa
- 2 × ESP32-S3 Ethernet -relemoduulia tulossa / käytettävissä
- Anturi-ESP olemassa, firmware tekemättä
- PWM-valaistus suunniteltu myöhempään vaiheeseen

---

## 10. Yhteenveto

Salena AU on vikasietoinen ja selkeästi kerrostettu venejärjestelmä, jossa:
- navigointi ja käyttöliittymät sijaitsevat Raspberry Pi:ssä,
- kuormien ohjaus toteutetaan itsenäisillä ESP32-S3 Ethernet -moduuleilla,
- manuaalinen käyttö ja sulakesuojaus säilyvät aina.

Järjestelmän päätavoite ei ole “älykäs vene”, vaan hallittava, dokumentoitu ja luotettava vene-elektroniikka.

---
