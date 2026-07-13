#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');

const DOMAIN = 'https://eletricista-urgente.pt';
const PHONE_DISPLAY = '+351 932 321 892';
const PHONE_E164 = '+351932321892';
const WHATSAPP = 'https://wa.me/351932321892?text=Ol%C3%A1%2C%20preciso%20de%20ajuda%20com%20uma%20avaria%20el%C3%A9trica';
const PRICE_TEXT = '70 €/h';
const ZONES_TEXT = 'Z1=15 € / Z2=25 € / Z3=35 € / Z4=45 € / Z5=55 € / Z6=65 €';
const BATCH_LIMIT = 95;

function die(message) {
  console.error(message);
  process.exitCode = 1;
}

function parseArgs(argv) {
  const args = { source: 'blog', outDir: 'blog', dryRun: false };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--source') args.source = argv[++i];
    else if (arg === '--out-dir') args.outDir = argv[++i];
    else if (arg === '--dry-run') args.dryRun = true;
    else if (arg === '--help') args.help = true;
    else throw new Error(`Argument inconnu: ${arg}`);
  }
  if (!args.source || !args.outDir) throw new Error('--source et --out-dir exigent une valeur');
  return args;
}

function help() {
  console.log(`Usage: node scripts/render-blog-md.js [options]\n\n` +
    `  --source <fichier|dossier>  Source Markdown (défaut: blog)\n` +
    `  --out-dir <dossier>        Sortie HTML (défaut: blog)\n` +
    `  --dry-run                  Valide sans écrire\n\n` +
    `Le renderer refuse tout contenu contraire à AGENTS.md. Un dossier de plus de ` +
    `${BATCH_LIMIT} sources est refusé afin de respecter R15.`);
}

function unquote(value) {
  const v = value.trim();
  if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) {
    return v.slice(1, -1);
  }
  return v;
}

function parseScalar(value) {
  const v = unquote(value);
  if (v.startsWith('[') && v.endsWith(']')) {
    return v.slice(1, -1).split(',').map((item) => unquote(item.trim())).filter(Boolean);
  }
  if (v === 'true') return true;
  if (v === 'false') return false;
  return v;
}

