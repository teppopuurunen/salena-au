cat > docs/todo.md <<'EOF'
# TODO

**Tavoite:** Edetä vaiheittain siten, että jokainen askel tuottaa testattavan “valmiin palan” eikä lisää kriittisiä riippuvuuksia.  
**Periaate:** Ensin mitat ja testipenkki, sitten yksi toimiva ohjausketju (painike → rele → kuorma), vasta sen jälkeen laajennukset.

---

## 1) Mittaukset ja mekaaninen layout

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
- [ ] Toteuta minimifirmware:
  - [ ] painike togglaa relettä paikallisesti
  - [ ] boottaa turvalliseen tilaan
  - [ ] Ethernet ylös (mutta ei pakollinen toimintaan)
  - [ ] tilatieto sarjaporttiin
- [ ] Tee yksinkertainen statusrajapinta (valitse yksi):
  - [ ] HTTP `/status` JSON
  - [ ] UDP broadcast
  - [ ] MQTT (vain jos broker on jo päätetty)

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

## 5) Anturi-ESP (kun relepilotointi on valmis)

- [ ] Päätä minimimittauspaketti:
  - [ ] 1 tankki
  - [ ] 1 akkujännite
  - [ ] 1 virta (päävirta tai kuormavirta)
- [ ] Toteuta firmware ja USB-datan ulostulo
- [ ] Dokumentoi kalibrointi ja rajat

---

## 6) Home Assistant käyttöliittymäksi (ei-kriittinen)

- [ ] Käynnistä HA konttina
- [ ] Lisää 3–5 ensimmäistä entiteettiä (releet + mittaus)
- [ ] Tee yksi selkeä dashboard (veneessä käytettävä)

---

## 7) Valaistus (myöhemmin)

- [ ] Päätä kanavamäärät ja ryhmät
- [ ] Pilotoi 1 ohjain (ESP + paikallinen käyttö)
- [ ] Testaa PWM-taajuudet ja mahdolliset häiriöt
- [ ] Lisää integraatio vasta lopuksi
EOF
