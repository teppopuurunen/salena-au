# Salena AU – Projektin yleiskatsaus

**Päivitetty:** 04/2026 · **Versio:** v5.1.0  
**Vene:** Amigo 40 "Salena" (mahonki, 1977)

---

## Vene

<img src="images/Salena.jpg" alt="Salena laiturissa" width="420">

Salena on mahongista valmistettu Amigo 40, rakennettu vuonna 1977 prototyypiksi
lasikuitusarjalle. Sähköjärjestelmä on lähes alkuperäinen. Salena AU -projekti
tuo sen 2020-luvulle.

---

## Järjestelmäarkkitehtuuri

```mermaid
graph TD
    subgraph L1["Taso 1 – Älytaso (Raspberry Pi 5)"]
        RPi["🖥️ Raspberry Pi 5\nOpenPlotter · SignalK · OpenCPN\nNVMe SSD · UPS HAT"]
        HA["🏠 Home Assistant\n(konttina, valinnainen)"]
        RPi --> HA
    end

    subgraph L2["Taso 2 – Automaatiotaso (ESP32-S3)"]
        RE1["⚡ Rele-ESP 1\nESP32-S3-ETH-8DI-8RO\n8 relettä · RS485 Modbus master\nPoE"]
        RE2["⚡ Rele-ESP 2\nESP32-S3-ETH-8DI-8RO\n8 relettä · paikallinen I/O\nPoE"]
        MESP["📊 Mittaus-ESP\nESP32-S3-POE-ETH\nINA228 + INA3221\n(hankkimatta)"]
        M1["📦 Modbus I/O 1\nSKU:26244\n8DI + 8DO\n(hankkimatta)"]
        M2["📦 Modbus I/O 2\nSKU:26244\n8DI + 8DO\n(hankkimatta)"]
        M3["📦 Modbus I/O 3\nSKU:26244\n8DI + 8DO\n(hankkimatta)"]
        RE1 -- "RS485 Modbus RTU" --> M1
        RE1 -- "RS485 Modbus RTU" --> M2
        RE1 -- "RS485 Modbus RTU" --> M3
    end

    subgraph L3["Taso 3 – Kenttätaso (12 V kuormat)"]
        NAV["🔦 Navigointi\nNAV_RUN · NAV_ANC\nNAV_MOT · NAV_COM\nNAV_IO"]
        IT["🌐 IT-verkko\nNET_IT · CAM · USB_PWR"]
        LOADS["🔌 Muut kuormat\nFRIDGE · HEATER\nAUTO_PL\n(kenttätaso, 1-0-Auto)"]
        BILGE["💧 Bilssipumput\nBILGE_SMALL (ESP2 + DI)\nBILGE_MID + BILGE_LARGE\n(sahkömek. kelluke)"]
    end

    RPi -- "Ethernet" --> RE1
    RPi -- "Ethernet" --> RE2
    RPi -- "Ethernet / PoE" --> MESP
    RPi -- "USB–RS422" --> AP["🧭 Autopilotti\nRaymarine ST5000"]
    RE1 -- "8 relettä" --> NAV
    RE2 -- "8 relettä" --> IT
    M1 & M2 & M3 -- "DO → ulkoiset releet" --> LOADS
    RE2 -- "BILGE_SMALL rele" --> BILGE
```

---

## Verkko ja väylät

```mermaid
graph LR
    subgraph ETH["Ethernet (ensisijainen)"]
        SW["🔀 Teltonika TSW101\n(hankkimatta)"]
        RT["📡 Huawei B818-263\n4G LTE"]
    end

    RPi5["🖥️ RPi 5"] -- "Ethernet" --- SW
    SW -- "Ethernet / PoE" --- RE1E["⚡ Rele-ESP 1"]
    SW -- "Ethernet / PoE" --- RE2E["⚡ Rele-ESP 2"]
    SW -- "Ethernet / PoE" --- MESPE["📊 Mittaus-ESP"]
    SW --- RT

    RE1E -- "RS485 Modbus RTU" --- MBUS["📦 3× SKU:26244"]

    MESPE -- "I2C (ISO1540 eristys)" --- INA["INA228 + INA3221\nmittausmoduulit"]

    RPi5 -- "USB–RS422" --- ST5["🧭 ST5000"]

    RT -- "Wi-Fi" --- UI["📱 Tabletti / Puhelin\n(käyttöliittymät)"]
```

