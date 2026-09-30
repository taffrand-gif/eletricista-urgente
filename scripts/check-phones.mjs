#!/usr/bin/env node
// Garde-fou numéros de téléphone (appels = conversion principale).
// Échoue si, dans les fichiers servis :
//   - « +351+351 » apparaît (double indicatif) ;
//   - un numéro contient des astérisques (numéro masqué) ;
//   - un lien tel:/WhatsApp ou un JSON-LD « telephone » ne vaut pas exactement le numéro du site ;
//   - un autre numéro de téléphone (autre métier, ancien, test, Staff-Seeker) apparaît dans le HTML servi ;
//   (un numéro Staff-Seeker, ancien ou de test est un « numéro inconnu » : seul le numéro du site est admis).
// Usage : node scripts/check-phones.mjs [dossier servi]   (défaut : dossier par défaut du site)
import fs from "node:fs";
import path from "node:path";

// Numéros confirmés par Filipe le 29/09/2026.
const PLUMBING = "928484451";
const ELECTRICITY = "932321892";
const SITE_NUMBER = ELECTRICITY;
const OTHER_NUMBER = SITE_NUMBER === PLUMBING ? ELECTRICITY : PLUMBING;
const DEFAULT_ROOT = ".";

const root = path.resolve(process.argv[2] || DEFAULT_ROOT);
const SKIP_DIRS = new Set(["node_modules", ".git", ".github", ".vercel", "scripts", "tools", "tests", "_audit", "_reports", "_indexing"]);
const TEXT_EXT = new Set([".html", ".htm", ".txt", ".xml", ".json", ".webmanifest"]);
const IGNORE_FILE = /\.(bak|orig|rej|backup|old|save|tmp)([-.].*)?$|~$|\.pre-fix-|\.backup-/;

const PHONE = /(?<![\d*])(?:\+?351[\s.\-]?)?([29]\d{2})[\s.\-]?(\d{3})[\s.\-]?(\d{3})(?![\d*])/g;
const MASKED = /(?:\+?351[\s.\-]*)?\*{3,}[\s.\-]*\d{2,4}|\+?351[\s.\-]*\*{2,}|tel:[^"'\s>]*\*/g;
const DOUBLE_CC = /\+\s?351[\s.\-]*\+\s?351/g;
const TEL = /href\s*=\s*["']tel:([^"']*)["']/gi;
const WA = /(?:wa\.me\/|api\.whatsapp\.com\/send\/?\?phone=)(\+?[\d*]+)/gi;
const LD_TEL = /"telephone"\s*:\s*"([^"]*)"/g;
// Suites de 9 chiffres qui ne sont pas des numéros de l'entreprise (vérifiées le 29/09/2026).
const NOT_BUSINESS_PHONE = new Map([
  ["248197770", "NIF Norte Reparos"],
  ["213424000", "Proteção Civil (numéro public tiers)"],
  ["999999999", "z-index CSS"],
  ["200000300", "statistique « 200.000-300.000 descargas »"],
]);

function* walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.isDirectory()) {
      if (!SKIP_DIRS.has(e.name)) yield* walk(path.join(dir, e.name));
    } else if (TEXT_EXT.has(path.extname(e.name)) && !IGNORE_FILE.test(e.name) && e.name !== "package.json" && e.name !== "package-lock.json" && !e.name.startsWith("tsconfig")) {
      yield path.join(dir, e.name);
    }
  }
}

const lineOf = (t, i) => t.slice(0, i).split("\n").length;
const digits = (s) => s.replace(/\D/g, "");
const errors = [];
let files = 0;
for (const f of walk(root)) {
  files++;
  const t = fs.readFileSync(f, "utf8");
  const rel = path.relative(root, f);
  const add = (i, rule, s) => errors.push(`${rel}:${lineOf(t, i)} [${rule}] ${s.slice(0, 80)}`);
  for (const m of t.matchAll(DOUBLE_CC)) add(m.index, "double +351", m[0]);
  for (const m of t.matchAll(MASKED)) add(m.index, "numéro masqué", m[0]);
  for (const m of t.matchAll(TEL)) if (digits(m[1]) !== "351" + SITE_NUMBER) add(m.index, "tel: incorrect", m[0]);
  for (const m of t.matchAll(WA)) if (digits(m[1]) !== "351" + SITE_NUMBER) add(m.index, "WhatsApp incorrect", m[0]);
  for (const m of t.matchAll(LD_TEL)) if (digits(m[1]) !== "351" + SITE_NUMBER) add(m.index, "JSON-LD telephone incorrect", m[0]);
  for (const m of t.matchAll(PHONE)) {
    const n = m[1] + m[2] + m[3];
    if (n === SITE_NUMBER || NOT_BUSINESS_PHONE.has(n)) continue;
    add(m.index, n === OTHER_NUMBER ? "numéro de l'autre métier" : "numéro inconnu", m[0]);
  }
}

if (!files) {
  console.error(`check-phones: aucun fichier dans ${root}`);
  process.exit(2);
}
if (errors.length) {
  const byRule = errors.reduce((a, e) => ((a[e.match(/\[(.*?)\]/)[1]] = (a[e.match(/\[(.*?)\]/)[1]] || 0) + 1), a), {});
  console.error(errors.slice(0, 200).join("\n"));
  console.error(`\ncheck-phones: ${errors.length} erreur(s) dans ${files} fichiers — ${JSON.stringify(byRule)}`);
  process.exit(1);
}
console.log(`check-phones: OK — ${files} fichiers, numéro unique +351 ${SITE_NUMBER}`);
