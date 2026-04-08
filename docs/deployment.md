# Deployment ja etäkehitys

**Dokumentti:** Salena AU Remote-SSH + Container Tools + Tailscale -kehitysympäristö  
**Päivitetty:** 04/2026  
**Tila:** Suunniteltu, toteutus vaiheittain

---

## Yhteenveto

Home Assistant -kontti hallinnoidaan VS Code:sta Remote-SSH-yhteyden yli Tailscale-VPN:n turvalla. Container Tools -laajennus tarjoaa graafisen käyttöliittymän Docker/Podman-hallintaan ilman SSH-komentoja.

---

## Arkkitehtuuri

```
Kehityskonesi (Windows/Mac/Linux)
  ├─ VS Code
  ├─ Remote - SSH laajennus
  └─ Container Tools laajennus
        ↓ Tailscale VPN (salattu, TCP/UDP)
        ↓
Raspberry Pi 5 (Salena-vene)
  ├─ Tailscale daemon
  ├─ SSH daemon
  └─ Docker/Podman
       └─ Home Assistant kontti (core-rpi5/docker-compose.yml)
```

---

## Edellytykset

### Kehitystaso
- VS Code (uusin versio)
- Remote - SSH laajennus (Microsoft)
- Container Tools laajennus (Microsoft)
- Tailscale asennettuna kehityskoneeseen

### RPi 5:n puoli
- Tailscale asennettuna ja aktiivisena
- SSH daemon käynnissä (oletus Raspbian:ssa)
- Docker tai Podman asennettuna

---

## Asennus (vaihe kerrallaan)

### 1. Tailscale RPi:lle

```bash
# SSH:n kautta Pi:hin
ssh pi@raspberrypi.local

# Tailscale asennus
curl -fsSL https://tailscale.com/install.sh | sh

# Activate (avaa linkkiä browser:issa)
sudo tailscale up

# Tarkista Tailscale IP (100.x.x.x)
tailscale ip -4
```

### 2. VS Code SSH-config

Lisää `~/.ssh/config`:

```
Host salena-rpi
    HostName 100.x.x.x
    User pi
    IdentityFile ~/.ssh/id_rsa
    StrictHostKeyChecking accept-new
```

VS Codessa: **Remote-SSH: Connect to Host** → `salena-rpi`

### 3. Container Tools käyttö

Kun olet kytketty Remote-SSH:lla:
1. Avaa VS Code File Explorer
2. Navigoi `core-rpi5/docker-compose.yml`
3. Oikeanklikkaa → **Docker: Compose Up**
4. Tarkastele logeja Output-paneelista

---

## docker-compose.yml (Home Assistant)

Sijainti: `core-rpi5/docker-compose.yml`

```yaml
version: '3.8'

services:
  home-assistant:
    image: homeassistant/home-assistant:latest
    container_name: salena-ha
    restart: unless-stopped

    # Veneen verkko: käytä host network -tilaa
    network_mode: host

    volumes:
      # HA konfiguraatiot
      - ./home-assistant:/config
      # Kellon synkkaus
      - /etc/localtime:/etc/localtime:ro

    environment:
      - TZ=Europe/Helsinki
      - PYTHONUNBUFFERED=1

    # Prosessorin rajoitus (pi5: 4 ydintä)
    deploy:
      resources:
        limits:
          cpus: '1.5'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M

  # Valinnainen: SignalK-integraation tuki (myöhemmin)
  # signalk:
  #   image: signalk/signalk:latest
  #   ...
```

**Huomio:** `network_mode: host` on kriittinen, koska HA tarvitsee pääsyn veneen sisäverkkoon (ESP32:t, MQTT, jne.)

---

## Kehitystyönkulku

### Päivittäin
1. Avaa VS Code
2. **Remote-SSH: Connect** → `salena-rpi` (automaattinen Tailscale-polku)
3. Avaa `core-rpi5/` kansiosta `docker-compose.yml`
4. Container Tools näkee HA konttin ja sen logit
5. Muokkaa `home-assistant/configuration.yaml` VS Code-editorissa
6. Päivitä: **Docker: Compose Restart** tai manuaalinen restart Container Tools UI:sta

### Konfiguraatiot
- `core-rpi5/home-assistant/configuration.yaml` – HA pääkonfiguraatio
- `core-rpi5/home-assistant/automations.yaml` – automaatiot
- `core-rpi5/home-assistant/scripts.yaml` – skriptit
- `core-rpi5/home-assistant/scenes.yaml` – näkymät

---

## Hyödyt

✅ **Etäkehitys:** Voit kehittää pitäen veneesi puolessa maailmassa  
✅ **Turvallinen:** Tailscale-VPN, ei portinavausta  
✅ **Graafinen:** Container Tools vs SSH-komennot  
✅ **Nopea:** Lokaalit logit ja konfiguraatio-editori samaan paikkaan  
✅ **Moderni:** Docker Compose On Demand

---

## Rajoitukset ja varotukset

⚠️ **Tailscale** vaatii internetyhteyden  
⚠️ **Host network** tarkoittaa, että HA näkee kaikki Pi:n portit (suunniteltu)  
⚠️ **SSH-avaimet** tulee hallita turvallisesti  
⚠️ **Muistin rajoitus** (Pi:llä 4GB): 512MB RAM HA-kontille riittää, mutta tight varauksilla  

---

## Seuraavat vaiheet

1. ✓ Tailscale asennus (alla)
2. ✓ SSH-config (alla)
3. ✓ Docker-compose pohja (alla)
4. ☐ Ensimmäinen HA startup ja testaus
5. ☐ SignalK-integraatio HA:han (integraatiot → HTTP REST)
6. ☐ MQTT-väylän integraatio (Mosquitto + HA)
7. ☐ ESP32-ohjainten integraatio HA:han (modbus-tcp tai MQTT)

---
