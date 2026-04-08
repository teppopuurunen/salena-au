# Suunnittelupäätökset

Tähän dokumenttiin kirjataan Salena AU -järjestelmän keskeiset arkkitehtuuri- ja suunnittelupäätökset. Tarkoitus on kuvata erityisesti *miksi* päätökset on tehty, jotta järjestelmää voidaan kehittää johdonmukaisesti myöhemmin.

---

## DD-01: Veneen on toimittava ilman automaatiota

**Päätös**  
Veneen perustoimintojen on toimittava, vaikka automaatio, keskuskone tai verkko ei olisi käytettävissä.

**Perustelu**  
Turvallisuus ja käytettävyys eivät saa olla riippuvaisia yksittäisistä vikapisteistä.

**Seuraukset**
- manuaalinen käyttö säilyy
- automaatio on avustava kerros
- vikaantuminen heikentää mukavuutta, ei turvallisuutta

---

## DD-02: Kerrosarkkitehtuuri (RPi + ESP + 12 V kenttätaso)

**Päätös**  
Järjestelmä jaetaan kolmeen tasoon:
- navigointi ja integraatiot (Raspberry Pi)
- automaatio ja I/O (ESP32-ohjaimet)
- kuormat ja suojaus (12 V kenttätaso)

**Perustelu**  
Selkeät vastuurajat parantavat huollettavuutta ja vikasietoisuutta.

---

## DD-03: Ethernet ensisijaisena automaatioväylänä

**Päätös**  
ESP-ohjainten ja Raspberry Pi:n välinen ensisijainen yhteys on Ethernet.

**Perustelu**  
Ethernet on häiriönkestävä, hyvin debugattava ja vähemmän satunnainen kuin Wi-Fi.

**Seuraukset**
- ohjaus ei ole Wi-Fi-riippuvainen
- Wi-Fi varataan käyttöliittymille

---

## DD-04: Home Assistant ei-kriittisenä kerroksena

**Päätös**  
Home Assistant toimii käyttöliittymä- ja automaatiokerroksena, mutta järjestelmän on toimittava ilman sitä.

**Perustelu**  
HA tuo hyötyä, mutta lisää riippuvuuksia ja kompleksisuutta.

---

## DD-05: Paikallinen ohjaus aina etusijalla

**Päätös**  
Fyysiset painikkeet/katkaisijat ohittavat etäohjauksen.

**Perustelu**  
Käyttäjä hallitsee venettä paikallisesti myös häiriö- ja hätätilanteissa.

---

## DD-06: Autopilotti-integraatio read-only ensin

**Päätös**  
Autopilotista luetaan data ja tehdään lokitus ennen kuin toteutetaan ohjaus.

**Perustelu**  
Ohjauspolun lisääminen navigointikriittiseen järjestelmään vaatii varmistetun protokollaymmärryksen ja vikatilojen hallinnan.

---

## DD-07: Testipenkki ennen asennusta

**Päätös**  
Uusi rauta ja firmware validoidaan testipenkissä ennen veneasennusta.

**Perustelu**  
Testipenkki vähentää riskiä, nopeuttaa debuggausta ja estää ketjuvikaantumiset veneessä.

---

## DD-08: Valaistus ei-kriittisenä järjestelmänä (varaus ja suunta)

**Päätös**  
Valaistus toteutetaan erillisenä, ei-kriittisenä mukavuusjärjestelmänä. Tässä vaiheessa pidetään vain kapasiteettivaraus (2 sulaketta + 2 relettä).

**Tila**
- PWM-valaistuksen suunnittelu ja toteutus tehdään myöhemmin

**Perustelu**  
Valaistuksen vika ei saa vaikuttaa navigointiin tai turvallisuuteen, ja toteutuksen kannattaa elää käytännön kokeilun mukaan.

---

## DD-09: RPi 5 Hard Reset optoeristyksellä (PC817 → J2)

**Päätös**  
Raspberry Pi 5 hard reset toteutetaan PC817-optoerottimella RPi 5:n J2-virtapainikeliitäntään.

**Perustelu**  
Ratkaisu säästää releitä ja erottaa älytason sekä automaatiotason maat.

