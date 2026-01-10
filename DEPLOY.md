# Guide de déploiement rapide

## ✅ Problèmes résolus

1. ❌ **Erreur de build** : Correction de la sérialisation datetime
2. ❌ **Erreurs YAML** : Suppression des `**` dans les prompts
3. ✅ **Déploiement automatique** : GitHub Actions configuré
4. ✅ **Déploiement manuel** : Script `deploy.sh` disponible

## 🚀 Workflow de déploiement

### Automatique (recommandé)
```bash
git add .
git commit -m "Mon message"
git push origin main
```
→ GitHub Actions déploie automatiquement sur gh-pages

### Manuel
```bash
./deploy.sh
```

## 🔍 Vérifier le déploiement

1. **Actions GitHub** : https://github.com/phlered/amersfoort/actions
   - Vérifier que le workflow "Déployer sur GitHub Pages" réussit
   
2. **Site live** : https://phlered.github.io/amersfoort/
   - Attendre 1-2 minutes après le push
   
3. **Settings GitHub Pages** : 
   - Aller dans Settings → Pages
   - Source doit être : `gh-pages` branch
   - Le site doit être marqué comme "active"

## 🛠️ Tester localement avant de déployer

```bash
# Build le site
./site.sh build

# Servir localement
./site.sh serve
```

Puis ouvrir http://localhost:8000

## ⚠️ En cas de problème

Si le site ne se met pas à jour :

1. Vérifier que le build local fonctionne :
   ```bash
   ./site.sh build
   ```

2. Vérifier les logs GitHub Actions :
   - Onglet "Actions" sur GitHub
   - Cliquer sur le dernier workflow
   - Vérifier les erreurs éventuelles

3. Vérifier la configuration GitHub Pages :
   - Settings → Pages
   - Source : Deploy from branch
   - Branch : gh-pages / (root)

4. Forcer un nouveau build :
   ```bash
   git commit --allow-empty -m "Forcer rebuild"
   git push origin main
   ```
