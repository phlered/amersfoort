# Snelstart - Amersfoort Frans Leren

## 🚀 In 3 stappen

### 1. Site bouwen

```bash
./site.sh build
```

### 2. Lokaal testen

```bash
./site.sh serve
```

Open in browser: **http://localhost:8000**

### 3. Nieuwe oefening maken

```bash
# Vanuit de parent map
cd ../comprehension_orale
.venv312/bin/python genmp3.py -l fr -p "Au marché" --niveau A2

# Terug naar amersfoort en site herbouwen
cd ../amersfoort
./site.sh build
```

## 📝 Commando's

| Commando | Actie |
|----------|-------|
| `./site.sh build` | Site genereren |
| `./site.sh serve` | Lokale server (poort 8000) |
| `./site.sh stats` | Aantal bronnen tonen |
| `./site.sh clean` | Tijdelijke bestanden wissen |

## 🎯 Website kenmerken

- **Automatische omleiding** naar Frans (geen taalkeuze)
- **Nederlandse interface** ("Zoeken", "Niveau", etc.)
- **36 Franse luisteroefeningen** (A1-C2)
- **Filtreren op niveau** (localStorage opgeslagen)
- **Responsive design** (mobiel + desktop)

## 📁 Belangrijke bestanden

- `build_site.py` - Genereert `site_langues/` uit `docs/`
- `index.html` - Redirect naar `search.html?lang=fr`
- `search.html` - Hoofdpagina met zoeken + filters
- `metadata.json` - Alle metadata (gegenereerd)
- `.gitignore` - Beschermt API keys

## 🔑 API Keys

**BELANGRIJK**: `.env` is uitgesloten van Git!

```bash
OPENAI_API_KEY=sk-...
AZURE_SPEECH_KEY=...
AZURE_SPEECH_REGION=westeurope
```

## ⚡ Tips

1. **Nieuwe ressource toevoegen**: Kopieer Franse `text.md` + `audio.mp3` naar `docs/`, run `./site.sh build`
2. **Niveau filter testen**: Kies niveau in browser, herlaad - filter blijft actief (localStorage)
3. **Design aanpassen**: Edit `styles.css` in `site_langues/`

## 🆘 Problemen?

- **Site leeg?** → Check `docs/` bevat Franse resources
- **Geen audio?** → Verifieer `audio.mp3` bestaat in dossiers
- **Build fout?** → Check Python 3 is geïnstalleerd

---

**Vraag?** Zie [README.md](README.md) voor details
