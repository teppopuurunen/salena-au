# Salena AU - Verkkosuunnitelma

Tämä asiakirja määrittelee S/Y Salenan lähiverkon rakenteen ja IP-osoitejaon.

## Laitteisto
* **Reititin:** Huawei B818-263 (LTE Cat19)
* **Sisäverkon IP-alue:** 192.168.1.0/24
* **Hallintaliittymä:** http://192.168.1.1

## IP-osoitteet (DHCP Varaukset)
| Laite | IP-osoite | Protokolla | Kuvaus |
| :--- | :--- | :--- | :--- |
| **Huawei B818** | 192.168.1.1 | HTTP | Reititin/Yhdyskäytävä |
| **Salena-RPi5** | 192.168.1.100 | MQTT/HTTP | Home Assistant & Mosquitto |
| **Rele 1 (Waveshare)** | 192.168.1.110 | MQTT | 8-kanavainen rele (Tulossa) |
| **Rele 2 (Waveshare)** | 192.168.1.111 | MQTT | 8-kanavainen rele (Tulossa) |
| **Akku-ESP** | 192.168.1.120 | MQTT | Akuston jännite ja virta |
| **Tankki-ESP** | 192.168.1.121 | MQTT | Polttoaine- ja vesitasot |

## MAC-osoitteet
* **Salena-RPi5 (eth0):** 2c:cf:67:da:17:16
