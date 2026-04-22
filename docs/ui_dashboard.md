# Käyttöliittymä- ja Dashboard-arkkitehtuuri

**Dokumentti:** Salena AU UI/Dashboard-suunnitelma  
**Päivitetty:** 04/2026  
**Tila:** Suunniteltu, osittain toteutettu

---

## Yhteenveto

Salena AU -järjestelmän käyttöliittymä on suunniteltu tarjoamaan optimaalinen näkyvyys ja hallinta kaikissa tilanteissa – veneessä navigoidessa, sähköjärjestelmiä valvottaessa tai etähallinnassa.

---

## 1. Dashboard-strategia: Home Assistant "Master Dash"

Järjestelmän keskitettynä hallintaliittymänä toimii Home Assistant (HA), johon kaikki data ja ohjaukset integroidaan yhdeksi näkymäksi.

### Järjestelmäintegraatio

- **Signal K ↔ HA:** Kaikki navigointidata (nopeus, syvyys, tuuli, GPS) tuodaan Signal K:sta HA-entiteeteiksi.
- **ESP32-automaatio:** Releohjaukset (12V kuormat) ja tilatiedot (rele-ESP:t) ohjataan suoraan HA:n kautta.
- **Energiaseuranta:** INA228- ja INA3221-mittausten data visualisoidaan sähköjärjestelmän dashboardille.

### Käyttötilat (Dashboard Views)

#### Purjehdusnäkymä (Sailing Mode)
- Painopiste reaaliaikaisessa datassa: isot numeronäytöt syvyydelle ja tuulelle
- Upotettu karttanäkymä (Signal K Freeboard-SK iFrame)
- Kriittiset navigointihälytykset

#### Sähkö- ja järjestelmänäkymä (System Mode)
- Akun tila, latausvirta (INA228) ja kulutus
- Releiden ohjauskytkimet ja 1-0-Auto-tilatiedot
- Pilssipumppujen ja muiden apulaitteiden valvonta

#### Satama- ja mukavuusnäkymä
- Valaistuksen ohjaus, sääennusteet ja säiliöiden täyttöasteet

---

## 2. Laitekohtaiset toteutukset

| Laite | Käyttötapa | Erityispiirteet |
|-------|-----------|-----------------|
| Samsung Tab S6 Lite | Kiinteä komentokeskus veneessä | Fully Kiosk Browser, kiosk mode, optimoitu ulkoiselle hiirelle |
| Älypuhelin | Nopeat tarkistukset laiturilta tai kannelta | Responsiivinen "Quick Check" -näkymä |
| Läppäri | Järjestelmäasetukset, koodaus, OpenCPN | Täysi työpöytänäkymä |

### Tabletti (Kiosk Mode)
- **Fully Kiosk Browser** lukitsee näytön HA-dashboardiin
- Estää muiden sovellusten häiriöt
- Optimoitu tarkkaa hallintaa varten ulkoisella hiirellä

---

## 3. Android-sovellus (suunnitteilla)

Autopilotti- ja sähköohjausta varten on suunnitteilla erillinen Android-natiivisovellus, joka toimii **vain paikallisverkossa** (ei vaadi internetyhteyttä tai VPN:ää).

- **Kohdealustat:** Samsung Galaxy -älypuhelin ja Samsung Galaxy Watch (Wear OS)
- **Käyttötarkoitus:** Autopilotin ohjaus ja 12V-sähkölaitteiden nopea hallinta kannelta tai laiturilta
- **Yhteys:** Paikallisverkko suoraan (RPi5-IP tai mDNS), ei Tailscale-riippuvuutta
- **Status:** Projekti avattu Android Studiossa, kehitys käynnissä

### Arkkitehtuuriperiaatteet
- Kommunikointi Home Assistantin REST API:n tai WebSocketin kautta
- Wear OS -sovellus näyttää kriittiset tilatiedot ja antaa pikakomennot ranteesta
- Offline-first: toimii veneen sisäverkossa vaikka internet ei toimisi

---

## 4. Etäyhteystekniikat

Dashboardien saumaton käyttö laitteesta ja sijainnista riippumatta perustuu seuraaviin tekniikoihin:

| Teknologia | Käyttötarkoitus |
|-----------|----------------|
| **Tailscale (VPN)** | Suojattu mesh-verkko laitteiden välille; suora pääsy dashboardille (`100.x.x.x:8123`) ilman porttiavausta |
| **RustDesk** | Työpöytätason etähallinta (Windows/RPi5); suora IP-yhteys ja virtuaalinäyttö yksityisyyden varmistamiseksi |
| **WayVNC** | Varayhteys Raspberry Pi:n työpöydän suoraan hallintaan |

---

## Katso myös

- [deployment.md](deployment.md) – Remote-SSH + Tailscale -etäkehitysympäristö
- [architecture.md](architecture.md) – Järjestelmäarkkitehtuuri kokonaisuudessaan
- [network.md](network.md) – Verkko ja väylät
