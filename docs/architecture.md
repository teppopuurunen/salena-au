 cat > docs/architecture.md <<'EOF'
# Järjestelmäarkkitehtuuri

**Versio:** v5.0.0  
**Projekti:** Integroitu veneautomaatio- ja navigointijärjestelmä (Amigo 40 “Salena”)  
**Periaate:** Vene toimii täysin ilman automaatiota. Automaatiokerros parantaa hallittavuutta ja näkyvyyttä, mutta ei ole kriittinen riippuvuus.

---

## Yleiskuva

Salena AU on kerroksellinen järjestelmä, jossa navigointi, automaatio ja 12 V kuormat on erotettu toisistaan. Kriittiset toiminnot eivät ole riippuvaisia Wi-Fi:stä, pilvestä tai Home Assistantista.

Järjestelmä jakautuu kolmeen tasoon:

- **Taso 1: Älytaso / navigointi** – Raspberry Pi 5 (OpenPlotter, SignalK, OpenCPN)
- **Taso 2: Automaatiotaso** – ESP32-S3 (Ethernet) kuormaohjauksiin ja mittauksiin
- **Taso 3: Kenttätaso** – 12 V kuormat, sulakkeet, manuaalinen ohitus

---

## Tavoitteet ja reunaehdot

### Päätavoitteet
- Navigointi ja datakeruu yhdessä alustassa (RPi 5)
- Kuormien ohjaus modulaarisesti (ESP32-yksiköt)
- Vikasietoisuus ja huollettavuus
- Laajennettavuus ilman uudelleensuunnittelua

### Reunaehdot
- Veneen perustoiminnot eivät saa olla riippuvaisia:
  - Raspberry Pi:stä
  - Home Assistantista
  - Wi-Fi-yhteydestä
  - ulkoisesta verkosta / internetistä
- Kaikki kuormat suojataan sulakkeilla; ohjain ei suojaa kuormaa (rele/MOSFET vain ohjaa).

---

## Looginen arkkitehtuuri

### Taso 1 – Raspberry Pi 5 (navigointi ja integraatiot)

**Rooli**
- Navigointi (OpenCPN)
- Datan välitys ja aggregointi (SignalK)
- Dataloggaus ja integraatiot (myöhemmin HA konttina)

**Laitteisto**
- Raspberry Pi 5
- WS-27709 PCIe → M.2 NVMe HAT+
- NVMe SSD
- WS-27966 UPS HAT (E)

**Rajapinnat**
- Ethernet ↔ ESP32-S3 rele- ja I/O-moduulit
- USB ↔ anturi-/mittaus-ESP (tankit, virrat, jännitteet)
- USB–RS422 ↔ Raymarine ST5000 (autopilotti)

**Kriittisyys**
- Ei kriittinen veneen perustoiminnalle

---

### Taso 2 – ESP32-S3 (automaatiotaso)

Automaatiotaso koostuu erillisistä, rajatuista ohjaimista. Jokaisella ohjaimella on selkeä vastuualue. Ohjainten logiikka ja fyysiset painikkeet toimivat paikallisesti, jolloin keskuskoneen tai verkon vika ei estä käyttöä.

#### Rele-ESP:t (2 kpl)

**Rooli**
- 12 V kuormien on/off-ohjaus
- Paikallinen ohjaus fyysisillä painikkeilla (inputit)
- Tilatiedot ja ohjaus Ethernetin yli (RPi / valinnainen HA)

**Laiteluokka**
- ESP32-S3-ETH-8DI-8RO
- 8 relelähtöä / moduuli
- Galvaanisesti erotetut I/O:t
- Syöttö 7–36 VDC

**Periaate**
- Toimii itsenäisesti myös ilman RPi:tä ja ilman HA:ta
- Ohjaus ei ole Wi-Fi-riippuvainen (Wi-Fi vain käyttöliittymille)

