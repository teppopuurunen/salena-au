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

## Fyysinen sijoittelu ja sähkösolmut (tarkennus)

### I. Sijoittelu ja solmut

| Sijainti | Komponentit | Rooli |
|---|---|---|
| Peräsolmu (akkutila) | Startti-, hupi- ja UPS-akut, 3 x high-side pääshuntti, yhteinen maapultti, Victron Orion DC-DC, Victron MPPT:t, Mittaus-ESP + Akku-ESP (SKU:28771) | Energian tuotanto, varastointi ja pääakkujen seuranta |
| Kabiinisolmu (kaappi) | Raspberry Pi 5, 2 x Rele-ESP, 2 x Teltonika TSW101, 2 x Motonet-sulakerasia, 1-0-Auto -teollisuuskytkimet, DIN-kisko Modbus-relekotelo (SKU:26244) | Järjestelmän aivot, kuormien ohjaus, IT-infra |

### II. Miinuslinja ja shuntit (tähtimaadoitus)

Tämä on järjestelmän sähköinen peruskivi: kaikki virta pakotetaan kulkemaan shunttien läpi.

**Yksi absoluuttinen maa**
- Kaikkien akkujen miinusnavat, moottorin lohko ja kaikkien laitteiden GND kytketään samaan järeään maapulttiin.
- Mittauspiirien (INA228/INA3221) GND ankkuroidaan samaan maapulttiin absoluuttisen 0V referenssin ylläpitämiseksi.
- Mittaus tehdään high-side-periaatteella plus-linjoista, ei miinusjohdoista.

**High-side shuntit + linjoilla**
- Hupiakku: 300A/75mV shuntti (`0.00025` ohm)
- Starttiakku/VSR-latauslinja: 100A/75mV shuntti (`0.00075` ohm)
- UPS-akku: 100A/75mV shuntti (`0.00075` ohm)

### III. Syöttöjohtojen mitoitus (2 m veto perästä kabiiniin)

Mitoitus perustuu jännitehäviön minimointiin (clean power -periaate).

| Linja | Koko (mm2) | Perustelu |
|---|---|---|
| Startti (+/-) | 25 mm2 | Volvo Penta 2003 käynnistysvirta |
| Hupi plus | 16 mm2 | Päävirta jääkaapille, lämmittimelle ja pumpuille |
| Hupi miinus | 16 mm2 | Erillinen paluutie hupikuormille, ei häiriöitä IT-puolelle |
| IT plus | 16 mm2 | Victron Orionilta stabiili jännite RPi:lle ja ESP:ille |
| IT miinus | 16 mm2 | Häiriötön referenssimiinus herkkää mittausdataa varten |

### IV. Automaatio ja mittaus (ESP-yksiköt)

- **Mittaus-ESP (perä):** lukee lämpötilat, kosteudet, tankit ja pilssipumppuihin liittyvät mittaukset/tilat ja lähettää datan Ethernet/PoE:lla Raspberry Pi 5:lle.
- **Akku-ESP (perä):** lukee I2C-väylällä (1 × ISO1540-erotin) INA228- ja INA3221-kanavat ja lähettää datan Ethernet/PoE:lla Raspberry Pi 5:lle.
- **Rele-ESP 1 ja 2 (kabiini):** ohjaavat 12V-kuormia; painikkeet kytketty suoraan DI-tuloihin paikallislogiikkaa varten.
- **1-0-Auto-ohitus:** mekaaninen ohitus säilyy; "1"-asennossa kytkin ohittaa ESP-releen.

### V. Verkko ja IT-infra

- **Reititin:** Huawei B818 (DHCP-master ja internet-gateway)
- **Kytkimet:** 2 x Teltonika TSW101 (PoE+), syöttävät datan ja virran ESP-moduuleille

**Topologia**
- RPi 5 -> Huawei LAN 1 (ei-PoE)
- Teltonika 1 -> Huawei LAN 2 (uplink)
- Teltonika 2 -> Teltonika 1 (daisy-chain) tai tähteen suoraan Huaweihin
- Kaikki ESP:t -> Teltonikan PoE-portteihin (portit 1-4)

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
- Ethernet ↔ Mittaus-ESP (lämpötilat, kosteudet, tankit, pilssit, PoE)
- Ethernet ↔ Akku-ESP (virrat, jännitteet, PoE)
- Ethernet ↔ Valo-ESP (älyvalot, PoE)
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

**Periaate ja Failover**
- Toimii itsenäisesti myös ilman RPi:tä ja ilman HA:ta
- Ohjaus ei ole Wi-Fi-riippuvainen (Wi-Fi vain käyttöliittymille)
- **Rele-ESP 1 toimii RS485 Modbus -masterina** (RS-portti valmiina, aktiivinen hallinta)
- **Rele-ESP 2 toimii varalla-masterina ja paikallisena I/O-releohjaimena**
  - Jos Rele-ESP 1 ei lähetä heartbeatia 3 sekuntiin tai sen RS485-portti kaatuu, Rele-ESP 2 ottaa Modbus-väylän Master-roolin
  - Taataan vikasietoinen kuormanohjaus: mitään kuormaa ei jää ilman hallintaa

