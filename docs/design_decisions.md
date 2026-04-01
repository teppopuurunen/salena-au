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
INA226-mittausväylä erotetaan digitaalisella I2C-erottimella (ISO1540 tai Si8600) Mittaus-ESP:n suuntaan.

**Perustelu**  
Eristys estää hupiakun miinuksen kytkeytymisen mittausväylän kautta Brain-elektroniikan maahan.

---

## DD-11: INA226 virtamittauksen peruspiirinä

**Päätös**  
Virtamittaus toteutetaan INA226-piireillä (16-bit), enintään 16 laitetta samalla I2C-väylällä osoitteistuksen avulla.

**Perustelu**  
Tarkkuus ja skaalautuvuus riittävät venejärjestelmän monikanavaiseen mittaukseen.

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

## DD-14: RST-painikkeet MCP23017-laajentimen kautta

**Päätös**  
RST-painikkeet luetaan MCP23017 I2C-laajentimella, eikä niitä kytketä suoraan rele-ESP:n inputteihin.

**Perustelu**  
Säästää ESP32:n GPIO-resursseja ja helpottaa kaapelointia.