function parseFrontmatter(source) {
  if (!source.startsWith('---\n')) throw new Error('frontmatter YAML manquant');
  const end = source.indexOf('\n---\n', 4);
  if (end === -1) throw new Error('frontmatter YAML non fermé');
  const raw = source.slice(4, end);
  const data = {};
  let currentKey = null;
  for (const line of raw.split('\n')) {
    if (!line.trim() || line.trimStart().startsWith('#')) continue;
    const top = line.match(/^([A-Za-z][\w-]*):(?:\s*(.*))?$/);
    if (top) {
      currentKey = top[1];
      data[currentKey] = top[2] ? parseScalar(top[2]) : {};
      continue;
    }
    const child = line.match(/^\s+([A-Za-z][\w-]*):(?:\s*(.*))?$/);
    if (child && currentKey) {
      if (typeof data[currentKey] !== 'object' || Array.isArray(data[currentKey])) data[currentKey] = {};
      data[currentKey][child[1]] = parseScalar(child[2] || '');
    }
  }
  return { data, body: source.slice(end + 5).trim() };
}

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function stripMarkdown(value) {
  return String(value)
    .replace(/!\[[^\]]*\]\([^)]*\)/g, '')
    .replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')
    .replace(/[*_`>#]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}

function slugify(value) {
  return stripMarkdown(value)
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
}

function inlineMarkdown(value) {
  let out = escapeHtml(value);
  out = out.replace(/`([^`]+)`/g, '<code>$1</code>');
  out = out.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  out = out.replace(/__([^_]+)__/g, '<strong>$1</strong>');
  out = out.replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, '<em>$1</em>');
  out = out.replace(/\[([^\]]+)\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g, (_m, label, href) => {
    const safeHref = /^(?:https?:\/\/|\/|tel:|mailto:)/.test(href) ? href : '#';
    return `<a href="${escapeHtml(safeHref)}">${label}</a>`;
  });
  return out;
}

function markdownToHtml(markdown) {
  const lines = markdown.replace(/\r\n/g, '\n').split('\n');
  const out = [];
  let paragraph = [];
  let listType = null;
  let inCode = false;
  let code = [];

  function flushParagraph() {
    if (paragraph.length) {
      out.push(`<p>${inlineMarkdown(paragraph.join(' '))}</p>`);
      paragraph = [];
    }
  }
  function closeList() {
    if (listType) {
      out.push(`</${listType}>`);
      listType = null;
    }
  }

  for (let i = 0; i < lines.length; i += 1) {
    const line = lines[i];
    if (line.startsWith('```')) {
      flushParagraph(); closeList();
      if (inCode) {
        out.push(`<pre><code>${escapeHtml(code.join('\n'))}</code></pre>`);
        code = [];
      }
      inCode = !inCode;
      continue;
    }
    if (inCode) { code.push(line); continue; }

    if (/^\s*\|.*\|\s*$/.test(line) && i + 1 < lines.length && /^\s*\|?\s*:?-+/.test(lines[i + 1])) {
      flushParagraph(); closeList();
      const headers = line.trim().replace(/^\||\|$/g, '').split('|').map((v) => v.trim());
      i += 1;
      const rows = [];
      while (i + 1 < lines.length && /^\s*\|.*\|\s*$/.test(lines[i + 1])) {
        i += 1;
        rows.push(lines[i].trim().replace(/^\||\|$/g, '').split('|').map((v) => v.trim()));
      }
      out.push('<div class="table-wrap"><table><thead><tr>' + headers.map((v) => `<th>${inlineMarkdown(v)}</th>`).join('') + '</tr></thead><tbody>');
      for (const row of rows) out.push('<tr>' + row.map((v) => `<td>${inlineMarkdown(v)}</td>`).join('') + '</tr>');
      out.push('</tbody></table></div>');
      continue;
    }

    const heading = line.match(/^(#{1,6})\s+(.+)$/);
    if (heading) {
      flushParagraph(); closeList();
      const level = heading[1].length;
      const text = stripMarkdown(heading[2]);
      out.push(`<h${level} id="${escapeHtml(slugify(text))}">${inlineMarkdown(heading[2])}</h${level}>`);
      continue;
    }

    const list = line.match(/^\s*([-+*])\s+(.+)$/);
    const ordered = line.match(/^\s*\d+[.)]\s+(.+)$/);
    if (list || ordered) {
      flushParagraph();
      const wanted = ordered ? 'ol' : 'ul';
      if (listType !== wanted) { closeList(); listType = wanted; out.push(`<${wanted}>`); }
      out.push(`<li>${inlineMarkdown((ordered || list)[ordered ? 1 : 2])}</li>`);
      continue;
    }

    const quote = line.match(/^>\s?(.*)$/);
    if (quote) {
      flushParagraph(); closeList();
      out.push(`<blockquote>${inlineMarkdown(quote[1])}</blockquote>`);
      continue;
    }

    if (/^\s*(?:---+|\*\*\*+)\s*$/.test(line)) {
      flushParagraph(); closeList(); out.push('<hr>'); continue;
    }
    if (!line.trim()) { flushParagraph(); closeList(); continue; }
    paragraph.push(line.trim());
  }
  flushParagraph(); closeList();
  if (inCode) throw new Error('bloc de code Markdown non fermé');
  return out.join('\n');
}

const CONFORMITY_RULES = [
  ['NAP plomberie/placeholder téléphone', /(?:\b928\s*484\s*451\b|tel:\+351\*{2,})/i],
  ['contenu plomberie hors métier', /\b(?:canalizador|canalização|desentupimento|autoclismo)\b/i],
  ['délai de réponse chiffré', /(?:resposta|chegada|chegar|técnic[oa]|demoram?)[^\n.]{0,45}\b\d+(?:[.,]\d+)?\s*(?:min(?:uto)?s?|h(?:oras?)?)\b|atendimento[^\n.]{0,45}\b\d+(?:[.,]\d+)?\s*(?:min(?:uto)?s?|horas?)\b/i],
  ['promesse R145', /\b(?:resposta prioritária|resposta rápida|resposta garantida|mediante confirmação|a confirmar por telefone|chegada em minutos)\b/i],
  ['témoignage ou exemple inventé', /(?:^|\n)#{2,4}\s+(?:testemunhos?|exemplos? reais?|casos reais?|dados de \d+\+?\s*interven[çc][õo]es?|com base na nossa experi[êe]ncia)\b|\b(?:dados de )?\d+\+?\s+intervenções\b|\b(?:Maria|João|Ana)\s+[A-Z]\./im],
  ['statistique terrain non sourcée', /\b\d+(?:[.,]\d+)?\s*%\s+(?:dos|das|de)\s+casos\b|\b(?:casos|problemas) que (?:vemos|resolvemos)\b/i],
  ['document/certification émis', /\b(?:emit(?:e|imos|ir|ido)[^\n.]{0,50}(?:certificad|relatório|ficha)|fichas? eletrotécnicas?|relatório técnico|certificado em \d|certificação completa|instalações certificadas)\b/i],
  ['statut DGEG interdit', /\b(?:DGEG|registo em curso|aguardando registo|1757\/2026\/DIEN)\b/i],
  ['prix/fourchette non sourcé', /(?:\b(?!70(?:[.,]0+)?\s*€\s*\/\s*h\b)\d+(?:[.,]\d+)?\s*€\s*(?:[-–]\s*\d+(?:[.,]\d+)?\s*€)?\s*\/\s*(?:h|hora)\b|\b\d+(?:[.,]\d+)?\s*€\s*por\s+(?:arranjar|reparar|substituir|diagn[óo]stico|interven[çc][ãa]o|m[ãa]o)|(?:desloca[çc][ãa]o|sa[íi]da)\s+(?!Z[1-6]\b)\d+\s*€)/i],
  ['ancienneté/volume non vérifié', /\b(?:\d+\+?\s+anos? de experiência|mais de \d+ anos|\d+%\s+(?:problemas?|casos?|clientes?|interven[çc][õo]es?|avarias?)\s+(?:resolvidos?|resolvidas?|satisfeitos?))\b/i],
  ['PT-BR', /\b(?:vazamento|entupiu|disjuntor caiu|pia)\b/i],
  ['service interdit', /^(?:title:.*|##\s+.*)\b(?:pain[ée]is?\s+solares?|instala[çc][ãa]o\s+solar|bomba\s+de\s+calor|carregador(?:es)?\s+(?:de\s+)?ve[íi]culos?\s+el[ée]tricos?|carregador\s+ve|ar\s+condicionado\s+central)\b/im],
  ['pronom client interdit', /(?<![a-záéíóúâêôãõç])(?:^|\.\s+)eu\s+(?:sou|faço|trabalho|posso|tenho|vou|vim|estou|aconselho|garanto|sugiro|recomendo|indico|preocupo|trato|atendo|mantenho|considero|costumo|preciso|prefiro|desejo|gosto|quisera|queria)\b|(?<![a-záéíóúâêôãõç])\bmeu\s+(?:contacto|telefone|número|email|preço|orçamento|cliente|serviço|empresa|trabalho)\b|(?<![a-záéíóúâêôãõç])\bminha\s+(?:empresa|marca|opinião|experiência|abordagem)\b|\bsozinho\s*,|\bcontacto\s+pessoal\b|\bfalar\s+comigo\b|(?<![a-záéíóúâêôãõç])posso\s+fazer\s+sozinho\b/i],
];

function auditConformity(source) {
  const findings = [];
  for (const [label, regex] of CONFORMITY_RULES) {
    const match = source.match(regex);
    if (match) findings.push({ label, sample: stripMarkdown(match[0]).slice(0, 100) });
  }
  return findings;
}

function bodyWithoutH1(body) {
  const h1 = body.match(/^#\s+(.+)$/m);
  if (!h1) throw new Error('H1 Markdown manquant');
  const count = (body.match(/^#\s+.+$/gm) || []).length;
  if (count !== 1) throw new Error(`exactement 1 H1 attendu, trouvé: ${count}`);
  return { h1: stripMarkdown(h1[1]), body: body.replace(/^#\s+.+\n?/m, '').trim() };
}

function wordCount(value) {
  return stripMarkdown(value).split(/\s+/).filter(Boolean).length;
}

function directAnswer(frontmatter, body) {
  let answer = stripMarkdown(frontmatter.directAnswer || frontmatter.excerpt || frontmatter.summary || '');
  if (!answer) {
    const first = body.split(/\n\s*\n/).find((block) => block.trim() && !block.trim().startsWith('#')) || '';
    answer = stripMarkdown(first);
  }
  const suffix = 'A nossa equipa explica o diagnóstico, aplica 70 €/h e apresenta orçamento por escrito antes de qualquer intervenção, com deslocação conforme a zona e sem surpresas na fatura.';
  while (wordCount(answer) < 40 && !answer.includes(suffix)) answer = `${answer} ${suffix}`.trim();
  const words = answer.split(/\s+/).filter(Boolean);
  if (words.length > 60) answer = `${words.slice(0, 59).join(' ').replace(/[,:;]$/, '')}.`;
  const count = wordCount(answer);
  if (count < 40 || count > 60) throw new Error(`resposta direta doit faire 40-60 mots, trouvé: ${count}`);
  const findings = auditConformity(answer);
  if (findings.length) throw new Error(`resposta direta non conforme: ${findings.map((f) => f.label).join(', ')}`);
  return answer;
}

function extractFaq(markdown) {
  const lines = markdown.split('\n');
  const start = lines.findIndex((line) => /^##\s+.*(?:Perguntas Frequentes|FAQ)/i.test(line));
  if (start === -1) return [];
  const entries = [];
  for (let i = start + 1; i < lines.length && entries.length < 16; i += 1) {
    if (/^##\s+/.test(lines[i])) break;
    const q = lines[i].match(/^###\s+(?:\d+[.)]\s*)?(.+?\??)$/) || lines[i].match(/^\*\*(?:P:|\d+[.)])?\s*(.+?\?)\*\*$/);
    if (!q) continue;
    const answer = [];
    for (i += 1; i < lines.length; i += 1) {
      if (/^#{2,3}\s+/.test(lines[i]) || /^\*\*(?:P:|\d+[.)])?\s*.+?\?\*\*$/.test(lines[i])) { i -= 1; break; }
      if (lines[i].trim()) answer.push(lines[i].trim());
    }
    const text = stripMarkdown(answer.join(' ')).replace(/^Resposta:\s*/i, '');
    if (text) entries.push({ question: stripMarkdown(q[1]), answer: text });
  }
  return entries;
}

function extractHowTo(markdown, frontmatter) {
  const type = frontmatter.schema && frontmatter.schema.type;
  const hasHowTo = String(type || '').toLowerCase() === 'howto' || /^##\s+.*(?:passo a passo|o que fazer)/im.test(markdown);
  if (!hasHowTo) return null;
  const steps = [];
  for (const match of markdown.matchAll(/^\s*\d+[.)]\s+(.+)$/gm)) {
    steps.push(stripMarkdown(match[1]));
    if (steps.length === 7) break;
  }
  if (steps.length < 2) return null;
  return steps;
}

function collectAreaServed(repoRoot) {
  const dir = path.join(repoRoot, 'concelhos');
  const names = fs.existsSync(dir)
    ? fs.readdirSync(dir).filter((name) => name.endsWith('.html')).map((name) => name.replace(/\.html$/, '').split('-').map((part) => part.charAt(0).toUpperCase() + part.slice(1)).join(' '))
    : [];
  return ['Trás-os-Montes', ...names].map((name) => ({ '@type': 'AdministrativeArea', name }));
}

function makeSchemas({ title, description, slug, date, faq, howTo, repoRoot }) {
  const url = `${DOMAIN}/blog/${slug}`;
  const areaServed = collectAreaServed(repoRoot);
  const provider = {
    '@type': 'EmergencyService',
    additionalType: ['https://schema.org/Electrician', 'https://schema.org/LocalBusiness'],
    '@id': `${DOMAIN}/#electrician`,
    name: 'Norte Reparos — Eletricista Urgente',
    telephone: PHONE_E164,
    url: DOMAIN,
    priceRange: '70 €/h + deslocação Z1-Z6',
    areaServed,
  };
  const emergency = { '@context': 'https://schema.org', ...provider };
  const service = {
    '@context': 'https://schema.org',
    '@type': 'Service',
    '@id': `${url}#service`,
    name: title,
    description,
    url,
    serviceType: 'Diagnóstico e reparação de avarias elétricas',
    provider: { '@id': `${DOMAIN}/#electrician` },
    areaServed,
    offers: { '@type': 'Offer', price: '70', priceCurrency: 'EUR', description: 'Mão de obra: 70 €/h; deslocação conforme Z1-Z6; +50% noite, domingo e feriado.' },
  };
  const faqSchema = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    '@id': `${url}#faq`,
    mainEntity: faq.map((entry) => ({ '@type': 'Question', name: entry.question, acceptedAnswer: { '@type': 'Answer', text: entry.answer } })),
  };
  const article = {
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    headline: title,
    description,
    url,
    datePublished: date,
    dateModified: date,
    author: { '@type': 'Organization', name: 'Norte Reparos' },
    publisher: { '@type': 'Organization', name: 'Norte Reparos', url: DOMAIN },
  };
  const schemas = [emergency, service, faqSchema, article];
  if (howTo) schemas.push({
    '@context': 'https://schema.org',
    '@type': 'HowTo',
    '@id': `${url}#howto`,
    name: title,
    description,
    step: howTo.map((text, index) => ({ '@type': 'HowToStep', position: index + 1, name: `Passo ${index + 1}`, text })),
  });
  return schemas;
}

function jsonLd(value) {
  return `<script type="application/ld+json">${JSON.stringify(value).replace(/<\//g, '<\\/')}</script>`;
}

function renderPage(parsed, repoRoot) {
  const { data: frontmatter, body: rawBody } = parsed;
  if (!frontmatter.title) throw new Error('frontmatter title manquant');
  if (!frontmatter.date) throw new Error('frontmatter date manquant');
  const { h1, body } = bodyWithoutH1(rawBody);
  const title = stripMarkdown(frontmatter.title);
  if (title !== h1) throw new Error(`title et H1 divergent: "${title}" != "${h1}"`);
  const titleFindings = auditConformity(title);
  if (titleFindings.length) throw new Error(`title/H1 non conforme: ${titleFindings.map((f) => f.label).join(', ')}`);
  const slug = slugify(frontmatter.slug || path.basename(frontmatter.__source, '.md'));
  if (!slug) throw new Error('slug vide');
  const answer = directAnswer(frontmatter, body);
  const faq = extractFaq(body);
  if (faq.length < 3) throw new Error(`FAQ insuffisante: 3 minimum, trouvé ${faq.length}`);
  const howTo = extractHowTo(body, frontmatter);
  const canonical = `${DOMAIN}/blog/${slug}`;
  const schemas = makeSchemas({ title, description: answer, slug, date: String(frontmatter.date), faq, howTo, repoRoot });
  const articleHtml = markdownToHtml(body);
  const metaDescription = answer.length <= 160 ? answer : `${answer.slice(0, 156).replace(/\s+\S*$/, '')}…`;

  return { slug, html: `<!DOCTYPE html>
<html lang="pt-PT">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${escapeHtml(frontmatter.metaTitle || title)}</title>
  <meta name="description" content="${escapeHtml(metaDescription)}">
  <link rel="canonical" href="${canonical}">
  <meta property="og:title" content="${escapeHtml(title)}">
  <meta property="og:description" content="${escapeHtml(metaDescription)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="${canonical}">
  <meta property="og:locale" content="pt_PT">
  <meta name="twitter:card" content="summary">
  ${schemas.map(jsonLd).join('\n  ')}
  <style>
    :root{--orange:#d95f02;--navy:#10324a;--ink:#1f2933;--muted:#5b6770;--paper:#fff;--soft:#f4f7f9;--line:#d8e0e5}
    *{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--soft);color:var(--ink);font:17px/1.75 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
    a{color:#a84300;text-decoration-thickness:.08em;text-underline-offset:.15em}header,main,footer{width:min(900px,calc(100% - 32px));margin:auto}.topbar{background:var(--navy);color:#fff;padding:14px 0}.topbar a{color:#fff}.topbar .inner{width:min(900px,calc(100% - 32px));margin:auto;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
    main{background:var(--paper);padding:clamp(22px,5vw,52px);margin-top:24px;margin-bottom:90px;border-radius:12px;box-shadow:0 8px 30px #102a4312}h1,h2,h3{line-height:1.22;color:var(--navy)}h1{font-size:clamp(2rem,5vw,3.2rem);margin-top:0}h2{font-size:1.65rem;margin-top:2.5em;border-bottom:2px solid var(--line);padding-bottom:.35em}h3{font-size:1.25rem;margin-top:1.8em}.direct-answer,.price-box,.trust-box,.evidence-box{padding:20px;border-radius:10px;margin:24px 0}.direct-answer{font-size:1.12rem;background:#fff4e8;border-left:5px solid var(--orange)}.price-box{background:#edf5f8;border-left:5px solid var(--navy)}.trust-box{background:#f7f4ff;border-left:5px solid #6741a5}.evidence-box{background:#f8fafb;border:1px solid var(--line)}.table-wrap{overflow-x:auto}table{border-collapse:collapse;width:100%;margin:1.5em 0}th,td{border:1px solid var(--line);padding:10px;text-align:left}th{background:var(--navy);color:#fff}blockquote{margin:1.5em 0;padding:12px 18px;border-left:4px solid var(--orange);background:#fff8f1}code{background:#eef1f3;padding:.1em .3em;border-radius:4px}pre{overflow:auto;background:#15202b;color:#fff;padding:16px;border-radius:8px}footer{color:var(--muted);padding:0 0 110px}.sticky-cta{position:fixed;left:0;right:0;bottom:0;z-index:20;background:#0d2d40ed;backdrop-filter:blur(8px);padding:12px}.sticky-cta .inner{width:min(900px,calc(100% - 24px));margin:auto;display:flex;gap:10px}.sticky-cta a{flex:1;text-align:center;text-decoration:none;font-weight:750;padding:12px;border-radius:8px}.call{background:var(--orange);color:#fff}.whatsapp{background:#1f9d55;color:#fff}.skip-link{position:absolute;left:-9999px}.skip-link:focus{left:8px;top:8px;background:#fff;padding:8px;z-index:30}@media(max-width:600px){body{font-size:16px}main{width:100%;margin-top:0;border-radius:0;padding:22px 16px}.topbar .inner{display:block}.sticky-cta .inner{width:100%}}
  </style>
</head>
<body>
  <a class="skip-link" href="#conteudo">Saltar para o conteúdo</a>
  <div class="topbar"><div class="inner"><a href="/">⚡ Eletricista Urgente</a><span>Atendimento 24h/7 dias · Trás-os-Montes</span></div></div>
  <main id="conteudo">
    <nav aria-label="Navegação estrutural"><a href="/">Início</a> › <a href="/blog/">Blog</a> › ${escapeHtml(title)}</nav>
    <article>
      <h1>${escapeHtml(h1)}</h1>
      <p class="direct-answer">${escapeHtml(answer)}</p>
      <section class="price-box" aria-labelledby="preco-transparente">
        <h2 id="preco-transparente">Preço transparente antes do trabalho</h2>
        <p><strong>${PRICE_TEXT}</strong> de mão de obra · Deslocação: <strong>${ZONES_TEXT}</strong> · Noite, domingo e feriado: <strong>+50 %</strong>.</p>
        <p><strong>Orçamento por escrito antes de qualquer intervenção, sem surpresas.</strong></p>
      </section>
      <section class="trust-box" aria-labelledby="quem-atende">
        <h2 id="quem-atende">Quem atende</h2>
        <p>Na Staff-Seekers / Norte Reparos, <strong>fala sempre com a mesma pessoa, não um call center</strong>. Explicamos o diagnóstico e o trabalho necessário antes de intervir. Emitimos fatura com NIF e damos garantia escrita do trabalho executado.</p>
      </section>
      ${articleHtml}
      <section class="evidence-box" aria-labelledby="relatos-verificados">
        <h2 id="relatos-verificados">Relatos de intervenção verificados</h2>
        <p>Esta secção está preparada para receber apenas intervenções documentadas e autorizadas pelos clientes. Enquanto não dispomos dessa confirmação, não publicamos nomes, locais, preços, fotografias ou histórias de trabalhos.</p>
      </section>
      <section class="price-box" aria-labelledby="contacto-urgente">
        <h2 id="contacto-urgente">Precisa de ajuda com uma avaria elétrica?</h2>
        <p>Não toque em cabos expostos, tomadas quentes ou componentes com sinais de queimadura. Se for seguro, desligue o circuito e contacte-nos.</p>
        <p><a href="tel:${PHONE_E164}"><strong>${PHONE_DISPLAY}</strong></a> · <a href="${WHATSAPP}">WhatsApp</a></p>
      </section>
    </article>
  </main>
  <footer><p>Conteúdo informativo da Norte Reparos · Atualizado em ${escapeHtml(String(frontmatter.date))} · <a href="/contactos">Contactos</a></p></footer>
  <div class="sticky-cta" aria-label="Contactos rápidos"><div class="inner"><a class="call" href="tel:${PHONE_E164}">Ligar ${PHONE_DISPLAY}</a><a class="whatsapp" href="${WHATSAPP}">WhatsApp</a></div></div>
</body>
</html>\n` };
}

function listSources(sourcePath) {
  const stat = fs.statSync(sourcePath);
  if (stat.isFile()) return [sourcePath];
  if (!stat.isDirectory()) throw new Error('source doit être un fichier ou un dossier');
  return fs.readdirSync(sourcePath).filter((name) => name.endsWith('.md')).sort().map((name) => path.join(sourcePath, name));
}

function main() {
  let args;
  try { args = parseArgs(process.argv.slice(2)); } catch (error) { die(error.message); return; }
  if (args.help) { help(); return; }
  const repoRoot = path.resolve(__dirname, '..');
  const sourcePath = path.resolve(args.source);
  const outDir = path.resolve(args.outDir);
  let files;
  try { files = listSources(sourcePath); } catch (error) { die(`SOURCE ERROR: ${error.message}`); return; }
  if (!files.length) { die('SOURCE ERROR: aucun Markdown trouvé'); return; }
  if (files.length > BATCH_LIMIT) { die(`BATCH BLOCK: ${files.length} sources dépassent R15 (${BATCH_LIMIT})`); return; }

  const rendered = [];
  const blocked = [];
  for (const file of files) {
    try {
      const source = fs.readFileSync(file, 'utf8');
      const findings = auditConformity(source);
      if (findings.length) {
        blocked.push({ file, findings });
        continue;
      }
      const parsed = parseFrontmatter(source);
      parsed.data.__source = file;
      const page = renderPage(parsed, repoRoot);
      rendered.push({ file, ...page });
    } catch (error) {
      blocked.push({ file, findings: [{ label: error.message, sample: '' }] });
    }
  }

  if (blocked.length) {
    console.error(`CONFORMITY BLOCK: ${blocked.length}/${files.length} source(s) refusée(s)`);
    for (const item of blocked) {
      console.error(`- ${path.relative(repoRoot, item.file)}: ${item.findings.map((f) => `${f.label}${f.sample ? ` [${f.sample}]` : ''}`).join('; ')}`);
    }
    process.exitCode = 2;
    return;
  }

  if (!args.dryRun) fs.mkdirSync(outDir, { recursive: true });
  for (const page of rendered) {
    const target = path.join(outDir, `${page.slug}.html`);
    if (!args.dryRun) fs.writeFileSync(target, page.html, 'utf8');
    console.log(`${args.dryRun ? 'VALID' : 'WRITE'} ${path.relative(repoRoot, page.file)} -> ${path.relative(repoRoot, target)}`);
  }
  console.log(`generated=${rendered.length} blocked=0 dry_run=${args.dryRun}`);
}

if (require.main === module) main();

module.exports = { auditConformity, markdownToHtml, parseFrontmatter, renderPage };
