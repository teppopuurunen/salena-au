# Salena AU - Relekartta v5.0.0

## 1. Yleisasetukset
- **Laite:** ESP32-S3-ETH-8DI-8RO
- **Väylä:** Ethernet (RJ45)
- **Protokolla:** MQTT / REST
- **Syöttö:** PoE
- **Kuormajännite:** 12V DC

## 2. Moduuli 1: Navigointi ja IT (IP: 10.10.10.11)
| Ch | Tunnus | Kuorma | Sulake | Hallinta | Huomio |
|:---|:---|:---|:---|:---|:---|
| R1 | NAV_RUN | Kulkuvalot | 5A (F1) | 1-0-Auto | Sivu + perävalot |
| R2 | NAV_ANC | Ankkurivalo | 5A (F2) | 1-0-Auto | Maston huippu |
| R3 | NAV_MOT | Ajovalo | 7.5A (F3) | 1-0-Auto | Maston etuosa |
| R4 | NAV_COM | Kompassivalo | 2A (F4) | Rele | |
| R5 | NAV_IO | Mittaristo/NMEA | 5A (F11) | Rele | Elektroniikan syöttö |
| R6 | NET_IT | Reititin/Kytkin | 5A (F12) | Aina päällä| Huawei B818-263 + Teltonika TSW101 |
| R7 | CAM | Kamerat | 5A (F14) | Rele | Mastokamera (Tapo) |
| R8 | USB_PWR | USB-lataukset | 10A (F16)| Rele | Kabiinin latauspisteet|

## 3. Releiden ulkopuoliset kuormat (kenttätaso)

Seuraavat kuormat ovat rele-ESP:n ulkopuolella ja ohjataan kenttätasolla:

| Tunnus | Kuorma | Sulake | Hallinta | Tila | Peruste |
|:---|:---|:---|:---|:---|:---|
| AUTO_PL | Autopilotti (ST5000) | 15A (F13) | 1-0-Auto | Käytössä | >10A, ei rele-ESP:lle |
| FRIDGE | Jääkaappi (Danfoss) | 15A (F21) | 1-0-Auto | Hankkimatta | >10A, ei rele-ESP:lle |
| HEATER | Lämmitin (VEVOR 5kW) | 15A (F20) | 1-0-Auto | Hankkimatta | >10A, ei rele-ESP:lle |
| BILGE | Bilssipumppu | 15A (F22) | 1-0-Auto | Hankkimatta | >10A, ei rele-ESP:lle |

Peruste: rele-ESP:n käytettävä kuormitusraja on 10A.
