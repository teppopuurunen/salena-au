cat > docs/index.md <<'EOF'
# Dokumentaatioindeksi

Tämä hakemisto sisältää Salena AU -järjestelmän “current truth” -dokumentit.

## Yleisdokumentit (docs/)

- `architecture.md` – Järjestelmäarkkitehtuuri (kerrokset, vastuut, rajapinnat)
- `current_state.md` – Todellinen nykytila (mikä on käytössä nyt)
- `design_decisions.md` – Keskeiset suunnittelupäätökset (miksi näin)
- `network.md` – Verkko ja väylät (Ethernet/Wi-Fi/USB/RS422)
- `procurement.md` – Hankinnat ja varaukset
- `todo.md` – Seuraavat työvaiheet (testipenkki, layout, firmware)

## Laitteisto (hardware/)

- `../hardware/relay_map.md` – Relekartta / kanavointi
- `../hardware/hardware_spec.md` – Laitteistohuomiot (sisältää myös legacy-oletuksia)
EOF