---

## Komponenttistatus

| Komponentti | Tunnus / Malli | Tila |
|:---|:---|:---:|
| Raspberry Pi 5 (8 GB) | RPi 5 | ✅ Käytössä |
| NVMe HAT+ | WS-27709 | ✅ Käytössä |
| NVMe SSD | 256/512 GB | ✅ Käytössä |
| UPS HAT (E) | WS-27966 | ✅ Käytössä |
| RS422→USB-adapteri | ST5000 | ✅ Hankittu |
| Reititin | Huawei B818-263 | ✅ Käytössä |
| Mastokamera | Tapo C500 | ✅ Hankittu |
| Salonkinäyttö | Blackstorm M245BN 24.5" | ✅ Hankittu |
| Rele-ESP 1 | ESP32-S3-ETH-8DI-8RO | ✅ Hankittu |
| Rele-ESP 2 | ESP32-S3-ETH-8DI-8RO | ✅ Hankittu |
| Kytkin | Teltonika TSW101 | ❌ Hankkimatta |
| Mittaus-ESP | SKU:28771 / ESP32-S3-POE-ETH | ❌ Hankkimatta |
| Modbus I/O 1 | Waveshare SKU:26244 | ❌ Hankkimatta |
| Modbus I/O 2 | Waveshare SKU:26244 | ❌ Hankkimatta |
| Modbus I/O 3 | Waveshare SKU:26244 | ❌ Hankkimatta |
| Pääakun shuntti | HoFL2-250A-50mV-0.1% | ❌ Hankkimatta |
| Pienkuormashuntit | 3× HoFL2-20A-75mV-0.1% | ❌ Hankkimatta |
| INA228-moduuli | MIKROE-4810 | ❌ Hankkimatta |
| INA3221-moduuli | MIKROE-4126 | ❌ Hankkimatta |
| I2C-erotin | MIKROE-1878 (ISO1540) | ❌ Hankkimatta |
| Aurinkopaneelit (3 × 50 W) | Victron BlueSolar + taivutettava | ✅ Asennettu |
| MPPT-säätimet | Victron SmartSolar 75/15 | ❌ Hankkimatta |
| DC-DC laturi (brain-akku) | Victron Orion-Tr Smart 12/12-18A | ✅ Asennettu |
| Pääkytkin + ACR | Blue Sea 7649 | ✅ Asennettu |
| Autopilotti | Raymarine ST5000 | ✅ Käytössä |
| Jääkaappi | Danfoss kompressori | ❌ Hankkimatta |
| Lämmitin | VEVOR 5 kW Diesel | ❌ Hankkimatta |
| Bilssipumput (3 kpl) | BILGE_SMALL/MID/LARGE | ❌ Hankkimatta |
| PIR-ilmaisimet (3 kpl) | Paradox NV5MF / Bosch | ❌ Hankkimatta |

---

## Ohjelmistostatus

| Ohjelmisto | Alusta | Tila |
|:---|:---|:---:|
| OpenPlotter | RPi 5 | ✅ Käytössä |
| SignalK | RPi 5 | ✅ Käytössä |
| OpenCPN + Suomen merikartat | RPi 5 | ✅ Käytössä |
| Home Assistant (kontti) | RPi 5 | ❌ Ei tuotannossa |
| Mosquitto MQTT (kontti) | RPi 5 | ❌ Ei tuotannossa |
| Rele-ESP firmware (ESPHome) | Rele-ESP 1 & 2 | ❌ Tekemättä |
| Mittaus-ESP firmware | Mittaus-ESP | ❌ Tekemättä |

---

