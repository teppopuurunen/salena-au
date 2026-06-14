# Projektin yleiskatsaus

**Dokumentti:** Salena AU projektin yleiskuva  
**Päivitetty:** 07.06.2026  
**Tila:** Current truth -tiivistelmä

---

## Yhteenveto

Salena AU modernisoi Amigo 40 "Salena" -veneen sähkö-, automaatio- ja
navigointijärjestelmät kerrokselliseksi kokonaisuudeksi. Arkkitehtuurin
perusperiaate on, että veneen perustoiminnot toimivat ilman automaatiota.

![Salena laiturissa](images/Salena.jpg)

---

## Arkkitehtuuri tiivistettynä

Järjestelmä jakautuu kolmeen tasoon:

1. Älytaso: Raspberry Pi 5 (OpenPlotter, SignalK, OpenCPN)
2. Automaatiotaso: Rele-ESP-yksiköt, Mittaus-ESP, Akku-ESP, Valo-ESP, RS485 Modbus
3. Kenttätaso: 12 V kuormat, sulakkeet, 1-0-Auto-ohitukset

Keskeiset väylät:

- Ethernet: ensisijainen ohjaus- ja integraatioväylä
- RS485 Modbus RTU: kenttä-I/O ja ulkoiset releet
- I2C (eristetty ISO1540): virran- ja jännitemittaukset
- USB-RS422: Raymarine ST5000 -autopilotti

Lisätiedot: [architecture.md](architecture.md), [network.md](network.md)

---

## Komponenttistatus

| Komponentti | Tunnus / malli | Tila |
|---|---|---|
| Raspberry Pi 5 (8 GB) | RPi 5 | Käytössä |
| NVMe HAT+ | WS-27709 | Käytössä |
| NVMe SSD | 256/512 GB | Käytössä |
| UPS HAT (E) | WS-27966 | hankkimatta |
| RS422-USB-adapteri | ST5000 integraatio | hankittu |
| Reititin | Huawei B818-263 | Käytössä |
| Salonkinäyttö | Blackstorm M245BN 24.5" | hankittu |
| Rele-ESP 1 | ESP32-S3-ETH-8DI-8RO | hankittu |
| Rele-ESP 2 | ESP32-S3-ETH-8DI-8RO | hankittu |
| Kytkin | Teltonika TSW101 | hankittu |
| Mittaus-ESP | SKU:28771 / ESP32-S3-POE-ETH | hankittu |
| Akku-ESP | SKU:28771 / ESP32-S3-POE-ETH | hankittu |
| Valo-ESP | SKU:28771 / ESP32-S3-POE-ETH | hankittu |
| Salonkinäyttö | Blackstorm M245BN 24.5" | hankittu |
| NÖRDIC vahvistin | SGM-197 (12V, 2×40W, BT 5.0) | hankittu |
| Yamaha kaiuttimet | NS-AW194 (IPX3) | hankittu |
| Cloudberry USB-PD laturit | 120W (3 kpl, 6.0A) | hankittu |
| Modbus I/O | Waveshare SKU:26244 (3 kpl) | hankkimatta |
| Modbus AI | Waveshare SKU:25767 (analoginen syöttö) | hankkimatta |
| Modbus AO | Waveshare SKU:26211 (analoginen lähtö) | hankkimatta |
| INA228-moduulit | 3 x INA228 (high-side) | hankkimatta |
| INA3221-moduulit | 2 x Adafruit INA3221 (The Shunt Hack) | hankkimatta |
| I2C-erotin | MIKROE-1878 (ISO1540) | hankkimatta |
| MPPT-säätimet | Victron SmartSolar 75/15 | hankkimatta |
| DC-DC laturi (IT-akku) | Victron Orion-Tr Smart 12/12-18A | Asennettu |
| Pääkytkin + ACR | Blue Sea 7649 | Asennettu |
| Autopilotti | Raymarine ST5000 | Käytössä |
| Jääkaappi | Danfoss kompressori | hankkimatta |
| Lämmitin | VEVOR 5 kW Diesel | hankkimatta |
| Bilssipumput | BILGE_SMALL/MID/LARGE | hankkimatta |

Lisätiedot: [procurement.md](procurement.md), [hardware/relay_map.md](../hardware/relay_map.md)

---

## Ohjelmistostatus

| Ohjelmisto | Alusta | Tila |
|---|---|---|
| OpenPlotter | RPi 5 | Käytössä |
| SignalK | RPi 5 | Käytössä |
| OpenCPN + Suomen merikartat | RPi 5 | Käytössä |
| Home Assistant (kontti) | RPi 5 | Ei tuotannossa |
| Paikallinen Ethernet/PoE datakerros | RPi 5 + Mittaus-ESP + Akku-ESP + Valo-ESP | Käytössä arkkitehtuuritasolla |
| Rele-ESP firmware (ESPHome) | Rele-ESP 1 ja 2 | Tekemättä |
| Mittaus-ESP firmware | Mittaus-ESP | Tekemättä |
| Akku-ESP firmware | Akku-ESP | Tekemättä |
| Valo-ESP firmware | Valo-ESP | Tekemättä |

Lisätiedot: [current_state.md](current_state.md), [deployment.md](deployment.md)

---

## Projektin eteneminen (tiivistelmä)

- Taso 1 (RPi): OpenPlotter/SignalK käytössä, NVMe+UPS käytössä
- Taso 2 (automaatio): Rele-ESP pilotointi käynnissä
- Taso 2 (ohjelmisto): ESPHome-firmware ja HA-käyttöliittymä seuraavana
- Taso 3 (kuormat): sähkökeskuksen layout käynnissä, johdotus seuraavaksi

Yksityiskohtainen eteneminen: [todo.md](todo.md)

---

## Suunnitteluperiaatteet

- Manuaalinen fallback: vene toimii ilman automaatiota
- Ei pilviriippuvuutta: järjestelmä toimii paikallisesti
- Kerroksellinen arkkitehtuuri: navigointi, automaatio ja kuormat erotettu
- Ethernet ensisijaisena: Wi-Fi käyttöliittymille
- Huollettavuus: selkeät kytkennät, sulakkeet, dokumentointi
- Vaiheittainen laajennus: lisäykset ilman uudelleensuunnittelua

---

## Viitteet

- [architecture.md](architecture.md)
- [current_state.md](current_state.md)
- [design_decisions.md](design_decisions.md)
- [network.md](network.md)
- [deployment.md](deployment.md)
- [ui_dashboard.md](ui_dashboard.md)
- [procurement.md](procurement.md)
- [hardware/relay_map.md](../hardware/relay_map.md)
- [hardware/power-setup.md](../hardware/power-setup.md)
- [todo.md](todo.md)