#### Modbus RTU I/O -moduulit (DI/DO)

**Laitteet**
- 3 × Waveshare SKU:26244 (Modbus RTU IO 8CH DI/DO)
- 30A/40A ulkoiset releet tarpeen mukaan SKU:26244 DO-kanavien taakse

**Rooli**
- Tilatiedot: optoeristetyt DI-tulot (kohokytkimet, 1-0-Auto asenot, releiden todellinen tila)
- Ulkoinen releohjaus: DO-lähdöt (Darlington sinking, 500mA)
- Keskisuuret kuormat: autoreleet tai DIN-kiskokannalliset releet SKU:26244-kanaville (10A-20A)

#### Modbus RTU Analogiamuunnokset (AI/AO)

**Analoginen syöttö (AI) – Waveshare SKU:25767**
- Lukee 0-5V analogisia signaaleja (tankkien pinnanmittaus, säätöpotentiometrit)
- Käyttötarkoitus:
  - Sepin pinnanmittaus: Simarine STR1 tutka (0-5V) → tankin täyttöastetta (%)
  - Puhdasveden pinnanmittaus: Hydrostaattinen uppoanturi (0-5V)
  - Dieseltankkien mittaus: 2 × KUS-sauvat signaalimuuntimien kautta (0-5V)
  - Säätöpotentiometrit ohjaamon pyöreille säädöille (himmennin, lämpötila, jne)

**Analoginen lähtö (AO) – Waveshare SKU:26211**
- Antaa 0-10V ohjaussignaaleja (PWM-himmennykseen, säätöpotentiarometreihin)
- Käyttötarkoitus:
  - PWM-LED-himmennykselle portaaton säädön mahdollistus
  - Säätöpotentiometrin paluusignaalit (0-10V) luetaan AI-tuloon, AO-lähtö ohjaa toimilaitteita

**Väylä ja erotus**
- Yhteydessä Modbus RTU -väylään (Rele-ESP 1 masteri)
- Kierretty parikaapeli (varjo sähkökeskuksesta säätöpotentiometreille)
- 10V referenssijännite tuodaan DC-DC-muuntimelta puhtaan signaalintason varmistamiseksi

#### Mittaus-ESP + Akku-ESP + Valo-ESP

**Rooli**
- **Mittaus-ESP:** lämpötilat, kosteudet, tankit ja pilssipumppuihin liittyvät mittaukset/tilat (sijainti: perä)
- **Akku-ESP:** virran- ja jänniteseuranta (sijainti: perä, sähkökeskus). Lukee INA-piirien I2C-väylällä ja välittää datan Ethernetin yli
- **Valo-ESP:** älyvalojen ohjaus (suunnitteilla, sijainti: TBD)
- Datan välitys Raspberry Pi:lle

**Mittausperiaate (Akku-ESP)**
- Akku-ESP lukee INA-piirit I2C-väylällä ja välittää datan Ethernetin yli
- 3 × INA228 high-side mittaukseen (galvaanisesti erillään):
  - Hupiakku: Milliohm 300A/75mV (`0.00025` ohm)
  - Startti/VSR-latauslinja: Milliohm 100A/75mV (`0.00075` ohm)
  - UPS-akku: Milliohm 100A/75mV (`0.00075` ohm)
- 2 × Adafruit INA3221 (The Shunt Hack, ulkoiset shuntit), 6 kanavaa:
  - Bilssi 1-2: Milliohm 50A/75mV (`0.0015` ohm)
  - Laajennus 1-4: Milliohm 20A/75mV (`0.00375` ohm)
- I2C-väylä erotetaan 1 × ISO1540-erottimella (MIKROE-1878)
- Toisen INA3221-kortin osoite muutetaan juotospadilla väyläkonfliktin estämiseksi (0x42 + 0x43)

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
- AUTO_PL, FRIDGE, HEATER, BILGE_MID ja BILGE_LARGE ohjataan kenttätasolla (ei rele-ESP-kanavissa), koska kuormat ylittävät 10A relekestoluokan.
- BILGE_SMALL (<10A) ohjataan Rele-ESP 2:lta, ja sen kellukekytkin luetaan Rele-ESP 2:n DI-tuloon paikallislogiikalla.
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
- **I2C (eristetty):** Akku-ESP ↔ INA228/INA3221 mittausmoduulit
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

### Taso 3 – Moottorin integraatio (Volvo Penta 2003)

