# Amersfoort - Frans leren 🇫🇷

Site web dédié aux **collégiens hollandais** pour l'apprentissage du **français** à travers des ressources audio générées par IA.

## Vue d'ensemble

- **Public cible** : Collégiens néerlandophones
- **Langue enseignée** : Français uniquement
- **Interface** : En néerlandais
- **Technologie** : Textes GPT + Audio Azure TTS
- **Niveaux** : A1 à C2

## Structure du projet

```
amersfoort/
├── docs/                    # 44 ressources françaises copiées
│   └── [slug]_[date]/
│       ├── text.md          # Texte + frontmatter + vocabulaire
│       └── audio.mp3        # Synthèse vocale Azure
├── site_langues/            # Site web généré
│   ├── index.html           # Redirection vers français
│   ├── search.html          # Interface de recherche (NL)
│   ├── metadata.json        # Métadonnées des ressources
│   └── resources/           # Copies des audio/text
├── build_site.py            # Générateur de site (filtre français)
├── genmp3.py                # Générateur de ressources
├── md2mp3.py                # Convertisseur MD → MP3
├── site.sh                  # Utilitaire de gestion
└── .gitignore               # Protection clés API
```

## Utilisation

### Générer le site

```bash
./site.sh build
```

### Serveur local

```bash
./site.sh serve
# Ouvrir http://localhost:8000
```

### Créer une nouvelle ressource

```bash
# Utiliser l'environnement Python du projet parent
../../.venv312/bin/python genmp3.py -l fr -p "Acheter du pain" --niveau A1
./site.sh build  # Régénérer le site
```

### Statistiques

```bash
./site.sh stats
```

## Différences avec comprehension_orale

| Aspect | comprehension_orale | amersfoort |
|--------|---------------------|------------|
| Langues | 7 langues | Français uniquement |
| Interface | Français | Néerlandais |
| Page d'accueil | Choix de langue | Redirection auto vers FR |
| Public | Général | Collégiens NL |
| Filtres | Langue + Niveau | Niveau seulement |

## Fichiers clés

- **build_site.py** : Filtre `langue == "Français"` uniquement
- **index.html** : Redirection `<meta refresh>` vers `search.html?lang=fr`
- **search.html** : Textes en NL ("Zoeken", "Niveau", "Alle niveaus")
- **.gitignore** : Protège `.env` (clés Azure/OpenAI)

## Configuration

Copier le `.env` depuis le projet parent :

```bash
OPENAI_API_KEY=sk-...
AZURE_SPEECH_KEY=...
AZURE_SPEECH_REGION=westeurope
```

## Déploiement

### Déploiement automatique (recommandé)

Le site se déploie automatiquement sur GitHub Pages à chaque push sur `main` grâce à GitHub Actions :

1. **Build** : Le workflow compile le site depuis `docs/`
2. **Deploy** : Le contenu de `site_langues/` est publié sur la branche `gh-pages`
3. **Live** : Disponible sur https://phlered.github.io/amersfoort/

**Configuration** : 
- Le workflow est dans [.github/workflows/deploy.yml](.github/workflows/deploy.yml)
- GitHub Pages doit être activé dans Settings → Pages → Source : `gh-pages` branch

### Déploiement manuel

Si besoin de déployer manuellement :

```bash
./deploy.sh
```

Ce script :
1. Build le site avec `./site.sh build`
2. Commit les changements sur `main`
3. Copie `site_langues/` vers la branche `gh-pages`
4. Push sur GitHub

### Résolution de problèmes

Si le site ne se met pas à jour :
- ✅ Vérifier que le build réussit : `./site.sh build`
- ✅ Vérifier les workflows GitHub Actions (onglet Actions)
- ✅ S'assurer que GitHub Pages est activé dans Settings
- ✅ Attendre 1-2 minutes pour la propagation

## Notes techniques

- **36 ressources françaises** actuellement (44 copiées, 8 incomplètes ignorées)
- **Voix Azure** : Variété de voix neurales françaises
- **Vocabulaire** : Extraction automatique avec traductions
- **Niveaux CECRL** : A1, A2, B1, B2, C1, C2

## Développement

Le projet est **indépendant** de `comprehension_orale` mais partage :
- Les mêmes scripts de génération (`genmp3.py`, `md2mp3.py`)
- Le même environnement Python (`.venv312/`)
- Les mêmes clés API (`.env`)

---

**Créé le** : 7 janvier 2026  
**Ressources françaises** : 36/44 actives
