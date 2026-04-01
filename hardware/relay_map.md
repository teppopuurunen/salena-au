# Salena AU - Relekartta v5.0.0

## 1. Yleisasetukset
- **Laite:** ESP32-S3-ETH-8DI-8RO
- **Väylä:** Ethernet (RJ45)
- **Protokolla:** MQTT / REST
- **Käyttöjännite:** 12V DC

## 2. Moduuli 1: Navigointi ja IT (IP: 10.10.10.11)
| Ch | Tunnus | Kuorma | Sulake | Hallinta | Huomio |
|:---|:---|:---|:---|:---|:---|
| R1 | NAV_RUN | Kulkuvalot | 5A (F1) | 1-0-Auto | Sivu + perävalot |
| R2 | NAV_ANC | Ankkurivalo | 5A (F2) | 1-0-Auto | Maston huippu |
| R3 | NAV_MOT | Ajovalo | 7.5A (F3) | 1-0-Auto | Maston etuosa |
| R4 | NAV_COM | Kompassivalo | 2A (F4) | Rele | |
| R5 | NAV_IO | Mittaristo/NMEA | 5A (F11) | Rele | Elektroniikan syöttö |
| R6 | NET_IT | Reititin/Kytkin | 5A (F12) | Aina päällä| 12V DC IT-laitteet |
| R7 | CAM | Kamerat | 5A (F14) | Rele | Mastokamera (Tapo) |
| R8 | USB_PWR | USB-lataukset | 10A (F16)| Rele | Kabiinin latauspisteet|

## 3. Moduuli 2: Tekniikka ja Mukavuus (IP: 10.10.10.12)
| Ch | Tunnus | Kuorma | Sulake | Hallinta | Huomio |
|:---|:---|:---|:---|:---|:---|
| R1 | AUTO_PL | Autopilotti | 15A (F13)| Rele | ST5000 pääsyöttö |
| R2 | MEDIA | Audio / Radio | 10A (F15)| Rele | |
| R3 | BATT_MON| Akkumonitori | 2A (F17) | Rele | |
| R4 | FRIDGE | Jääkaappi | 15A (F21)| Rele | Danfoss-kompressori |
| R5 | WTR_PUMP| Painevesipumppu| 10A (F18)| 1-0-Auto | |
| R6 | HEATER | Lämmitin | 15A (F20)| Rele | VEVOR 5kW Diesel |
| R7 | BILGE | Bilssipumppu | 15A (F22)| 1-0-Auto | Manuaaliohitus |
| R8 | SPARE | Varaus | - | - | |