**Periaate**
- Moottorin alkuperäinen paneeli säilyy rinnalla täysin toimintakuntoisena
- Raskaat 12V-sähköt pidetään galvaanisesti erillään dataverkosta
- Turvallisuus ja telemetria hoituvat ohjelmiston hard interlockilla

**Ohjaus (ESP32 optoeristetyillä releillä)**
- Rele-ESP 2:n DO-lähdöt maadoittavat apureleiden kelat
- Napa 15 (virta) kytketään virtalukon rinnalle (1-0-Auto -kytkimellä)
- Napa 50 (startti) käyttää 70A järeää relettä, jonka kelassa on 1N4007-estosuuntadiodi

**Laitteistotason turvallisuus (optokanavat)**
- Laturin D+-nasta: luetaan ESP32-keskeytyksellä SparkFun-optoerrottimen (BOB-09118) läpi
- Öljynpainehälytys: luetaan optokanavasta (Volvo alkuperäinen anturi)
- Jäähdytysvesihälytys: luetaan optokanavasta (Volvo alkuperäinen anturi)
- Optokanavien etuvastukset: 1kΩ / 2W

**Ohjelmiston Interlock-logiikka**
- Hard Interlock: Kun D+ on aktiivinen (moottori käy), startin käynnistyminen estetään ohjelmassa
- Öljynpaineen ja jäähdytysveden hälytykset aktivoivat summerin ja ESP32-keskeytyksen
- Turvallisuusperiaate: ohjelmisto ei saa antaa starttireleen aktivoida itseään käynnissä olevan moottorin kanssa

**Telemetria**
- Kierrosluku (RPM): luetaan laturin W-navasta tai induktiivisen anturin pulsseista suoraan ESP32:n hardware-laskurilla (PCNT)
- Startin kulutus: lasketaan matemaattisesti vetokäskyn keston perusteella (virtuaalishuntti)
- Kaikki telemetria välitetään Ethernetin yli Raspberry Pi:lle

### Taso 3 – IT-media ja Äänentoisto (Salonki)

**Periaate**
- Viihteen arkkitehtuuri on rakennettu energiatehokkaaksi ilman tyhjäkäyntihäviöitä tuottavia 230V inverttereitä
- Äänijärjestelmä syötetään 12V LiFePO4-akusta, tuetaan Cloudberry USB-PD laturilla

**Näyttö ja Plotteri**
- Blackstorm M245BN 24.5", saa kuvan HDMI:llä Raspberry Pi:ltä (Home Assistant / Navigointi)
- Syöttö: 12V DC, UPS-akusta

**Audiosysteemi**
- Vahvistin: NÖRDIC SGM-197 (kompakti 12V D-luokan digitaalivahvistin, BT 5.0, AUX, $2 \times 40\text{W}$ RMS)
- Kaiuttimet: Yamaha NS-AW194 (IPX3 säänkestävät) salongissa U-asennustelineillä
- Laajennus: mahdollisuus 12V aktiivisella penkinalussubwooferilla NÖRDIC:in Sub Out -liitännästä

**Signaalireititys ja Maasilmukan esto**
- Reitti: RPi $\rightarrow$ HDMI $\rightarrow$ Blackstorm-näyttö $\rightarrow$ 3.5mm/RCA $\rightarrow$ NÖRDIC-vahvistin
- Jos maalenkit aiheuttavat digitaalista surinaa, RCA-linjaan lisätään passiivinen galvaaninen maaerotin (Ground Loop Isolator)

**UPS ja Lataus (IT-verkko)**
- Arctic Marine -sulakerasiasta otetaan virta Cloudberry 120W USB-PD -autolaturiin
- Cloudberry: 6.0A autolaturit jännitenäytöllä (USB-C + USB-A)
- Sähkökeskukseen varataan 3 x Cloudberry-laturille omat sulakkeet ja tupakansytytin-adapterit

---

## Vikasietoisuus ja turvallisuus

- Ei yksittäistä kriittistä vikapistettä
- Manuaalinen ohitus kriittisille kuormille
- Verkko ja palvelut ovat lisäkerros, eivät edellytys
- Käyttöönotto etenee testipenkki ensin -periaatteella
- IT-verkon syöttö toteutetaan releen NC-koskettimen kautta (fail-safe oletuksena päällä).
- D+ signaalin hard interlock estää starttireleen ohjauksen välittömästi moottorin käydessä.

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
- Akku-ESP hoitaa INA-mittauslinjan (INA228 + INA3221, eristetty I2C)
- Mittaus-ESP hoitaa lämpötila-, kosteus-, tankki- ja pilssidatan
- Valo-ESP on varattu älyvalojen ohjaukseen
- 12 V kenttätaso on suojattu sulakkein ja säilyttää manuaalisen käytettävyyden

Järjestelmä kehittyy vaiheittain ilman, että veneen perustoiminnot muuttuvat riippuvaisiksi automaatiosta.