---

## DD-10: I2C-eristys mittausväylään

**Päätös**  
Mittaus-ESP:n I2C-mittauslinja erotetaan digitaalisella I2C-erottimella (ISO1540, MIKROE-1878) pääasiaksi veneen 12V-puolesta.

**Perustelu**  
Eristys estää hupiakun miinuksen kytkeytymisen mittausväylän kautta Brain-elektroniikan maahan. Tämä on kriittinen galvaanisen erotuksen kannalta.

---

## DD-11: INA228 + INA3221 mittausperiaatteena

**Päätös**  
Virtamittaus toteutetaan kahdella eri tarkkuusluokalla:
- **Pääakku**: INA228 (MIKROE-4810, 20-bit) + shuntti 5705-HoFL2-250A-50mV-0.1%
- **Pienkuormat**: INA3221 (MIKROE-4126, 3-kanavainen) + 3× shuntti HoFL2-20A-75mV-0.1%

**Perustelu**  
Kaksiportainen mittaus antaa riittävän tarkkuuden sekä pääakun SOC-seuraannalle (0,1 % laboratoriotarkkuus) että pienkuormien seurantaan. INA3221 mahdollistaa 3 pilssipumpun virran mittauksen samalla väylällä.

---

## DD-12: Kriittiset >10A kuormat pois rele-ESP:ltä

**Päätös**  
AUTO_PL, FRIDGE ja HEATER ohjataan kenttätasolla 1-0-Auto-kytkimillä, ei rele-ESP-kanavilla.

**Perustelu**  
Relekortin käytettävä jatkuva kuormitusraja on 10A, joten suuremmat kuormat siirretään erilliseen ohjaukseen.

---

## DD-13: IT-verkon NC fail-safe

**Päätös**  
IT-laitteiden syöttö reititetään releen NC-koskettimen kautta.

**Perustelu**  
Verkko pysyy oletuksena päällä myös automaatiotason vikatilanteessa.

---

## DD-14: Lisäpainikkeet MCP23017-laajentimen kautta

**Päätös**  
Jokaiselle releelle kytketään oma painike suoraan rele-ESP:n inputtiin.
Lisäksi 8 lisäpainiketta luetaan MCP23017 I2C-laajentimella.

**Perustelu**  
Säästää ESP32:n GPIO-resursseja ja helpottaa kaapelointia.

---

## DD-15: RS485 Modbus master Rele-ESP 1:ssä

**Päätös**  
Rele-ESP 1:n sisäänrakennettu RS485-portti (EIA-485) toimii Modbus RTU -masterina kenttä-I/O-moduuleille (SKU:26244).
Rele-ESP 2 toimii paikallisena I/O- ja releohjaimena ilman Modbus-masterin roolia.

**Perustelu**  
- Häiriönkestävä RS485-väylä sopii sähkökeskukseen ja veneen häiriöympäristöön.
- Modbus RTU standardointi varmistaa modulaarisen ja laajennettavan rakenteen.
- Rele-ESP 1:n RS-portti on valmiina eikä vaadi erillisiä muunnoksia.
- Master-slave -malli helpottaa tilaitetojen ja releohjauksen koordinointia.

---

## DD-16: Ulkoiset 30A/40A releet SKU:26244-kanaville

**Päätös**  
Keskisuuret kuormat (10A–20A) ohjataan ulkoisilla autorehlyillä tai DIN-diskokannallisilla releillä, joiden liinit kytketään Modbus I/O -moduulin (SKU:26244) DO-lähtöjen perään.

**Perustelu**  
- SKU:26244:n sisäänrakennetut DO-lähdöt (Darlington sinking 500mA) eivät kestä 10A–20A suoraa kuormaa.
- Ulkoiset releet mahdollistavat merkittävästi suuremman kuorman ilman moduulin rikkoutumista.
- DIN-kisko-asennus vastaa teollisen automaation parhaita käytäntöjä ja helpottaa huoltoa.
- Ratkaisu on kustannustehokas: yksi ulkoinen rele maksaa alle 30EUR verrattuna 50EUR Modbus-moduuliin.
