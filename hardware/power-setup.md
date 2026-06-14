# Salena-au: Akut, Laturit ja Paneelit

Tämä dokumentti kuvaa Amigo 40 *Salena* -veneen sähköjärjestelmän arkkitehtuurin, akkupankit ja latauslogiikan.

---

## 1. Akkupankit

Järjestelmä on jaettu kolmeen sähköisesti eristettyyn kokonaisuuteen kriittisen datan ja käynnistysvirran varmistamiseksi:

### Starttiakku
- **Käyttötarkoitus:** Pyhitetty Volvo Penta 2003 (1997) -moottorin käynnistykseen
- **Koko:** TBD (alkuperäisen moottorin spesifin mukainen)
- **Hallinta:** Blue Sea 7649 ACR-latausrele

### AGM-Hupiakusto
- **Käyttötarkoitus:** Raskaat kuormat (jääkaappi, pumput, valaistus, tuleva subbari)
- **Koko:** TBD
- **Lataus:** Kaksi itsenäistä **Victron SmartSolar MPPT 75/15** -säätimellä (ruffi- ja peräpaneelit), sekä moottorin laturilta ja Ctek M300:lta maasähköstä

### 100Ah LiFePO4 (IT-verkko / UPS-akku)
- **Käyttötarkoitus:** Täysin eristetty älyverkon akku (Pi, näyttö, vahvistin, kamerat, reititin, kytkin)
- **Koko:** 100Ah
- **Erotus:** **Victron Orion-Tr Smart 12/12-18A Isolated DC-DC** -laturi eristää akkun galvaanisesti
- **Tarkoitus:** Suojaa herkkää elektroniikkaa jännitepiikeiltä ja maasilmukoilta, jotka voisivat häiritä Ethernet-liikennettä

---

## 2. Latauslähteet

| Lähde | Laite | Teho/Malli | Kohde |
| :--- | :--- | :--- | :--- |
| **Aurinko (Ruffi)** | Victron SmartSolar MPPT | 75/15 | Hupiakku |
| **Aurinko (Perä)** | Victron SmartSolar MPPT | 75/15 | Hupiakku |
| **Maasähkö** | Ctek M300 | 25A + 4A | Hupi + Startti |
| **Moottori** | Volvo Penta Laturi | n. 50-60A | Starttiakku |
| **DC-DC Laturi** | Victron Orion-Tr Smart | 12/12-18A Isolated | Hupi -> IT-akku |

---

## 3. Tarkkuusmittaus (I2C ja High-Side Shuntit)

Virran ja jännitteen seuranta tehdään sähkökeskuksessa ESP32:lla I2C-väylän yli. Koko mittauspiiri on eristetty **MIKROE-1878 (ISO1540)** -galvaanisella eristimellä häiriöiden estämiseksi. Mittausperiaate on high-side, eli virta mitataan plus-linjoista ei miinusjohdoista.

### Päävirrat (3 × INA228, 24-bit high-side)

| Akku/Linja | Shuntti | Ohm | Huomio |
|---|---|---|---|
| **Hupiakku** | Milliohm 300A / 75mV | 0.00025 | Pääkulutus |
| **Startti/VSR-lataus** | Milliohm 100A / 75mV | 0.00075 | Moottorilataus ja pääkytkin |
| **UPS-akku (LiFePO4)** | Milliohm 100A / 75mV | 0.00075 | IT-verkko, isoloitu |

### Pienkuormat (2 × INA3221 "The Shunt Hack", 6 kanavaa ulkoisilla shunteilla)

| Kuormaryhmä | Shuntti | Ohm | Huomio |
|---|---|---|---|
| **Bilssi 1-2** | 2 × Milliohm 50A / 75mV | 0.0015 | Pilssipumput, kellukkeistetyt |
| **Laajennus 1-4** | 4 × Milliohm 20A / 75mV | 0.00375 | Tuleville kuormille varaus |

### Väylän suojaus (kriittinen)

- **Erotin:** MIKROE-1878 (ISO1540) galvaaninen erotus
- **Tehtävä:** Erottaa veneen 12V-puolen (akut, kuormat) ja ESP32/Brain-puolen (GND + VCC)
- **I2C-osoitteet:** INA3221-kortin osoite muutetaan juotospadilla väyläkonfliktin estämiseksi (0x42 + 0x43)
- **Referenssi:** Kaikkien mittauspiirien GND ankkuroituu yhteiseen järeään maapulttiin

---

## 3. Aurinkopaneelijärjestelmä (3 x 50W)
Paneelit on jaettu kahteen itsenäiseen piiriin varjostuksen hallinnan parantamiseksi:

### Ruffipaneeli (1 x 50W)
* **Tyyppi**: Taivutettava paneeli.
* **Sijainti**: Salongin luukun suojan päällä (hiukan kaareva pinta).
* **Ohjaus**: Dedikoitu MPPT-säädin eristämään ruffin varjostus muusta järjestelmästä.

### Takatolppapaneelit (2 x 50W)
* **Tyyppi**: Jäykät Victron BlueSolar -lasipaneelit (EAN: 8719076040330).
* **Sijainti**: Rosteriset takatolpat, kääntyvät ja kallistuvat NOA-kannakkeet.
* **Kytkentä**: Rinnan kytketty (parantaa tuottoa maston varjostaessa toista paneelia).



---

## 4. Hallinta ja Erotus

* **Blue Sea 7649 Add-A-Battery**: Sisältää 65A ACR-latausreleen ja Dual Circuit Plus -pääkytkimen. Järjestelmä yhdistää akut automaattisesti latauksen ajaksi ja erottaa ne kulutuksen aikana.
* **Victron Orion-Tr Smart Isolated**: Eristää UPS-akun galvaanisesti muusta verkosta. Tämä suojaa herkkää elektroniikkaa jännitepiikeiltä ja maasilmukoilta, jotka voisivat häiritä Ethernet-liikennettä.

---

## 5. Fyysinen Asennus
Kaikki komponentit on sijoitettu akkutilaan jännitehäviöiden minimoimiseksi:

* **Jäähdytys**: Laitteet on asennettu pystysuoraan seinälle ilmankierron varmistamiseksi (erityisesti Orion ja Ctek).
* **Suojaus**: ESP32-piirit on sijoitettu erilliseen IP-suojattuun koteloon suojaan akun mahdollisilta kaasuilta.
* **Kytkennät**: Kaikki laitteet on kytketty yhteiseen järeään maapulttiin potentiaalierojen välttämiseksi.
* **Mittausperiaate**: Kaikki virta- ja jännitemittaukset tehdään high-side-periaatteella plus-linjoista. INA228/INA3221 GND ankkuroidaan samaan maapulttiin.

