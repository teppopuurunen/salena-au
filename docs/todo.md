# TODO

**Tavoite:** Edetä vaiheittain siten, että jokainen askel tuottaa testattavan “valmiin palan” eikä lisää kriittisiä riippuvuuksia.  
**Periaate:** Ensin mitat ja testipenkki, sitten yksi toimiva ohjausketju (painike → rele → kuorma), vasta sen jälkeen laajennukset.

---

## 0) Kehitysympäristö: Tailscale + VS Code Remote-SSH + Container Tools

Yleiset ohjeet: [docs/deployment.md](deployment.md)

- [ ] Asenna Tailscale kehityskoneeseen ja RPi 5:lle
  - [ ] Varmista Tailscale-linkit aktiivisina (100.x.x.x adressi)
- [ ] Asenna VS Code laajennukset:
  - [ ] Remote - SSH (Microsoft)
  - [ ] Container Tools (Microsoft)
- [ ] Konfiguroi SSH config (~/.ssh/config):
  ```
  Host salena-rpi
      HostName 100.x.x.x
      User pi
      IdentityFile ~/.ssh/id_rsa
  ```
- [ ] Testaa yhteys: **Remote-SSH: Connect** → `salena-rpi`
- [ ] Tarkista että Docker/Podman on käynnissä RPi:llä
  - [ ] Testaa: `docker ps` (SSH terminaalissa)

- [ ] Ota sähkökeskuksen mitat layouttia varten:
  - [ ] kaapin sisämitat (leveys/korkeus/syvyys)
  - [ ] DIN-kiskojen pituudet ja sijainnit
  - [ ] läpivientien sijainnit ja halkaisijat
  - [ ] kiinnityspisteet / ruuvijaot / “ei saa porata” -alueet
  - [ ] johtokourujen reitit ja maksimikoot
- [ ] Kirjaa sijoitteluperiaatteet:
  - [ ] pääsyötöt ja suuret virrat erilleen signaaleista
  - [ ] huoltovarat ja kaapelilenkit liittimille
  - [ ] moduulijako (RPi / ESP / sulakkeet / kytkimet)
- [ ] Tee karkea 2D-layout luonnos mittojen pohjalta

---

## 2) Autopilotti testipenkkiin (read-only ensin)

- [ ] Pura Raymarine ST5000 testipenkkiin:
  - [ ] dokumentoi johdot ja liittimet (kuvat + nimeäminen)
  - [ ] kirjaa virtasyöttövaatimukset ja sulakekoko
- [ ] Rakenna testipenkki:
  - [ ] 12 V virtalähde (11–14.5 V)
  - [ ] sulake testipenkkiin
- [ ] USB–RS422-adapteri kiinni Raspberry Pi:hin:
  - [ ] varmista että adapteri näkyy (tty-laite)
  - [ ] kaappaa raakadata 5–10 min ja tallenna `docs/autopilot/` alle

---

## 3) Rele-ESP pilotointi (minimi)

- [ ] Valitse yksi rele-ESP pilotiksi
- [ ] Kytke 1 painike inputtiin ja 1 rele ulostuloon (testikuorma)
- [ ] Luo ESPHome runkotiedostot releohjaimille:
  - [ ] `core-rpi5/home-assistant/esphome/rele-esp-1.yaml`
  - [ ] `core-rpi5/home-assistant/esphome/rele-esp-2.yaml`
- [ ] Toteuta minimifirmware:
  - [ ] painike togglaa relettä paikallisesti
  - [ ] boottaa turvalliseen tilaan
  - [ ] Ethernet ylös (mutta ei pakollinen toimintaan)
  - [ ] tilatieto sarjaporttiin
- [ ] Tee yksinkertainen statusrajapinta (valitse yksi):
  - [ ] HTTP `/status` JSON
  - [ ] UDP broadcast
  - [ ] MQTT (vain jos broker on jo päätetty)
- [ ] Pilssipumppu (DD-17) minimitoteutus:
  - [ ] Kytke BILGE_SMALL rele-ESP 2:n relekanavaan
  - [ ] Kytke BILGE_SMALL kellukekytkin rele-ESP 2:n DI-tuloon
  - [ ] Varmista, etta BILGE_MID ja BILGE_LARGE ovat vain sahkomekaanisia (kelluke + sulake)

---

## 4) Relekartta ja sulakekartta (ennen pysyvää johdotusta)

- [ ] Päätä ensimmäisen vaiheen kuormat, jotka menevät releiden taakse
- [ ] Laadi taulukko:
  - [ ] kanava → kuorma
  - [ ] arvioitu virta
  - [ ] sulakekoko
  - [ ] johdinpoikkipinta (arvio)
  - [ ] manuaaliohitus kyllä/ei
- [ ] Linkitä kartta layoutiin

---

## 5) Mittaus-ESP (kun relepilotointi on valmis)

- [ ] Päätä minimimittauspaketti:
  - [ ] 1 tankki
  - [ ] 1 akkujännite
  - [ ] 1 virta (päävirta tai kuormavirta)
- [ ] Luo ESPHome runkotiedosto mittausohjaimelle:
  - [ ] `core-rpi5/home-assistant/esphome/mittaus-esp.yaml`
- [ ] Toteuta firmware ja Ethernet/PoE-datan ulostulo
- [ ] Dokumentoi kalibrointi ja rajat
- [ ] Pilssipumppujen virta- ja tilakalibrointi (DD-17):
  - [ ] Luo hakemisto `docs/calibration/`
  - [ ] Luo tiedostot `bilge_pump1.md`, `bilge_pump2.md`, `bilge_pump3.md`
  - [ ] Kirjaa jokaiselle pumpulle: normivirta, kuivakayntivirta, kaynnistyspiikki, kellukkeen DI-taso
  - [ ] Maarita pumppukohtaiset halytysrajat kalibrointidatan perusteella

---

## 6) Home Assistant kehitys (Container Tools + Remote-SSH)

- [ ] Käynnistä HA kontti:
  - [ ] Avaa VS Code, kytkeytyminen `salena-rpi` (Remote-SSH)
  - [ ] Avaa `core-rpi5/docker-compose.yml`
  - [ ] Container Tools: Oikeanklikkaa yaml → **Compose Up**
  - [ ] Tarkista logit (Output panel)
- [ ] Asetus HA-konfiguraation pohjat (ensikerran):
  - [ ] Lisää `core-rpi5/home-assistant/configuration.yaml`
  - [ ] Lisää integraatiot tarpeen mukaan
- [ ] Lisää 3–5 ensimmäistä entiteettiä:
  - [ ] Releet (ESPHome + MQTT topicit)
  - [ ] Mittaukset (Mittaus-ESP, ESPHome + MQTT)
  - [ ] Autopilotti tila (read-only)
- [ ] Ota MQTT käyttöön HA:ssa (Mosquitto-integraatio)
- [ ] Pilssihalytykset (valvova, ei ohjaava):
  - [ ] Halytys jos pumppu kay > X min
  - [ ] Halytys jos pumppu kay > N kertaa / 24h
  - [ ] Varmista: automaatio ei koskaan katkaise pilssipumpun virtaa
- [ ] Tee yksi yksinkertainen dashboard (tablet-käyttöä varten)

---

## 7) Valaistus (myöhemmin)

- [ ] Päätä kanavamäärät ja ryhmät
- [ ] Pilotoi 1 ohjain (paikallinen käyttö)
- [ ] Testaa PWM-taajuudet ja mahdolliset häiriöt
- [ ] Lisää integraatio vasta lopuksi
