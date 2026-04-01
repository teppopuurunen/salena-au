# Salena-au: Akut, Laturit ja Paneelit

Tämä dokumentti kuvaa Amigo 40 *Salena* -veneen sähköjärjestelmän arkkitehtuurin, akkupankit ja latauslogiikan.

---

## 1. Akkupankit
Järjestelmä on jaettu kolmeen sähköisesti eristettyyn kokonaisuuteen kriittisen datan ja käynnistysvirran varmistamiseksi:

* **Starttiakku**: Omistettu Volvo Penta 2003 (1997) -moottorin käynnistykseen.
* **Hupiakusto**: Syöttää yleistä kulutusta, kuten valot, pumput ja jääkaapin.
* **Brain-akku (UPS)**: Pyhitetty elektroniikalle (Raspberry Pi, 2x rele-ESP + 1x Mittaus-ESP, reititin, kytkin, kamerat). Toimii puskurina jännitevaihteluita vastaan.

---

## 2. Latauslähteet

| Lähde | Laite | Teho/Malli | Kohde |
| :--- | :--- | :--- | :--- |
| **Aurinko (Ruffi)** | Victron SmartSolar MPPT | 75/15 | Hupiakku |
| **Aurinko (Perä)** | Victron SmartSolar MPPT | 75/15 | Hupiakku |
| **Maasähkö** | Ctek M300 | 25A + 4A | Hupi + Startti |
| **Moottori** | Volvo Penta Laturi | n. 50-60A | Starttiakku |
| **DC-DC Laturi** | Victron Orion-Tr Smart | 12/12-18A Isolated | Hupi -> Brain-akku |

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
* **Victron Orion-Tr Smart Isolated**: Eristää Brain-akun galvaanisesti muusta verkosta. Tämä suojaa herkkää elektroniikkaa jännitepiikeiltä ja maasilmukoilta, jotka voisivat häiritä Ethernet-liikennettä.

---

## 5. Fyysinen Asennus
Kaikki komponentit on sijoitettu akkutilaan jännitehäviöiden minimoimiseksi:

* **Jäähdytys**: Laitteet on asennettu pystysuoraan seinälle ilmankierron varmistamiseksi (erityisesti Orion ja Ctek).
* **Suojaus**: ESP32-piirit on sijoitettu erilliseen IP-suojattuun koteloon suojaan akun mahdollisilta kaasuilta.
* **Kytkennät**: Kaikki laitteet on kytketty yhteiseen järeään miinus-kokoojakiskoon potentiaalierojen välttämiseksi.


