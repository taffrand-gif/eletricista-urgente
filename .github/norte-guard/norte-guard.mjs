#!/usr/bin/env node
// norte-guard — garde-fou anti-régression Norte (mode WARNING par défaut, exit 0).
// Sans dépendance. Même fichier dans les 4 dépôts ; le site est déduit de package.json / dossier / NORTE_SITE.
// Usage :
//   node scripts/norte-guard.mjs --changed            fichiers modifiés vs origin/main (CI PR)
//   node scripts/norte-guard.mjs --all                tout le dépôt suivi par git (dry-run)
//   node scripts/norte-guard.mjs --files a.html b.tsx
//   options : --strict (exit 1 si sévérité BLOCK) · --json out.json · --site CNR|CU|ENR|EU
// Grille officielle : 30 € + 70 €/h (jour ouvré) · 50 € + 100 €/h (nuit/WE/férié) — _governance/20-BUSINESS-FACTS.json.
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { execSync } from "node:child_process";

const argv = process.argv.slice(2);
const has = (f) => argv.includes(f);
const val = (f) => (argv.includes(f) ? argv[argv.indexOf(f) + 1] : null);
const ROOT = process.cwd();

const SITES = {
  CNR: { domain: "canalizador-norte-reparos.pt", trade: "plumbing", phone: "928484451", other: "932321892", sibling: "eletricista-" },
  CU: { domain: "canalizador-urgente.pt", trade: "plumbing", phone: "928484451", other: "932321892", sibling: "eletricista-" },
  ENR: { domain: "eletricista-norte-reparos.pt", trade: "electricity", phone: "932321892", other: "928484451", sibling: "canalizador-" },
  EU: { domain: "eletricista-urgente.pt", trade: "electricity", phone: "932321892", other: "928484451", sibling: "canalizador-" },
};
const detect = () => {
  const forced = val("--site") || process.env.NORTE_SITE;
  if (forced) return forced;
  const n = path.basename(ROOT);
  for (const [k, v] of Object.entries(SITES)) if (n.includes(v.domain.replace(".pt", ""))) return k;
  try {
    const p = JSON.parse(fs.readFileSync("package.json", "utf8")).name || "";
    for (const [k, v] of Object.entries(SITES)) if (p.includes(v.domain.replace(".pt", ""))) return k;
  } catch {}
  const r = execSync("git config --get remote.origin.url || true", { encoding: "utf8" });
  for (const [k, v] of Object.entries(SITES)) if (r.includes(v.domain.replace(".pt", ""))) return k;
  throw new Error("site inconnu : passer --site CNR|CU|ENR|EU");
};
const SITE = detect();
const S = SITES[SITE];
const PLUMB = S.trade === "plumbing";

// ---------- sélection des fichiers ----------
const EXT = /\.(html|tsx|txt|json|mjs)$/;
const SKIP = /(^|\/)(node_modules|dist|\.git|_archive[^/]*|_audit|_reports|_indexing|_prototype|drizzle|scripts\/archive)\//;
const SKIPFILE = /(package(-lock)?|tsconfig[^/]*|components|vercel)\.json$|\.bak|\.orig|(^|\/)(CLAUDE|AGENTS|LECONS|JOURNAL|MARKETING|PRICING|SEO_PLAN|context|README)\.md$|norte-guard/;
function listFiles() {
  let l;
  if (has("--files")) l = argv.slice(argv.indexOf("--files") + 1).filter((a) => !a.startsWith("--"));
  else if (has("--changed")) {
    const base = val("--base") || "origin/main";
    l = execSync(`git diff --name-only --diff-filter=ACMR ${base}...HEAD`, { encoding: "utf8" }).split("\n").filter(Boolean);
  } else l = execSync("git ls-files -z", { encoding: "utf8", maxBuffer: 1 << 28 }).split("\0").filter(Boolean);
  return l.filter((f) => EXT.test(f) && !SKIP.test(f) && !SKIPFILE.test(f) && fs.existsSync(f));
}

