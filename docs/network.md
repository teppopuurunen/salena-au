cat > docs/network.md <<'EOF'
# Verkko ja väylät

Tämä dokumentti kuvaa Salena AU -järjestelmän tiedonsiirron periaatteet ja rajaukset.

---

## Periaate

- Ethernet on ensisijainen väylä automaatiolle (ESP ↔ RPi)
- Wi-Fi on käyttöliittymille (tabletti/puhelin), ei kriittiselle ohjaukselle
- USB:llä hoidetaan mittaukset ja erikoisliitännät (esim. RS422)

---

## Yhteydet

### Ethernet
- ESP32-S3 relemoduulit ja mahdolliset muut ohjaimet
- Tavoite: deterministinen ja helposti debugattava liikenne

### Wi-Fi
- Käyttöliittymät (esim. selain/HA-näkymä)
- Ei oleteta toimivaksi ohjauspoluksi

### USB
- Anturi-/mittaus-ESP (USB sarja tai vastaava)
- Autopilotti (USB–RS422-adapteri)

---

## Home Assistant
- HA on ei-kriittinen käyttöliittymäkerros
- HA:n vika ei saa estää paikallista ohjausta tai perustoimintoja

---

## Rajaukset tässä vaiheessa
- Ei pilvipalveluriippuvuuksia
- Ei Wi-Fi-riippuvaista kuormaohjausta
- Autopilotti-integraatio ensin read-only
EOF
