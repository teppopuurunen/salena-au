# Tekniset tiedot - Salena AU v5.0

## 1. Verkkotopologia (IPv4)
| Laite-ID | Laitteisto | IP-osoite | Protokolla |
| :--- | :--- | :--- | :--- |
| Core-Master | RPi 5 | 10.10.10.1 | SSH, HTTP, MQTT, SignalK |
| Node-Forward | WS-31130 | 10.10.10.11 | REST/MQTT |
| Node-Aft | WS-31130 | 10.10.10.12 | REST/MQTT |

## 2. Liitäntäkartta (Sarjaväylät/USB)
- **USB-portti 0:** Victron SmartSolar (VE.Direct)
- **USB-portti 1:** Raymarine ST5000 (RS422-muunnin)
- **USB-portti 2:** Tankki/Virta ESP32-S3 (Home ESP)

## 3. I/O-logiikkataulukko (Pääsolmut)
| Kanava | Toiminto | Nimelliskuorma | Sulake | Paikallinen ohitus |
| :--- | :--- | :--- | :--- | :--- |
| N1-R1 | Kulkuvalot | 1.2A | 5A (F1) | Mekaaninen (1-0-A) |
| N1-R2 | Ankkurivalo | 0.8A | 5A (F2) | Mekaaninen (1-0-A) |
| N2-R1 | Jääkaappi | 4.5A | 10A (F11) | Vain ohjelmistollinen |
| N2-R3 | Autopilotti syöttö | 3.0A | 15A (F13) | Vain ohjelmistollinen |

## 4. Toiminnalliset rajat
- **Syöttöjännite:** 9.0VDC - 16.0VDC
- **Maksimikuorma (Järjestelmä):** 12A (ilman vinssien/keulapotkurin kuormia)
- **Päivitystaajuus:** Signal K (10Hz), Akkuvalvonta (1Hz)