// ---------- résultats ----------
const findings = [];
const add = (file, line, rule, sev, surface, snippet) =>
  findings.push({ file, line, rule, sev, surface, snippet: snippet.replace(/\s+/g, " ").trim().slice(0, 140) });
const lineOf = (t, i) => t.slice(0, i).split("\n").length;

// ---------- règles ----------
const OFFICIAL = new Set([30, 50, 70, 100]);
const eurAmt = (s) => parseInt(s.replace(/\D/g, ""), 10);
const MATERIAL_CTX = /material|materiais|tomada|disjuntor|cabo\b|torneira|autoclismo|marca\b|modelo|produto|aparelho|lâmpada|lampada|quadro|termoacumulador|bomba|contador|wallbox/i;

// {regex, rule, sev}
const RX_TECH = [
  [/tel:\+?351\s?\*+|\*{3,}\s?\d{3,4}|\+?351[\s.-]*\*{2,}/g, "TEL_MASQUE", "BLOCK"],
  [/\{\{\s*[a-z-]+\s*:\s*[a-z0-9#%.-]+\s*;?\s*\}\}/gi, "CSS_DOUBLE_ACCOLADE", "BLOCK"],
  [/\+351\s*\+351/g, "TEL_DOUBLE_INDICATIF", "BLOCK"],
];
const RX_PRICE = [
  [/\bZ[1-6]\b(?=[^a-z]{0,25}(km|€|eur|\d))/gi, "PRIX_ZONE_Z1_Z6", "BLOCK"],
  [/\bzona\s?[1-6]\b/gi, "PRIX_ZONE_NUM", "WARN"],
  [/\bsuplemento\b[^.\n]{0,60}(€|%)|\+\s?50\s?%[^.\n]{0,40}(noite|noturn|fim de semana|nuit|feriad)/gi, "PRIX_ANCIEN_SUPPLEMENT", "WARN"],
  [/\bpriceAdjustment\b|\btotalMin\b|\btotalMax\b|\bosrm\b|\btomtom\b[^\n]{0,40}(pre[cç]o|price)/gi, "PRIX_LOGIQUE_DISTANCE", "BLOCK"],
];
const RX_CLAIMS = [
  [/trustpilot|avalia[cç][õo]es? (no )?google|rating(Value|Count)|AggregateRating|"@type"\s*:\s*"Review"/gi, "CLAIM_AVIS", "WARN"],
  [/\b(8\d|9\d)\s?%|\b30\s?%\s+abaixo/gi, "CLAIM_POURCENTAGE", "WARN"],
  [/garantia (de )?\d+|\b(12 meses|24 meses|1 ano|2 anos)\b[^.\n]{0,20}garantia|garantia[^.\n]{0,30}\b(12 meses|1 ano|2 anos)\b/gi, "CLAIM_GARANTIE_CHIFFREE", "WARN"],
  [/seguro[^.\n]{0,40}\d{2,3}[ .]?000\s?€|\d{2,3}[ .]?000\s?€[^.\n]{0,30}seguro/gi, "CLAIM_ASSURANCE_CHIFFREE", "WARN"],
  [/\b\d{2,3}\s?km\b[^.\n]{0,30}(raio|cobertura|dist[aâ]ncia)|raio (de )?\d{2,3}\s?km/gi, "CLAIM_RAYON", "WARN"],
  [/\b(chega(mos)?|chegada|resposta)\b[^.\n]{0,40}\b(\d+\s?(min|h)\b)|\b15\s?[–-]\s?(40|90)\s?min|\b(1|2|3|5)\s?h\b[^.\n]{0,15}(chegada|resposta)|confirma[cç][aã]o-?[235]h|resposta imediata|atendimento imediato/gi, "CLAIM_DELAI_ARRIVEE", "WARN"],
  [/resolvido em 1\s?h|garantid[oa]s?\b|o mais barato|\bmais barato\b|\bo melhor\b|\bmelhor (pre[cç]o|canalizador|eletricista)\b|\b[úu]nic[oa] (em|na|no)\b|\bmesma pessoa\b/gi, "CLAIM_SUPERLATIF", "WARN"],
  [/credenciado pela DGEG|TRIESP|certificad[oa]s? (pela|DGEG)|\b(Grundfos|Schneider|Legrand|Efapel|Hager|ABB|Geberit|Grohe)\b/gi, "CLAIM_CERT_MARQUE", "INFO"],
  [/Mensagem directa|Resposta a confirmar/gi, "TUILE_MENSAGEM_DIRECTA", "WARN"],
];
const RX_METIER_PLUMB_ON_ELEC = /canaliza[cç][aã]o|canalizador|fuga de [aá]gua|esgoto|desentup|Guia Canaliza|guia-canalizacao|entupid/gi;
const RX_METIER_ELEC_ON_PLUMB = /ficha eletrot[eé]cnica|termo de responsabilidade|instala[cç][aã]o el[eé]trica|eletricista|quadro el[eé]trico|curto-circuito|wallbox|TRIESP|DGEG/gi;

// ---------- extraction par surface ----------
function surfaces(file, t) {
  const out = []; // {surface, text, offset}
  if (!/\.html$/.test(file)) return [{ surface: /\.(txt|json)$/.test(file) ? "file-text" : "source", text: t, offset: 0 }];
  let rest = t;
  const mask = (re, surface) => {
    rest = rest.replace(re, (m, g1, off) => {
      out.push({ surface, text: m, offset: off });
      return " ".repeat(m.length);
    });
  };
  mask(/<script[^>]*application\/ld\+json[^>]*>([\s\S]*?)<\/script>/gi, "jsonld");
  mask(/<script\b(?![^>]*application\/ld\+json)[^>]*>([\s\S]*?)<\/script>/gi, "script");
  mask(/<style[\s\S]*?<\/style>/gi, "style");
  mask(/<meta\b[^>]*(name|property)=["'](description|og:[a-z:]+|twitter:[a-z]+)["'][^>]*>|<title>[\s\S]*?<\/title>/gi, "meta");
  out.push({ surface: "visible", text: rest, offset: 0 });
  return out;
}

// ---------- vérifs structurelles HTML ----------
const siteFiles = new Set(execSync("git ls-files", { encoding: "utf8", maxBuffer: 1 << 28 }).split("\n"));
let rewrites = [];
try {
  rewrites = (JSON.parse(fs.readFileSync("vercel.json", "utf8")).rewrites || []).map((r) =>
    new RegExp("^" + r.source.replace(/:[a-zA-Z]+\*?/g, "[^/]+").replace(/\(\.\*\)/g, ".*").replace(/\//g, "\\/") + "$"));
} catch {}
const roots = [".", "client/public", "public", "dist/public"];
const routeExists = (p) => {
  p = p.split(/[?#]/)[0].replace(/\/$/, "") || "/";
  if (p === "/") return true;
  if (rewrites.some((re) => re.test(p))) return true; // rewrites génériques : non vérifiable ici (faux négatifs documentés)
  return roots.some((r) => [p, p + ".html", p + "/index.html"].some((c) => siteFiles.has(path.posix.join(r, c.slice(1)).replace(/^\.\//, ""))));
};

function checkHtml(file, t) {
  const isFullPage = /<html[\s>]/i.test(t) && /<head[\s>]/i.test(t);
  if (!isFullPage) return;
  const noindex = /<meta[^>]+name=["']robots["'][^>]+noindex/i.test(t);
  const redirectStub = /http-equiv=["']refresh["']/i.test(t);
  // JSON-LD
  for (const m of t.matchAll(/<script[^>]*application\/ld\+json[^>]*>([\s\S]*?)<\/script>/gi)) {
    let j;
    try { j = JSON.parse(m[1]); } catch (e) { add(file, lineOf(t, m.index), "JSONLD_INVALIDE", "BLOCK", "jsonld", e.message); continue; }
    const nodes = [].concat(j["@graph"] || j);
    for (const n of nodes) {
      if (!n || typeof n !== "object") continue;
      for (const k of ["type", "context", "id"]) if (k in n && !("@" + k in n)) add(file, lineOf(t, m.index), "JSONLD_CLE_CASSEE", "BLOCK", "jsonld", `clé « ${k} » sans @`);
      if (!n["@type"] && !("@graph" in j) && !("@context" in n)) add(file, lineOf(t, m.index), "JSONLD_SANS_TYPE", "WARN", "jsonld", Object.keys(n).join(","));
    }
    const walk = (o) => {
      if (Array.isArray(o)) return o.forEach(walk);
      if (o && typeof o === "object") for (const [k, v] of Object.entries(o)) {
        if (/^(price|minPrice|maxPrice|lowPrice|highPrice)$/.test(k) && v !== "" && !String(v).split(/[-–]/).every((x) => OFFICIAL.has(Number(x.replace(",", ".")))) && Number(v) !== 0)
          add(file, lineOf(t, m.index), "PRIX_JSONLD_NON_OFFICIEL", "BLOCK", "jsonld", `${k}=${v}`);
        if (/ratingValue|reviewCount|ratingCount/.test(k)) add(file, lineOf(t, m.index), "CLAIM_AVIS_JSONLD", "WARN", "jsonld", `${k}=${v}`);
        walk(v);
      }
    };
    walk(j);
  }
  // canonical
  if (!noindex && !redirectStub) {
    const c = t.match(/<link[^>]+rel=["']canonical["'][^>]*>/i);
    if (!c) add(file, 1, "CANONICAL_ABSENTE", "BLOCK", "meta", "pas de rel=canonical sur page indexable");
    else {
      const h = (c[0].match(/href=["']([^"']*)["']/i) || [])[1] || "";
      if (!h || /undefined|null|\{\{|\$\{|\.\.|%7B/.test(h) || !/^https:\/\//.test(h) || /^https:\/\/[^/]+\/.*\/\//.test(h) || !h.includes(S.domain))
        add(file, lineOf(t, c.index), "CANONICAL_CASSEE", "BLOCK", "meta", h);
    }
  }
  // scripts inline : syntaxe
  for (const m of t.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)) {
    if (/application\/ld\+json|type=["'](module|text\/template|importmap)/i.test(m[1]) || !m[2].trim()) continue;
    try { new vm.Script(m[2]); } catch (e) { add(file, lineOf(t, m.index), "JS_SYNTAXE", "BLOCK", "script", e.message); }
  }
  // liens tel / WhatsApp / internes
  for (const m of t.matchAll(/href=["']([^"']+)["']/gi)) {
    const h = m[1];
    if (/^tel:/i.test(h)) {
      const d = h.replace(/^tel:/i, "").replace(/[\s.-]/g, "");
      if (!/^\+351\d{9}$/.test(d)) add(file, lineOf(t, m.index), "TEL_INVALIDE", "BLOCK", "visible", h);
      else if (!d.endsWith(S.phone)) add(file, lineOf(t, m.index), "TEL_MAUVAIS_METIER", "BLOCK", "visible", `${h} (attendu ${S.phone})`);
      else if (h !== "tel:" + d) add(file, lineOf(t, m.index), "TEL_FORMAT_ESPACES", "INFO", "visible", h);
    } else if (/wa\.me|whatsapp\.com/i.test(h)) {
      const d = (h.match(/(?:wa\.me\/|phone=)\+?([\d*]+)/i) || [])[1];
      if (!d) add(file, lineOf(t, m.index), "WHATSAPP_SANS_NUMERO", "WARN", "visible", h);
      else if (!/^351\d{9}$/.test(d)) add(file, lineOf(t, m.index), "WHATSAPP_INVALIDE", "BLOCK", "visible", h);
      else if (!d.endsWith(S.phone)) add(file, lineOf(t, m.index), "WHATSAPP_MAUVAIS_METIER", "BLOCK", "visible", `${h} (attendu ${S.phone})`);
    } else if (h.startsWith("/") && !h.startsWith("//") && !/\.(png|jpe?g|webp|svg|ico|css|js|xml|txt|pdf|json|woff2?)$/i.test(h)) {
      if (!routeExists(h)) add(file, lineOf(t, m.index), "LIEN_INTERNE_404", "WARN", "visible", h);
    } else if (h.includes(S.sibling) && /\.pt/.test(h)) {
      // lien domaine frère : toléré en navigation/orientation (nav, footer) — signalé INFO sinon WARN
      const ctx = t.slice(Math.max(0, m.index - 600), m.index);
      const inNav = /<(nav|footer)\b(?![\s\S]*<\/(nav|footer)>)/i.test(ctx) || /orienta|site-irm[aã]o|outros servi[cç]os/i.test(ctx);
      add(file, lineOf(t, m.index), "LIEN_DOMAINE_FRERE", inNav ? "INFO" : "WARN", "visible", h);
    }
  }
}

// ---------- scan texte par surface ----------
function scanText(file, t) {
  const isGenerator = /\.(mjs)$/.test(file);
  for (const sf of surfaces(file, t)) {
    const run = (list, extraFilter) => {
      for (const [rx, rule, sev0] of list) {
        for (const m of sf.text.matchAll(rx)) {
          let sev = sev0;
          const ln = sf.text.slice(Math.max(0, m.index - 80), m.index + m[0].length + 80);
          if (extraFilter && !extraFilter(rule, ln, m)) continue;
          add(file, lineOf(t, sf.offset + m.index), rule, sev, sf.surface, ln);
        }
      }
    };
    run(RX_TECH);
    // tsx : accolades doubles légitimes en JSX, on ne garde que les cas CSS dans une chaîne
    run(RX_PRICE);
    run(RX_CLAIMS);
    // montants €/h et déplacement
    for (const m of sf.text.matchAll(/(\d{1,3}(?:[.,]\d{1,2})?)\s?(?:€|EUR|euros?)\s?\/\s?(?:h|hora)\b/gi)) {
      const a = eurAmt(m[1]);
      const ln = sf.text.slice(Math.max(0, m.index - 80), m.index + 80);
      if (OFFICIAL.has(a)) continue;
      if (MATERIAL_CTX.test(ln)) { add(file, lineOf(t, sf.offset + m.index), "PRIX_HORAIRE_CTX_MATERIEL?", "INFO", sf.surface, ln); continue; }
      add(file, lineOf(t, sf.offset + m.index), "PRIX_HORAIRE_NON_OFFICIEL", sf.surface === "visible" || sf.surface === "jsonld" ? "BLOCK" : "WARN", sf.surface, ln);
    }
    for (const m of sf.text.matchAll(/desloca[cç][aã]o[^.\n<]{0,40}?(\d{1,3})\s?(?:€|EUR|euros?)|(\d{1,3})\s?(?:€|EUR|euros?)\s+(?:de\s+)?desloca[cç][aã]o/gi)) {
      const a = parseInt(m[1] || m[2], 10);
      if (!OFFICIAL.has(a)) add(file, lineOf(t, sf.offset + m.index), "PRIX_DEPLACEMENT_NON_OFFICIEL", "WARN", sf.surface, m[0]);
    }
    // séparation des métiers (hors jsonld/script/style pour limiter le bruit : visible, meta, fichiers texte, sources)
    if (["visible", "meta", "file-text", "source"].includes(sf.surface) && !isGenerator) {
      const rx = PLUMB ? RX_METIER_ELEC_ON_PLUMB : RX_METIER_PLUMB_ON_ELEC;
      const rule = PLUMB ? "METIER_ELEC_SUR_SITE_PLOMBERIE" : "METIER_PLOMBERIE_SUR_SITE_ELEC";
      for (const m of sf.text.matchAll(rx)) {
        const ln = sf.text.slice(Math.max(0, m.index - 80), m.index + m[0].length + 80);
        const sibling = /href=["'][^"']*(eletricista|canalizador)-[^"']*\.pt/i.test(ln);
        add(file, lineOf(t, sf.offset + m.index), rule, sibling ? "INFO" : "WARN", sf.surface, ln);
        if (/guia-canalizacao|Guia Canaliza/i.test(m[0]) && !PLUMB) findings[findings.length - 1].rule = "GUIA_CANALISATION_SUR_ELEC";
      }
      // autre numéro métier en clair
      const other = new RegExp(`(?<!\\d)(?:\\+?351[\\s.-]?)?${S.other.slice(0, 3)}[\\s.-]?${S.other.slice(3, 6)}[\\s.-]?${S.other.slice(6)}(?!\\d)`, "g");
      for (const m of sf.text.matchAll(other)) add(file, lineOf(t, sf.offset + m.index), "TEL_AUTRE_METIER", /\.(txt|json)$/.test(file) && new RegExp(S.sibling + "[a-z-]*\\.pt").test(sf.text.slice(Math.max(0, m.index - 120), m.index + 60)) ? "INFO" : "BLOCK", sf.surface, sf.text.slice(Math.max(0, m.index - 60), m.index + 40));
    }
  }
  if (/\.html$/.test(file)) checkHtml(file, t);
}

// ---------- main ----------
const files = listFiles();
for (const f of files) {
  let t;
  try { t = fs.readFileSync(f, "utf8"); } catch { continue; }
  if (t.length > 3_000_000) continue;
  scanText(f, t);
}

// --added-only : ne garde que les constats situés sur des lignes ajoutées/modifiées vs --base (évite de reprocher l'historique à une PR)
let kept = findings;
if (has("--added-only")) {
  const base = val("--base") || "origin/main";
  const added = {};
  let cur = null;
  for (const l of execSync(`git diff -U0 --no-color ${base}...HEAD`, { encoding: "utf8", maxBuffer: 1 << 28 }).split("\n")) {
    const f = l.match(/^\+\+\+ b\/(.+)$/); if (f) { cur = f[1]; added[cur] = new Set(); continue; }
    const h = l.match(/^@@ -\S+ \+(\d+)(?:,(\d+))? @@/);
    if (h && cur) { const st = +h[1], n = h[2] === undefined ? 1 : +h[2]; for (let i = 0; i < n; i++) added[cur].add(st + i); }
  }
  kept = findings.filter((f) => added[f.file] && added[f.file].has(f.line));
  findings.length = 0; findings.push(...kept);
}
const sum = {};
for (const f of findings) { const k = `${f.sev} ${f.rule}`; sum[k] = (sum[k] || 0) + 1; }
const nBlock = findings.filter((f) => f.sev === "BLOCK").length;
console.log(`norte-guard · site=${SITE} · fichiers=${files.length} · constats=${findings.length} (BLOCK=${nBlock}) · mode=${has("--strict") ? "STRICT" : "WARNING"}`);
for (const [k, n] of Object.entries(sum).sort()) console.log(`  ${String(n).padStart(6)}  ${k}`);
if (val("--json")) fs.writeFileSync(val("--json"), JSON.stringify({ site: SITE, files: files.length, summary: sum, findings }, null, 1));
if (process.env.GITHUB_ACTIONS) {
  for (const f of findings.filter((x) => x.sev !== "INFO").slice(0, 50))
    console.log(`::warning file=${f.file},line=${f.line},title=${f.rule}::${f.surface} · ${f.snippet.replace(/[\r\n%]/g, " ")}`);
}
process.exit(has("--strict") && nBlock ? 1 : 0);
