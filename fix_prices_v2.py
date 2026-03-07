#!/usr/bin/env python3
"""
Script pour corriger les prix de déplacement dans les pages urgente
selon les zones officielles 2026 - VERSION CORRIGÉE
"""

import os
import re
from pathlib import Path

# Zones officielles 2026
ZONES = {
    # Zona 1 - 15€
    'macedo-de-cavaleiros': 15,
    'mirandela': 15,
    
    # Zona 2 - 25€
    'vila-flor': 25,
    'alfandega-da-fe': 25,
    'carrazeda-de-ansiaes': 25,
    
    # Zona 3 - 35€
    'braganca': 35,
    'vinhais': 35,
    'vimioso': 35,
    'torre-de-moncorvo': 35,
    'mogadouro': 35,
    'freixo-de-espada-a-cinta': 35,
    
    # Zona 4 - 45€
    'miranda-do-douro': 45,
    'vila-nova-de-foz-coa': 45,
    'sao-joao-da-pesqueira': 45,
    'murca': 45,
    'valpacos': 45,
    
    # Zona 5 - 55€
    'vila-real': 55,
    'alijo': 55,
    'sabrosa': 55,
    'tabuaco': 55,
    'armamar': 55,
    'peso-da-regua': 55,
    'lamego': 55,
    'santa-marta-de-penaguiao': 55,
    'mesao-frio': 55,
    
    # Zona 6 - 65€
    'chaves': 65,
    'vila-pouca-de-aguiar': 65,
    'boticas': 65,
    'montalegre': 65,
    'ribeira-de-pena': 65,
    'mondim-de-basto': 65,
    'moimenta-da-beira': 65,
    'sernancelhe': 65,
    'penedono': 65,
}

def extract_city_from_filename(filename):
    """Extrait le nom de la ville du nom de fichier"""
    city = filename.replace('-urgente.html', '')
    return city

def fix_price_in_file(filepath):
    """Corrige le prix dans un fichier HTML"""
    filename = os.path.basename(filepath)
    city = extract_city_from_filename(filename)
    
    if city not in ZONES:
        print(f"⚠️  {filename}: ville non trouvée dans les zones")
        return False
    
    correct_price = ZONES[city]
    
    # Lit le fichier
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern flexible pour trouver la ligne de prix (avec espaces/indentation)
    # Cherche: <td>Deslocação Urgente [texte]</td> suivi de <td>XX€</td>
    pattern = r'(<td>Deslocação Urgente[^<]+</td>\s*<td>)\d+€(</td>)'
    
    # Remplace le prix
    new_content = re.sub(pattern, rf'\g<1>{correct_price}€\g<2>', content)
    
    if content == new_content:
        print(f"✅ {filename}: déjà correct ({correct_price}€)")
        return False
    
    # Écrit le fichier
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ {filename}: corrigé → {correct_price}€")
    return True

def main():
    public_dir = Path('public')
    
    if not public_dir.exists():
        print("❌ Dossier public/ non trouvé")
        return
    
    files = list(public_dir.glob('*-urgente.html'))
    print(f"🔍 {len(files)} fichiers trouvés\n")
    
    fixed = 0
    for filepath in sorted(files):
        if fix_price_in_file(filepath):
            fixed += 1
    
    print(f"\n✅ {fixed} fichiers corrigés")

if __name__ == '__main__':
    main()
