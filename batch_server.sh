#!/bin/bash

# Lancement du serveur batch UI
# Usage: ./batch_server.sh [--port 5000] [--debug]

set -e

# Choisir le binaire Python (python3 en priorité)
PYTHON_BIN="${PYTHON_BIN:-$(command -v python3 || true)}"
if [ -z "$PYTHON_BIN" ]; then
    PYTHON_BIN="${PYTHON_BIN:-$(command -v python || true)}"
fi

if [ -z "$PYTHON_BIN" ]; then
    echo "❌ Aucun interpréteur Python trouvé (python3 ou python)"
    echo "👉 Installez Python puis relancez le script"
    exit 1
fi

# S'assurer que pip est disponible pour cet interpréteur
if ! "$PYTHON_BIN" -m pip --version >/dev/null 2>&1; then
    echo "❌ pip n'est pas disponible pour $PYTHON_BIN"
    echo "📦 Tentative d'initialisation de pip..."
    if ! "$PYTHON_BIN" -m ensurepip --upgrade >/dev/null 2>&1; then
        echo "❌ Impossible d'initialiser pip. Installez pip puis relancez."
        exit 1
    fi
fi

# Déterminer le répertoire du script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Vérifier que Flask est installé
if ! "$PYTHON_BIN" -c "import flask" 2>/dev/null; then
    echo "❌ Flask n'est pas installé"
    echo "📦 Installation de Flask..."
    "$PYTHON_BIN" -m pip install --user flask
fi

# Récupérer les arguments
PORT="${PORT:-5000}"
DEBUG="${DEBUG:-false}"

for arg in "$@"; do
    case $arg in
        --port)
            PORT="$2"
            shift 2
            ;;
        --debug)
            DEBUG="true"
            shift
            ;;
        --help)
            echo "Usage: ./batch_server.sh [options]"
            echo ""
            echo "Options:"
            echo "  --port PORT      Port du serveur (défaut: 5000)"
            echo "  --debug          Mode debug (rechargement automatique)"
            echo "  --help           Afficher cette aide"
            echo ""
            echo "Exemples:"
            echo "  ./batch_server.sh"
            echo "  ./batch_server.sh --port 8080"
            echo "  ./batch_server.sh --port 3000 --debug"
            exit 0
            ;;
    esac
done

# Lancer le serveur
echo "🚀 Démarrage du serveur batch UI sur le port $PORT..."
echo ""
echo "📌 Ouvrez http://localhost:$PORT dans votre navigateur"
echo ""

if [ "$DEBUG" = "true" ]; then
    DEBUG_FLAG="--debug"
else
    DEBUG_FLAG=""
fi

"$PYTHON_BIN" batch_server.py --port "$PORT" $DEBUG_FLAG
