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

---

## DD-17: Pilssipumppuautomaatio turvallisuuskriittisena toimintona

**Paatos**
- Pilssipumput jaetaan ohjaustavan mukaan:
	- **BILGE_SMALL (<10A)** ohjataan **Rele-ESP 2** -kanavalta.
	- **BILGE_SMALL:n kellukekytkin** kytketaan **Rele-ESP 2:n DI-tuloon**.
	- **BILGE_MID** ja **BILGE_LARGE** toimivat kenttatasolla suoraan sahkomekaanisella kellukekytkimella ja sulakkeella.
- DD-12:n rajaus sailyy: yli 10A kuormia ei ohjata rele-ESP:lta.
- Automaatio on valvova ja halyttava kerros, ei ensisijainen kaynnistysmekanismi.

**Perustelu**
- Pilssipumppaus on turvallisuuskriittinen toiminto ja sen on toimittava ilman RPi:ta, HA:ta tai Ethernetia.
- Pienimman pumpun paikallinen ohjaus mahdollistaa automaattisen kaynnistyksen ilman keskuskonetta.
- Keskikokoinen ja suurin pumppu pidetaan yksinkertaisena kenttatason sahkomekaanisena toteutuksena.

**Paikallinen logiikka (vain BILGE_SMALL, Rele-ESP 2)**
- DI = 1 (kelluke ylhaalla) -> rele ON -> pumppu kay
- DI = 0 (kelluke alhaalla) -> rele OFF -> pumppu seis

**Vikasietoisuus**
- Rele-ESP 2 / Ethernet / RPi / HA vika: BILGE_MID ja BILGE_LARGE toimivat edelleen kenttatasolla.
- Mittausvian vaikutus: valvonta heikkenee, mutta pumppaus ei esty.

---

## DD-18: Liike- ja lasnaolotunnistus - halytysjarjestelma ja valojenohjaus

**Paatos**

Jarjestelmaan lisataan kolme PIR-ilmaisinta: kaksi kuiviin sisatiloihin
(salonki, keulakajuutta) ja yksi IP55-luokiteltu dual-tech-ilmaisin
istumalaatikkoon/avotilaan. Halytyskaytto ja valojenohjaus kayttavat samaa
anturitietoa - erillisia antureita ei tarvita.

Halytysjarjestelman kytkenta (paalle/pois) ja istumalaatikon anturin
aktivointi hoidetaan ohjelmallisesti HA:ssa. Fyysista erillista kytkinta
ei tarvita.

PIR-antureiden sahkoinen yhteensopivuus SKU:26244:n DI-tuloihin
varmistetaan testipenkissa ennen lopullista asennuspaatosta.

**Perustelu**

Halytysjarjestelman PIR-ilmaisimet ovat koteloltaan, jannitteeltaan (12V) ja
lahtotyypiltaan (potentiaalivapaa NC-kosketin) todennakoisesti hyvin
yhteensopivia SKU:26244:n optoeristettyjen DI-tulojen kanssa. Sama tilatieto
on kaytettavissa seka halytykseen etta valojenohjaukseen HA:ssa.
NC-kytkenta varmistaa, etta johtokatko tai piirin vika nakyy aktiivisena
halytys-/vikatilana eika jaa huomaamatta.

Istumalaatikko ja peran teltta ovat sama fyysinen paikka - yksi anturi,
kayttotilanne valitaan HA:ssa halytysjarjestelmaa kytkettaessa.

**Anturit**

| Tila | Malli | Peruste |
|---|---|---|
| Salonki | Paradox NV5MF tai Bosch ISC-BPR2-W12 | Kuiva sisatila |
| Keulakajuutta | Paradox NV5MF tai Bosch ISC-BPR2-W12 | Kuiva sisatila |
| Istumalaatikko / avotila | Bosch ISC-BDL2-WP12G (IP55, dual-tech) | Saa + veneen liike. Dual-tech vaatii PIR + mikroaalto yhta aikaa - vahentaa vaaria halytyksia |

Sisatila-anturit valitaan samasta mallista -> yksi varaosa kattaa molemmat.

