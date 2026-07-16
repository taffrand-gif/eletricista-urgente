#!/usr/bin/env python3
"""
Fix unique 404-confirmed: eletricista-urgente-cortiços.html
Source file has <link canonical href="...corticos"> (no cedilha) → prod 404.
Also og:url shares the same bad slug.
Fix both with cedilha to match source filename.
"""
from pathlib import Path
import re

target = Path("eletricista-urgente-cortiços.html")
old_canon = "https://eletricista-urgente.pt/eletricista-urgente-corticos"  # sans cedilha
new_canon = "https://eletricista-urgente.pt/eletricista-urgente-cortiços"  # avec cedilha (matches filename)

raw = target.read_bytes()
text = raw.decode("utf-8")

count = text.count(old_canon)
print(f"AVANT: '{old_canon}' trouvé {count}x dans {target.name}")
assert count >= 1, f"Attendu au moins 1, trouvé {count}"

new_text = text.replace(old_canon, new_canon)
new_bytes = new_text.encode("utf-8")

# Verify post-fix
RE_CANON = re.compile(
    r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']',
    re.IGNORECASE,
)
new_canons = RE_CANON.findall(new_text)
print(f"APRÈS: {len(new_canons)} <link canonical> trouvé(s)")
assert len(new_canons) == 1
assert new_canons[0] == new_canon, f"Mismatch: {new_canons[0]}"
print(f"  -> canonical: {new_canons[0]}")

# Verify og:url updated
RE_OG = re.compile(r'<meta[^>]+property=["\']og:url["\'][^>]+content=["\']([^"\']+)["\']', re.IGNORECASE)
og_urls = RE_OG.findall(new_text)
for og in og_urls:
    if "cortico" in og:
        assert og == new_canon, f"og:url pas synchro: {og}"
        print(f"  -> og:url: {og} (synchro ✓)")

# Diff bytes (string-level diff, length-normalized)
text_count = sum(1 for a, b in zip(text.split('\n'), new_text.split('\n')) if a != b)
diff_size = abs(len(new_text) - len(text))
print(f"DIFF chaîne: {len(new_text)} car après vs {len(text)} avant (delta {diff_size})")
assert diff_size <= 10, f"Trop de chars changés: {diff_size}"
# ECP check: same line count
assert len(text.split('\n')) == len(new_text.split('\n')), "Ligne count changed!"

if new_bytes == raw:
    print("NO-OP: bytes identiques, abandon")
else:
    target.write_bytes(new_bytes)
    print(f"✓ ÉCRIT: {target.name}")
