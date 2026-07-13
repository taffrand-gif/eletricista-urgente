#!/usr/bin/env node
/**
 * Idempotent .md normalisation for eletricista-urgente blog
 *
 * Doctrine source-of-truth:
 *   ~/.claude/skills/norte-prices/SKILL.md (70 €/h élec, Z1 15€ → Z6 65€, +50% nuit/WE/feriado)
 *   AGENTS.md §11 (zéro invention), §12 (Transparence Radicale), §13 (gabarit élec)
 *
 * Rules: ce script N'INVENTE rien. Il nettoie les violations identifiées.
 * Les articles qui restent non-conformes après passage sont loggés pour réécriture manuelle.
 *
 * Usage:
 *   node scripts/normalize-blog-md.js --dry-run   # log + counts only, no write
 *   node scripts/normalize-blog-md.js             # write + render
 */

const fs = require('fs');
const path = require('path');
const { auditConformity } = require('./render-blog-md.js');

const BLOG_DIR = path.join(__dirname, '..', 'blog');
const DRY_RUN = process.argv.includes('--dry-run');

// 7 .md to JETER (hors-scope : plomberie/clima/regadio)
const TO_DELETE = new Set([
  'canalizador-braganca-guia-completo.md',
  'canalizador-macedo-cavaleiros-sede-operacional.md',
  'canalizador-mirandela-solucoes-locais.md',
  'casa-passiva-construir.md',
  'ventilacao-mecanica-vmc.md',
  'ventilacao-natural-casa.md',
  'sistema-rega-automatico.md',
]);

// === Règles de nettoyage (idempotentes) ===

