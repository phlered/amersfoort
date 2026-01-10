#!/bin/bash

# deploy.sh - Déployer le site Amersfoort vers GitHub Pages

set -e  # Arrêter en cas d'erreur

echo "🚀 Déploiement vers GitHub Pages..."

# 1. Build le site
echo "📦 1/4 - Build du site..."
./site.sh build

# 2. Commit les changements sur main
echo "💾 2/4 - Commit des changements..."
git add .
if git diff --staged --quiet; then
    echo "   Aucun changement à commiter"
else
    git commit -m "🔧 Mise à jour du site - $(date '+%Y-%m-%d %H:%M')"
    git push origin main
    echo "   ✅ Changements poussés sur main"
fi

# 3. Pousser site_langues vers gh-pages
echo "📤 3/4 - Déploiement sur gh-pages..."
TEMP_DIR=$(mktemp -d)
cp -r site_langues/* "$TEMP_DIR/"

git checkout gh-pages
git pull origin gh-pages --rebase || true

# Copier le contenu du dossier temporaire à la racine de gh-pages
# en préservant les fichiers existants non présents dans site_langues
cp -r "$TEMP_DIR"/* .
rm -rf "$TEMP_DIR"

git add .
if git diff --staged --quiet; then
    echo "   Aucun changement sur gh-pages"
else
    git commit -m "📱 Déploiement site - $(date '+%Y-%m-%d %H:%M')"
    git push origin gh-pages
    echo "   ✅ Site déployé sur gh-pages"
fi

# 4. Retour sur main
echo "🔄 4/4 - Retour sur main..."
git checkout main

echo ""
echo "✨ Déploiement terminé !"
echo "🌐 Le site sera disponible sur : https://phlered.github.io/amersfoort/"
echo ""
