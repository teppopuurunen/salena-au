# Projektin yleiskatsaus

**Dokumentti:** Salena AU projektin yleiskuva  
**Päivitetty:** 04/2026  
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
2. Automaatiotaso: Rele-ESP-yksiköt, Mittaus-ESP, RS485 Modbus
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
| UPS HAT (E) | WS-27966 | Käytössä |
| RS422-USB-adapteri | ST5000 integraatio | Hankittu |
| Reititin | Huawei B818-263 | Käytössä |
| Salonkinäyttö | Blackstorm M245BN 24.5" | Hankittu |
| Rele-ESP 1 | ESP32-S3-ETH-8DI-8RO | Hankittu |
| Rele-ESP 2 | ESP32-S3-ETH-8DI-8RO | Hankittu |
| Kytkin | Teltonika TSW101 | Hankkimatta |
| Mittaus-ESP | SKU:28771 / ESP32-S3-POE-ETH | Hankkimatta |
| Modbus I/O | Waveshare SKU:26244 (3 kpl) | Hankkimatta |
| INA228-moduuli | MIKROE-4810 | Hankkimatta |
| INA3221-moduuli | MIKROE-4126 | Hankkimatta |
| I2C-erotin | MIKROE-1878 (ISO1540) | Hankkimatta |
| MPPT-säätimet | Victron SmartSolar 75/15 | Hankkimatta |
| DC-DC laturi (IT-akku) | Victron Orion-Tr Smart 12/12-18A | Asennettu |
| Pääkytkin + ACR | Blue Sea 7649 | Asennettu |
| Autopilotti | Raymarine ST5000 | Käytössä |
| Jääkaappi | Danfoss kompressori | Hankkimatta |
| Lämmitin | VEVOR 5 kW Diesel | Hankkimatta |
| Bilssipumput | BILGE_SMALL/MID/LARGE | Hankkimatta |

Lisätiedot: [procurement.md](procurement.md), [hardware/relay_map.md](../hardware/relay_map.md)

---

## Ohjelmistostatus

| Ohjelmisto | Alusta | Tila |
|---|---|---|
| OpenPlotter | RPi 5 | Käytössä |
| SignalK | RPi 5 | Käytössä |
| OpenCPN + Suomen merikartat | RPi 5 | Käytössä |
| Home Assistant (kontti) | RPi 5 | Ei tuotannossa |
| Mosquitto MQTT (kontti) | RPi 5 | Ei tuotannossa |
| Rele-ESP firmware (ESPHome) | Rele-ESP 1 ja 2 | Tekemättä |
| Mittaus-ESP firmware | Mittaus-ESP | Tekemättä |

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
