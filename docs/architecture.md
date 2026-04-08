# Järjestelmäarkkitehtuuri

**Versio:** v5.1.0  
**Projekti:** Integroitu veneautomaatio- ja navigointijärjestelmä (Amigo 40 “Salena”)  
**Periaate:** Vene toimii täysin ilman automaatiota. Automaatiokerros parantaa hallittavuutta ja näkyvyyttä, mutta ei ole kriittinen riippuvuus.

---

## Yleiskuva

Salena AU on kerroksellinen järjestelmä, jossa navigointi, automaatio ja 12 V kuormat on erotettu toisistaan. Kriittiset toiminnot eivät ole riippuvaisia Wi-Fi:stä, pilvestä tai Home Assistantista.

Järjestelmä jakautuu kolmeen tasoon:

- **Taso 1: Älytaso / navigointi** – Raspberry Pi 5 (OpenPlotter, SignalK, OpenCPN)
- **Taso 2: Automaatiotaso** – ESP32-S3 + RS485 Modbus kuormaohjauksiin ja mittauksiin
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
- Syöttö: Lenovo 65W USB-C DC Travel Adapter

**Hallinta ja resetointi**
- Hard Reset toteutetaan optoerottimella (PC817) RPi 5:n J2-virtapainikeliitäntään.
- Toteutus pitää äly- ja automaatiotason maat erotettuina.

**Rajapinnat**
- Ethernet ↔ ESP32-S3 rele- ja I/O-moduulit
- Ethernet ↔ Mittaus-ESP (tankit, virrat, jännitteet, PoE)
- USB–RS422 ↔ Raymarine ST5000 (autopilotti)

**Kriittisyys**
- Ei kriittinen veneen perustoiminnalle

---

### Taso 2 – ESP32-S3 + RS485 Modbus (automaatiotaso)

Automaatiotaso koostuu erillisistä, rajatuista ohjaimista. Jokaisella ohjaimella on selkeä vastuualue. Ohjainten logiikka ja fyysiset painikkeet toimivat paikallisesti, jolloin keskuskoneen tai verkon vika ei estä käyttöä.

#### Rele-ESP:t (2 kpl)

**Rooli**
- 12 V kuormien on/off-ohjaus
- Jokaiselle releelle oma painike suoraan rele-ESP:n inputtiin
- Lisäksi 8 lisäpainiketta MCP23017 I2C-laajentimen GPIO-linjoissa
- Tilatiedot ja ohjaus Ethernetin yli (RPi / valinnainen HA)

**Laiteluokka**
- ESP32-S3-ETH-8DI-8RO
- 8 relelähtöä / moduuli
- Galvaanisesti erotetut I/O:t
- Syöttö: PoE

**Periaate**
- Toimii itsenäisesti myös ilman RPi:tä ja ilman HA:ta
- Ohjaus ei ole Wi-Fi-riippuvainen (Wi-Fi vain käyttöliittymille)
- Rele-ESP 1 toimii RS485 Modbus -masterina (RS-portti valmiina)
- Rele-ESP 2 toimii paikallisena I/O- ja releohjaimena

#### Modbus RTU I/O -moduulit

**Laitteet**
- 3 x Waveshare SKU:26244 (Modbus RTU IO 8CH)
- 30A/40A ulkoiset releet tarpeen mukaan SKU:26244 DO-kanavien taakse

**Rooli**
- Tilatiedot: optoeristetyt DI-tulot
- Ulkoinen releohjaus: DO-lähdöt (Darlington sinking)
- Keskisuuret kuormat: autoreleet tai DIN-kiskokannalliset releet SKU:26244-kanaville (10A-20A)

#### Mittaus-ESP

**Rooli**
- Tankkimittaukset
- Virran- ja jänniteseuranta
- Datan välitys Raspberry Pi:lle

**Mittausperiaate**
- Mittaus-ESP lukee INA-piirit ja välittää datan Ethernetin yli.
- Pääakku: INA228 (MIKROE-4810) + 5705-HoFL2-250A-50mV-0.1%.
- Pienkuormat: INA3221 (MIKROE-4126) + 3 x HoFL2-20A-75mV-0.1%.
- I2C-väylä erotetaan ISO1540-erottimella (MIKROE-1878).

**Laitetiedot**
- SKU: 28771
- Part No.: ESP32-S3-POE-ETH

**Yhteys**
- Ethernet (PoE) ↔ Raspberry Pi

**Kriittisyys**
- Ei kriittinen; mittaus tukee valvontaa ja päätöksentekoa

#### Valaistuksen ohjaus (suunnitelma / varaus)

Valaistusratkaisu on tässä vaiheessa tarkoituksella avoin. Sähkökeskukseen varataan kapasiteetti, jotta valaistuksen toteutus voidaan tehdä myöhemmin ilman uudelleenkaapelointia.

**Nykyinen varaus**
- 2 × sulake (valaistuksen varaus)
- 2 × relekanava (valaistuksen varaus)

**Rajaus**
- Valaistus ei ole turvallisuuskriittinen toiminto
- Toteutus tehdään myöhemmin

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
- AUTO_PL, FRIDGE, HEATER ja BILGE ohjataan kenttätasolla (ei rele-ESP-kanavissa), koska kuormat ylittävät 10A relekestoluokan.
- Kriittiset kuormat toteutetaan 1-0-Auto -ohituksella.

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
- **RS485 Modbus RTU:** Rele-ESP 1 (master) ↔ kenttämoduulit (SKU:26244)
- **I2C (eristetty):** Mittaus-ESP ↔ INA228/INA3221 mittausmoduulit
- **USB:** autopilotti-adapteri (RS422)

**Verkkolaitteet**
- Reititin: Huawei B818-263 4G LTE
- Perässä kytkin: Teltonika TSW101

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
- IT-verkon syöttö toteutetaan releen NC-koskettimen kautta (fail-safe oletuksena päällä).

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
- Rele-ESP 1 hoitaa RS485 Modbus -masteroinnin ja Rele-ESP 2 paikallisen I/O-ohjauksen
- Mittaus-ESP hoitaa INA-mittauslinjan (INA228 + INA3221, eristetty I2C)
- 12 V kenttätaso on suojattu sulakkein ja säilyttää manuaalisen käytettävyyden

Järjestelmä kehittyy vaiheittain ilman, että veneen perustoiminnot muuttuvat riippuvaisiksi automaatiosta.
