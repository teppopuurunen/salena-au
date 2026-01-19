cat > docs/design_decisions.md <<'EOF'
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

**Todennäköinen suunta**
- paikalliset ESP-ohjaukset Ethernet-väylällä
- pieni kosketusnäyttö (ESPHome) käyttöön ja himmennykseen
- äly-LED-nauhat lattiaan ja kattoon

**Perustelu**  
Valaistuksen vika ei saa vaikuttaa navigointiin tai turvallisuuteen, ja toteutuksen kannattaa elää käytännön kokeilun mukaan.
EOF
