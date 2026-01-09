#!/usr/bin/env python3
"""
Script pour générer le site web Amersfoort - Frans leren
Site dédié uniquement au français pour collégiens hollandais
Interface en néerlandais
"""

import os
import json
import re
import shutil
import unicodedata
from pathlib import Path
from datetime import datetime

# Configuration des chemins
SCRIPT_DIR = Path(__file__).parent
DOCS_DIR = SCRIPT_DIR / "docs"
SITE_DIR = SCRIPT_DIR / "site_langues"
RESOURCES_DIR = SITE_DIR / "resources"

# Pour Amersfoort : uniquement français
LANGUAGE_MAP = {"Français": "fr"}
LANGUAGE_NAMES = {"fr": "Frans"}

def slugify(value):
    """Normalise en ASCII sûr pour les URLs/dossiers (accents supprimés)."""
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^A-Za-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or "resource"

def extract_frontmatter(text_file):
    """Extrait les métadonnées du front matter YAML d'un fichier text.md"""
    with open(text_file, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        return None, None
    frontmatter_text = match.group(1)
    body = match.group(2)
    metadata = {}
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip()
    return metadata, body

def extract_text_and_vocab(body):
    """Extrait le texte et le vocabulaire depuis le corps du markdown"""
    text_match = re.search(r'##\s+(Texte|Text)\s*\n\n(.*?)(?=\n##|$)', body, re.DOTALL)
    text_content = text_match.group(2).strip() if text_match else ""
    vocab_match = re.search(r'##\s+(Vocabulaire|Vocabulary)\s*\n\n(.*?)$', body, re.DOTALL)
    vocab_content = vocab_match.group(2).strip() if vocab_match else ""
    return text_content, vocab_content

def scan_docs_directory():
    """Scanne le répertoire docs/ et génère les métadonnées - uniquement français"""
    resources = []
    for folder in DOCS_DIR.iterdir():
        if not folder.is_dir() or folder.name.startswith('.'):
            continue
        text_file = folder / "text.md"
        audio_file = folder / "audio.mp3"
        if not text_file.exists() or not audio_file.exists():
            print(f"⚠️  Incomplete map genegeerd: {folder.name}")
            continue
        metadata, body = extract_frontmatter(text_file)
        if not metadata:
            print(f"⚠️  Geen frontmatter in: {folder.name}")
            continue
        langue_full = metadata.get('langue', '')
        if langue_full != 'Français':
            continue
        text_content, vocab_content = extract_text_and_vocab(body)
        slug = slugify(folder.name)
        resource = {
            "id": slug,
            "langue": "fr",
            "prompt": metadata.get('prompt', ''),
            "resume": metadata.get('resume', metadata.get('prompt', '')),
            "niveau": metadata.get('niveau', ''),
            "classe": metadata.get('classe', ''),
            "axe": metadata.get('axe', ''),
            "genre": metadata.get('voix', metadata.get('genre', '')),
            "drapeau": metadata.get('drapeau', ''),
            "voix_variant": metadata.get('voix_variant', ''),
            "date": metadata.get('date_generation', ''),
            "longueur": int(metadata.get('longueur', 0)),
            "text_preview": text_content[:200] + "..." if len(text_content) > 200 else text_content,
            "vocab_count": len(re.findall(r'^\s*[-*]\s+\*\*', vocab_content, re.MULTILINE)),
            "audio_path": f"resources/{slug}/audio.mp3",
            "text_path": f"resources/{slug}/text.md",
            "titre_nl": metadata.get('titre_nl', ''),
            "mots_cles_nl": metadata.get('mots_cles_nl', '')
        }
        resources.append(resource)
        print(f"✅ {folder.name} -> {slug} - {resource['prompt'][:50]}")
    return resources

def copy_resources():
    """Copie les ressources (audio + text.md) vers site_langues/resources/"""
    if RESOURCES_DIR.exists():
        shutil.rmtree(RESOURCES_DIR)
    RESOURCES_DIR.mkdir(parents=True, exist_ok=True)
    for folder in DOCS_DIR.iterdir():
        if not folder.is_dir() or folder.name.startswith('.'):
            continue
        text_file = folder / "text.md"
        audio_file = folder / "audio.mp3"
        if not text_file.exists() or not audio_file.exists():
            continue
        metadata, _ = extract_frontmatter(text_file)
        if metadata and metadata.get('langue', '') == 'Français':
            slug = slugify(folder.name)
            dest_folder = RESOURCES_DIR / slug
            dest_folder.mkdir(parents=True, exist_ok=True)
            shutil.copy2(audio_file, dest_folder / "audio.mp3")
            shutil.copy2(text_file, dest_folder / "text.md")

def generate_metadata_json(resources):
    """Génère le fichier metadata.json"""
    metadata = {
        "generated_at": datetime.now().isoformat(),
        "total_resources": len(resources),
        "languages": ["fr"],
        "resources": resources
    }
    output_file = SITE_DIR / "metadata.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"\n✅ metadata.json gegenereerd met {len(resources)} bronnen")

def main():
    print("🔨 Amersfoort - Frans leren site genereren...")
    print(f"📂 Docs map: {DOCS_DIR}")
    print(f"📂 Site map: {SITE_DIR}\n")
    print("📖 Bronnen scannen (alleen Frans)...\n")
    resources = scan_docs_directory()
    if not resources:
        print("❌ Geen Franse bronnen gevonden!")
        return
    print(f"\n📋 {len(resources)} bronnen kopiëren...")
    copy_resources()
    print("\n📝 metadata.json genereren...")
    generate_metadata_json(resources)
    print("\n✨ Site met succes gegenereerd!")
    print(f"👉 Map: {SITE_DIR}")
    print(f"🇫🇷 {len(resources)} Franse luisteroefeningen beschikbaar")

if __name__ == "__main__":
    main()