#### Mittaus-/anturi-ESP (“Home-ESP”)

**Rooli**
- Tankkimittaukset
- Virran- ja jänniteseuranta
- Datan välitys Raspberry Pi:lle

**Yhteys**
- USB ↔ Raspberry Pi

**Kriittisyys**
- Ei kriittinen; mittaus tukee valvontaa ja päätöksentekoa

#### Valaistuksen ohjaus (suunnitelma / varaus)

Valaistusratkaisu on tässä vaiheessa tarkoituksella avoin. Sähkökeskukseen varataan kapasiteetti, jotta valaistuksen toteutus voidaan tehdä myöhemmin ilman uudelleenkaapelointia.

**Nykyinen varaus**
- 2 × sulake (valaistuksen varaus)
- 2 × relekanava (valaistuksen varaus)

**Todennäköinen suunta**
- Paikalliset ESP-ohjaukset Ethernet-väylällä
- Pieni kosketusnäyttö (ESPHome) käyttöön ja himmennykseen
- Äly-LED-nauhat lattiaan ja kattoon tunnelma-/mukavuusvalaistukseen

**Rajaus**
- Valaistus ei ole turvallisuuskriittinen toiminto
- Toteutus ei saa luoda uusia kriittisiä riippuvuuksia

---

### Taso 3 – Kenttätaso (12 V kuormat ja suojaus)

**Rooli**
- Kuormat (valot, pumput, elektroniikka, ym.)
- Sulakkeet ja jakelu
- Manuaalinen ohitus kriittisille toiminnoille

**Periaate**
- Sulake suojaa johdotuksen ja kuorman
- Rele/MOSFET ohjaa, ei suojaa
- Kriittisissä kuormissa säilyy käsikäyttö

---

## Autopilotti

**Autopilotti**
- Raymarine ST5000 (säilytetään)

**Integraatio**
- USB–RS422-adapteri Raspberry Pi:hin
- Lähtökohtaisesti read-only (tilojen lukeminen ja lokitus) ennen ohjaustoimintoja

**Periaate**
- Digitaalinen integraatio ei saa heikentää manuaalista toimintaa tai autopilotin perusluotettavuutta

---

## Väylät ja tiedonsiirto

### Ensisijaiset yhteydet
- **Ethernet:** ESP32-S3 ↔ Raspberry Pi (ohjaus/tilat)
- **USB:** anturit/mittaukset + autopilotti-adapteri (RS422)

### Wi-Fi:n rooli
- Wi-Fi on käyttöliittymille (tablet/puhelin)
- Wi-Fi ei ole kriittinen ohjausväylä

### Home Assistantin rooli
- Home Assistant toimii käyttöliittymänä ja ei-kriittisenä automaatiokerroksena
- Järjestelmä toimii ilman Home Assistantia

---

## Vikasietoisuus ja turvallisuus

- Ei yksittäistä kriittistä vikapistettä
- Manuaalinen ohitus kriittisille kuormille
- Verkko ja palvelut ovat lisäkerros, eivät edellytys
- Käyttöönotto etenee testipenkki ensin -periaatteella

---

## Rajaukset (tässä vaiheessa)

- Ei pilvipalveluita
- Ei Wi-Fi-riippuvaista kuormaohjausta
- Ei monoliittista “kaikki yhdessä” -ohjainta
- Valaistus jätetään auki (vain sulake + relevaraus)

---

## Yhteenveto

Salena AU on kerroksellinen ja modulaarinen kokonaisuus, jossa:
- Raspberry Pi 5 hoitaa navigoinnin ja integraatiot
- ESP32-S3-moduulit hoitavat kuormien ohjauksen ja mittaukset
- 12 V kenttätaso on suojattu sulakkein ja säilyttää manuaalisen käytettävyyden

Järjestelmä kehittyy vaiheittain ilman, että veneen perustoiminnot muuttuvat riippuvaisiksi automaatiosta.
EOF