**Kytkentaperiaate**

```text
12V (+)  ->  PIR VCC
GND      ->  PIR GND
PIR NC   ->  SKU:26244 DI-tulo
```

NC-kytkenta: piiri on normaalitilassa suljettu. Havainto tai johtokatko
tuottaa aktiivisen halytys-/vikatilan.

**Halytysjarjestelman toimintaperiaate HA:ssa**

Halytysten kytkenta ja anturien aktivointi hoidetaan kokonaan HA:ssa.
Kayttaja kytkee halytykset paalle HA:n kayttoliittymasta (tabletti/puhelin).
Kytkennan yhteydessa valitaan sisaltyyko istumalaatikon anturi vai ei -
telttakaytossa se otetaan mukaan, purjehduksella jattetaan pois.

```text
HA: Halytykset paalle
	-> kayttaja valitsee: sisatilat / sisatilat + istumalaatikko
	-> HA seuraa valittuja DI-tiloja
	-> liikehavainto -> HA-halytys (push / aani / merkkivalo)
```

Valojenohjauksen puolella sama PIR-tilatieto voidaan kayttaa DD-08:n mukaisen
valaistusautomaation ohjaukseen. Halytys- ja valotilat erotetaan HA:ssa
toimintamoodien perusteella.

**DI-resurssien kaytto (SKU:26244)**

| DI-kanava | Kaytto |
|---|---|
| DI-x | Salonki PIR |
| DI-x | Keulakajuutta PIR |
| DI-x | Istumalaatikko PIR |

3 DI-tuloa.

**Vikasietoisuus**

- NC-kytkenta varmistaa johtokatkon tai piirin vian havaitsemisen.
- HA:n vika tarkoittaa, etta halytykset eivat toimi - hyvaksytty rajoite,
	koska halytysjarjestelma on mukavuus- eika turvallisuustoiminto tassa
	jarjestelmassa.

**Seuraukset**

- Relekanaviin ei tule muutosta.
- SKU:26244 DI-tuloista varataan 3 kpl PIR-ilmaisimille.
- Hankintalistaan lisataan 3 PIR-ilmaisinta.
- Todo-listaan lisataan hankinta-, testaus- ja HA-konfigurointitehtavat.

---

## DD-19: Salonkinaytto karttapoydan ja kipparin kayttoon

**Paatos**

Asennetaan Blackstorm 24.5" Full HD -naytto (M245BN, 12V DC) salongin seinalla
kaantyvalla mahonkisella telineella niin, etta naytto voidaan suunnata
karttapoydalle, kipparille ja matkustajille.

Naytto liitetaan HDMI:lla Raspberry Pi 5 -jarjestelmaan. Naytolla esitetaan
navigointi- ja mittarinakymat seka mastokameran kuva.

Karttapoydalle lisataan Bluetooth-nappaimisto ja Bluetooth-hiiri kayttoa varten.

Lisaksi maaritetaan seuraavat mediasisallot:
- kaynnistyksen tervetulotoivotus
- Salena-logo tai sponsorimainos
- naytonsaastajaksi videokooste parhaista purjehdus- ja veneilyhetkista

**Perustelu**

- Sama naytto palvelee seka navigointia etta salonkikayttoa ilman erillisia
	paneeleita.
- Kaantyva teline parantaa ergonomiaa eri kayttotilanteissa (kippari /
	karttapoyta / matkustajat).
- 12V-syotto on veneasennukseen luonteva eika vaadi erillista invertteria.
- Sisaltoprofiilit (tervetulo, logo/mainos, screensaver) tekevat naytosta
	myos viestinta- ja tunnelmaelementin satamassa ja vieraskaytossa.

**Seuraukset**

- Mekaaninen asennus vaatii mahonkisen kaantotelineen mitoituksen ja
	tarinankestavan kiinnityksen.
- Kayttoliittymaprofiilit on suunniteltava niin, etta navigointinakema on
	ensisijainen ajossa.
- Mediasisallot tulee tallettaa paikallisesti, jotta ne toimivat myos ilman
	internetyhteytta.