## Relekartta (yhteenveto)

```mermaid
graph LR
    subgraph RE1["Rele-ESP 1 – Navigointi & IT (10.10.10.11)"]
        R1["R1 NAV_RUN\nKulkuvalot\n5A F1"]
        R2["R2 NAV_ANC\nAnkkurivalo\n5A F2"]
        R3["R3 NAV_MOT\nAjovalo\n7.5A F3"]
        R4["R4 NAV_COM\nKompassivalo\n2A F4"]
        R5["R5 NAV_IO\nMittaristo/NMEA\n5A F11"]
        R6["R6 NET_IT\nReititin/Kytkin\n5A F12"]
        R7["R7 CAM\nKamerat\n5A F14"]
        R8["R8 USB_PWR\nUSB-lataukset\n10A F16"]
    end

    subgraph FIELD["Kenttätaso (ei rele-ESP:llä)"]
        F1["AUTO_PL\nAutopilotti\n15A F13\n1-0-Auto"]
        F2["FRIDGE\nJääkaappi\n15A F21\n1-0-Auto"]
        F3["HEATER\nLämmitin\n15A F20\n1-0-Auto"]
        F4["BILGE_MID\nKeskipumppu\n15A F23\nKelluke"]
        F5["BILGE_LARGE\nIsopumppu\n20A F24\nKelluke"]
    end

    subgraph RE2["Rele-ESP 2 – Kenttä-I/O"]
        B1["BILGE_SMALL\nBilssipumppu\n10A F22\n+ DI kelluke"]
        BVAR["7 kanavaa\nvaralla"]
    end
```

---

## Projektin eteneminen

```mermaid
gantt
    title Salena AU – Vaiheistus
    dateFormat  YYYY-MM
    section Taso 1 – RPi
    OpenPlotter + SignalK käyttöön   :done,    rpi1, 2025-01, 2025-03
    NVMe + UPS käyttöön              :done,    rpi2, 2025-03, 2025-05
    Salonkinäyttö asennus            :active,  rpi3, 2026-04, 2026-06
    section Taso 2 – Automaatio
    Rele-ESP pilotointi              :active,  esp1, 2026-04, 2026-07
    Modbus I/O hankinta + testaus    :         esp2, 2026-06, 2026-09
    Mittaus-ESP hankinta + firmware  :         esp3, 2026-07, 2026-10
    section Taso 2 – Ohjelmisto
    ESPHome firmware (releet)        :         fw1,  2026-05, 2026-08
    Home Assistant käyttöliittymä    :         ha1,  2026-08, 2026-11
    section Taso 3 – Kuormat
    Sähkökeskuksen layout            :active,  el1,  2026-04, 2026-06
    Johdotus ja asennus              :         el2,  2026-06, 2026-09
    Pilssipumput + jääkaappi         :         el3,  2026-08, 2026-11
```

---

## Suunnitteluperiaatteet (tiivistelmä)

| Periaate | Kuvaus |
|:---|:---|
| 🔒 Manuaalinen fallback | Vene toimii täysin ilman automaatiota |
| 🌐 Ei pilviriippuvuutta | Järjestelmä toimii paikallisesti |
| 🔁 Kerroksellinen arkkitehtuuri | Navigointi, automaatio ja kuormat erotettu |
| 🔌 Ethernet ensisijaisena | Wi-Fi vain käyttöliittymille |
| 🔧 Huollettavuus | Selkeät kytkennät, sulakkeet, dokumentointi |
| 📈 Vaiheittainen laajennus | Lisäykset ilman uudelleensuunnittelua |

---

## Viitteet

- [Järjestelmäarkkitehtuuri](architecture.md)
- [Nykytila](current_state.md)
- [Suunnittelupäätökset](design_decisions.md)
- [Verkko ja väylät](network.md)
- [Hankinnat](procurement.md)
- [Relekartta](../hardware/relay_map.md)
- [Akut, laturit ja paneelit](../hardware/power-setup.md)
- [TODO](todo.md)
