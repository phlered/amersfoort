#!/bin/bash

# site.sh - Gestion du site Amersfoort - Frans leren

case "$1" in
    build)
        echo "🔨 Site genereren..."
        python3 build_site.py
        ;;
    serve)
        echo "🌐 Lokale server starten op http://localhost:8000"
        echo "📂 Map: site_langues/"
        echo "⚠️  Druk op Ctrl+C om te stoppen"
        cd site_langues && python3 -m http.server 8000
        ;;
    stats)
        echo "📊 Statistieken Frans:"
        find docs -name "text.md" -exec grep -l "^langue: Français" {} \; | wc -l | xargs echo "  Totaal aantal bronnen:"
        ;;
    clean)
        echo "🧹 Opruimen van tijdelijke bestanden..."
        rm -f _temp_*
        echo "✅ Klaar"
        ;;
    *)
        echo "Gebruik: ./site.sh {build|serve|stats|clean}"
        echo ""
        echo "Commando's:"
        echo "  build  - Site genereren uit docs/"
        echo "  serve  - Lokale server starten (poort 8000)"
        echo "  stats  - Statistieken tonen"
        echo "  clean  - Tijdelijke bestanden verwijderen"
        exit 1
        ;;
esac