// 1. Suppression des sections de témoignages / exemples inventés
function stripTestemunhosSections(md) {
  // H2/H3 de témoignages + tout le contenu jusqu'au prochain H2
  const sections = [
    // Titre principal ou suffixe parenthésé : Testemunhos, Casos reais, Exemplos reais, Dados de X+ intervenções, Com base na nossa experiência
    /^#{2,4}\s+[^\n]*\b(?:Testemunhos?|Casos (?:reais?|de (?:sucesso|clientes?|verdadeiros?))|Exemplos? (?:reais?|de (?:trabalhos?|interven[çc][õo]es?|pre[çc]os?|servi[çc]os?|or[çc]amentos?))|Hist[óo]rias? (?:de clientes?|reais?)|O que dizem os (?:nossos? )?clientes?|Dados de\s+\d+\+?\s*interven[çc][õo]es?|Com base na nossa experi[êe]ncia)\b[^\n]*$/gim,
    // Citation inventée en H3 : "### Maria S., Bragança" / "### João Silva, Porto" / "### António Costa"
    /^###\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]+(?:\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ]?[a-záéíóúâêôãõç]+|\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ]\.)*\.?,?\s*[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]+(?:\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]+)*\.?\s*$/gim,
  ];
  for (const re of sections) {
    md = md.replace(re, '## [Secção removida — testemunhos/exemplos inventados proibidos por R11]');
  }
  // Suppression des citations inventées ("Maria S. disse:", "O Sr. João confirmou:")
  md = md.replace(/^\s*["""][^"""]+["""]\s*[-—–]\s*[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]+(?:\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]+)*\.?\s*$/gm, '');
  // Phrases d'autorité "X+ intervenções", "Com base na nossa experiência"
  md = md.replace(/\bCom base na nossa experi[êe]ncia de \d+\+?\s*interven[çc][õo]es?[^.\n]*\.?/gi, '');
  md = md.replace(/\bDados de \d+\+?\s*interven[çc][õo]es?\b/gi, '');
  return md;
}

// 2. Suppression des marques commerciales
function stripMarcas(md) {
  const brands = [
    'Schneider Electric', 'Schneider', 'Legrand', 'ABB', 'Hager',
    'Bticino', 'BTicino', 'Chint', 'Siemens', 'Eaton', 'Finder',
    'Finderrelay', 'Finderrelés',
  ];
  for (const brand of brands) {
    const re = new RegExp(`\\b${brand.replace(/\./g, '\\.')}\\b[\\s,.;:()]*`, 'g');
    md = md.replace(re, '');
  }
  return md;
}

// 3. Suppression des stats non sourcées
function stripStatsNonSourcees(md) {
  const patterns = [
    /\b\d+(?:[.,]\d+)?\s*%\s+(?:dos|das|de)\s+casos\b/gi,
    /\b(?:casos|problemas)\s+que\s+(?:vemos|resolvemos)\b/gi,
    /\b\d+\+?\s+anos?\s+de\s+experi[êe]ncia\b/gi,
    /\bmais\s+de\s+\d+\s+anos?\b/gi,
    /\b\d+\s+anos?\s+de\s+experi[êe]ncia\b/gi,
    /\b\d+%\s+(?:problemas?|casos?|clientes?|interven[çc][õo]es?|avarias?)\s+(?:resolvidos?|resolvidas?|satisfeitos?|satisfeitas?|resolvem)\b/gi,
  ];
  for (const re of patterns) md = md.replace(re, '');
  return md;
}

// 4. Suppression des références à documentation émise
function stripDocsEmis(md) {
  const patterns = [
    /\b(?:emit(?:imos?|imos?|ir|ido|e)|fazemos|emit[êe]mos|fizer(?:am|emos))\s+[^.\n]{0,80}(?:certifica[çc][ãa]o|ficha(?:s)? eletrot[ée]cnic(?:a|as)|relat[óo]rio(?:s)? t[ée]cnic(?:o|os)|certificado)\b[^.\n]*/gi,
    /\bfichas?\s+eletrot[ée]cnic(?:a|as)\b/gi,
    /\brelat[óo]rio(?:s)?\s+t[ée]cnic(?:o|os)?\b/gi,
    /\binstala[çc][õo]es?\s+certificadas\b/gi,
    /\bcertifica[çc][ãa]o\s+completa\b/gi,
    /\bcertificado\s+em\s+\d{4}\b/gi,
  ];
  for (const re of patterns) md = md.replace(re, '');
  return md;
}

// 5. Suppression statuts DGEG
function stripDGEG(md) {
  const patterns = [
    /\bDGEG\b/g,
    /\bregisto\s+em\s+curso\b/gi,
    /\baguardando\s+registo\b/gi,
    /\b1757\/2026\/DIEN\b/g,
    /\b(?:em|em\s+processo\s+de)\s+inscri[çc][ãa]o\s+(?:na|na\s+DGEG|na\s+entidade)\b/gi,
  ];
  for (const re of patterns) md = md.replace(re, '');
  return md;
}

// 6. NAP faux → vrai
function fixNAP(md) {
  // 928484451 = canal (plomberie) → interdit
  md = md.replace(/\+?351\s*928\s*484\s*451/g, '+351 932 321 892');
  md = md.replace(/\b928\s*484\s*451\b/g, '+351 932 321 892');
  // 928 seul (avec contexte téléphone)
  md = md.replace(/\b928\s+321\s+892\b/g, '+351 932 321 892');
  // wa.me/351928321892 (canal) → wa.me/351932321892 (élec)
  md = md.replace(/wa\.me\/351928321892/g, 'wa.me/351932321892');
  return md;
}

// 7. Délais chiffrés → formulations honnêtes (sans promesse)
function stripDelaisChiffres(md) {
  // "em X minutos" / "em X horas" / "chegamos em" / "tempo médio de resposta"
  const patterns = [
    /\b(?:resposta|chegada|chegar|t[ée]cnic[oa]|demoram?)[^.\n]{0,45}\b\d+(?:[.,]\d+)?\s*(?:min(?:uto)?s?|h(?:oras?)?)\b/gi,
    /\batendimento[^.\n]{0,45}\b\d+(?:[.,]\d+)?\s*(?:min(?:uto)?s?|horas?)\b/gi,
    /\btempo\s+m[ée]dio\s+de\s+resposta[^.\n]{0,30}\d+/gi,
    /\bchegamos\s+em\s+\d+/gi,
  ];
  for (const re of patterns) md = md.replace(re, '');
  // Promesses R145
  const r145 = [
    /\bresposta\s+priorit[áa]ria\b/gi,
    /\bresposta\s+r[áa]pida\b/gi,
    /\bresposta\s+garantida\b/gi,
    /\bmediante\s+confirma[çc][ãa]o\b/gi,
    /\ba\s+confirmar\s+por\s+telefone\b/gi,
    /\bchegada\s+em\s+minutos\b/gi,
  ];
  for (const re of r145) md = md.replace(re, '');
  return md;
}

// 8. Pronoms client interdits → formulations neutres
function fixPronouns(md) {
  const swaps = [
    [/\bsozinho\b/g, 'sem a nossa equipa'],
    [/\b(?:sozinha)\b/g, 'sem a nossa equipa'],
    [/\bcontacto\s+pessoal\b/gi, 'contacto com a nossa equipa'],
    [/\bfalar\s+comigo\b/gi, 'contactar a nossa equipa'],
    [/\bminha\s+empresa\b/gi, 'a nossa empresa'],
    [/\bmeu\s+contacto\b/gi, 'o nosso contacto'],
    [/\bfalo\s+consigo\b/gi, 'a nossa equipa contacta'],
  ];
  for (const [re, rep] of swaps) md = md.replace(re, rep);
  return md;
}

// 9. Prix non sourcés → grille officielle ou suppression
function normalizePrecos(md) {
  // a) "X-Y€" fourchettes inventées hors grille → on supprime la fourchette
  //    sauf si X€ = 70 (tarif/h officiel) ou pattern Z1-Z6 (déplacement)
  md = md.replace(/(\d+(?:[.,]\d+)?)\s*€\s*[-–—]\s*(\d+(?:[.,]\d+)?)\s*€\s*\/\s*h\b/g, (m, a, b) => {
    if (parseFloat(a) <= 70 && parseFloat(b) <= 100) return m; // plausible
    return 'sob orçamento';
  });
  // b) "X€ / hora" hors 70€/h → "sob orçamento"
  md = md.replace(/(\d+(?:[.,]\d+)?)\s*€\s*\/\s*(?:h|hora)\b/g, (m, n) => {
    if (parseFloat(n) === 70) return m;
    return 'sob orçamento';
  });
  // c) "X€ + iva" / "X€ (sem iva)" / "acrescer 23%" → suppression
  md = md.replace(/\(?\s*(?:acrescer|sem IVA|sem iva)\s*\+?\s*23%\s*\)?\s*/gi, '');
  md = md.replace(/\b(?:sem iva|com iva)\b\s*/gi, '');
  md = md.replace(/\bIVA\s+(?:a|à|em)\s+taxa\s+(?:legal|normal|em vigor)\b/gi, '');
  // c-bis) PT-BR comuns : pia → lavatório, vazamento → fuga, entupiu → entupido
  md = md.replace(/\bAlarme\s+["“]?pia["”]?\b/gi, 'Alarme do lavatório');
  md = md.replace(/\b(?:na|em)\s+pia\b/gi, (m) => m.replace('pia', 'lavatório'));
  md = md.replace(/["“]pia["”]/g, '"lavatório"');
  // d) "X€/mês" / "X€/ano" → suppression (pas dans la grille)
  md = md.replace(/\b\d+(?:[.,]\d+)?\s*€\s*\/\s*(?:m[êe]s|ano)\b/gi, 'sob orçamento');
  // e) "X€ deslocação" / "X€ saída" → Z1-Z6 si chiffre correspond (15/25/35/45/55/65)
    //    sinon → "sob orçamento" si X € inventé hors grille
    md = md.replace(/(\d+)\s*€\s*(?:desloca[çc][ãa]o|sa[íi]da)/gi, (m, n) => {
      const validZ = ['15','25','35','45','55','65'];
      const z = validZ.indexOf(n);
      if (z >= 0) return `Z${z+1} (${n} € deslocação)`;
      // Pour deslocação hors grille, on supprime et on renvoie "sob orçamento" via patch suivant
      return `sob orçamento (deslocação conforme zona — Z1 15 € a Z6 65 €)`;
    });
    // f) "deslocação X€" (autre sens) → même traitement (sans \b autour de €)
    md = md.replace(/\bdesloca[çc][ãa]o\s+(\d+)\s*€/gi, (m, n) => {
      const validZ = ['15','25','35','45','55','65'];
      const z = validZ.indexOf(n);
      if (z >= 0) return `Z${z+1} (${n} € deslocação)`;
      return `sob orçamento (deslocação conforme zona — Z1 15 € a Z6 65 €)`;
    });
    // g) "preço/valor/custo X€" → si X hors 70€/h → "sob orçamento" (sans \b autour de €)
    md = md.replace(/\b(?:pre[çc]o|valor|custo)\s+(?!70\s*€|15\s*€|25\s*€|35\s*€|45\s*€|55\s*€|65\s*€)(\d+(?:[.,]\d+)?)\s*€/gi, 'sob orçamento');
  return md;
}

// 10. Liens vers pages interdites (certificação/ficha eletrotécnica)
function stripForbiddenLinks(md) {
  md = md.replace(/\[[^\]]*\]\([^)]*(?:certifica[çc]|ficha-eletro|certiel|dgeg)[^)]*\)/gi, '[página removida — serviço não prestado]');
  return md;
}

// 11. CTAs "Ligue agora" → formulations honnêtes
function fixCTA(md) {
  md = md.replace(/\bLigue agora:?\s*\+?\d+/gi, 'Contacto:');
  md = md.replace(/\bLigue j[áa]:?\s*\+?\d+/gi, 'Contacto:');
  md = md.replace(/Arranjo no pr[óo]prio dia/gi, 'Intervenção após diagnóstico e orçamento');
  md = md.replace(/Garantia \d+ meses?/gi, 'garantia por escrito');
  // "WhatsApp:" → préserver (canal légitime)
  return md;
}

// 12. Section "Artigos Relacionados" → ne garder que les liens internes valides (extensionless)
function fixRelatedLinks(md) {
  // garder tel quel — le sitemap et l'audit linkeront
  return md;
}

// 13. Anciennes dates "Última atualização: X 2026" → suppression (datation inventée)
function stripFakeDates(md) {
  md = md.replace(/\*?Última atualiza[çc][ãa]o:?\s*[^.\n]+\*?\s*/gi, '');
  md = md.replace(/\*?Pre[çc]os v[áa]lidos[^.\n]+\*?\s*/gi, '');
  md = md.replace(/\*?Valores? sem IVA[^.\n]+\*?\s*/gi, '');
  return md;
}

// 14. Fausses stats dans le titre (metaTitle, metaDescription)
function fixFrontmatter(md) {
  // métadescription avec "Ligue X" → on n'insère pas le téléphone
  md = md.replace(/(\bLigue\b[^"\n]{0,40}?)\d{3}\s*\d{3}\s*\d{3}/g, '$1Contacto por telefone ou WhatsApp');
  // prix fourchettes dans metaDescription → "sob orçamento"
  return md;
}

// === Master transformation ===
function normalize(md) {
  md = stripTestemunhosSections(md);
  md = stripMarcas(md);
  md = stripStatsNonSourcees(md);
  md = stripDocsEmis(md);
  md = stripDGEG(md);
  md = fixNAP(md);
  md = stripDelaisChiffres(md);
  md = fixPronouns(md);
  md = normalizePrecos(md);
  md = stripForbiddenLinks(md);
  md = fixCTA(md);
  md = stripFakeDates(md);
  md = fixFrontmatter(md);
  return md;
}

// === Main ===
const allMd = fs.readdirSync(BLOG_DIR).filter((f) => f.endsWith('.md'));
const stats = {
  total: allMd.length,
  deleted: 0,
  pilotAlreadyOK: 0,
  normalized: 0,
  needsManual: [],
  skipped: [],
};

for (const f of allMd) {
  const fp = path.join(BLOG_DIR, f);
  const base = path.basename(f);

  if (TO_DELETE.has(base)) {
    if (DRY_RUN) {
      console.log(`[JETE] ${base}`);
    } else {
      fs.unlinkSync(fp);
      // Also unlink the .html if it exists
      const html = fp.replace(/\.md$/, '.html');
      if (fs.existsSync(html)) fs.unlinkSync(html);
    }
    stats.deleted++;
    continue;
  }

  if (base === 'quadro-eletrico-dispara.md' || base === 'disjuntor-dispara-noite-causas-solucoes.md') {
    if (DRY_RUN) console.log(`[PILOTE-OK] ${base} (déjà conforme — skip)`);
    stats.pilotAlreadyOK++;
    continue;
  }

  const orig = fs.readFileSync(fp, 'utf8');
  const beforeFindings = auditConformity(orig);
  if (beforeFindings.length === 0) {
    if (DRY_RUN) console.log(`[DEJA-OK] ${base}`);
    stats.normalized++;
    continue;
  }

  const cleaned = normalize(orig);
  const afterFindings = auditConformity(cleaned);

  if (afterFindings.length === 0) {
    if (!DRY_RUN) {
      fs.writeFileSync(fp, cleaned, 'utf8');
      // Re-render .html
      const { execSync } = require('child_process');
      try {
        execSync(`node scripts/render-blog-md.js --source blog/${base} --out-dir blog`, { stdio: 'pipe', cwd: path.join(__dirname, '..') });
      } catch (e) {
        console.error(`[RENDER-FAIL] ${base}: ${e.message}`);
      }
    }
    if (DRY_RUN) {
      console.log(`[NORMALISE-OK] ${base} (${beforeFindings.length} → 0)`);
    }
    stats.normalized++;
  } else {
    if (DRY_RUN) {
      console.log(`[MANUAL] ${base} (${afterFindings.length} violations restantes)`);
      afterFindings.forEach((f) => console.log(`         - ${f.label}: ${f.sample}`));
    }
    stats.needsManual.push({ file: base, remaining: afterFindings.map((f) => f.label) });
  }
}

console.log('\n=== BILAN ===');
console.log(`Total .md           : ${stats.total}`);
console.log(`Jetés (hors-scope)  : ${stats.deleted}`);
console.log(`Pilotes OK (skip)   : ${stats.pilotAlreadyOK}`);
console.log(`Normalisés (0 viol) : ${stats.normalized}`);
console.log(`À réécrire manuellement : ${stats.needsManual.length}`);
if (stats.needsManual.length > 0) {
  console.log('\nFichiers MANUAL :');
  for (const m of stats.needsManual) console.log(`  - ${m.file} : ${m.remaining.join(', ')}`);
}