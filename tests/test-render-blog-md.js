#!/usr/bin/env node

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync, spawnSync } = require('node:child_process');

const repo = path.resolve(__dirname, '..');
const script = path.join(repo, 'scripts', 'render-blog-md.js');
const { auditConformity } = require(script);
const fixture = path.join(repo, 'tests', 'fixtures', 'blog-safe.md');
const unsafeFixture = path.join(repo, 'tests', 'fixtures', 'blog-unsafe.md');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'eu-blog-render-'));

try {
  const rendered = execFileSync(process.execPath, [script, '--source', fixture, '--out-dir', tmp], {
    cwd: repo,
    encoding: 'utf8',
  });
  const output = path.join(tmp, 'teste-seguranca-eletrica.html');
  assert.match(rendered, /generated=1/);
  assert.equal(fs.existsSync(output), true, 'renderer must create one HTML file');

  const html = fs.readFileSync(output, 'utf8');
  assert.match(html, /<html lang="pt-PT">/);
  assert.match(html, /<h1>Teste de Segurança Elétrica<\/h1>/);
  assert.match(html, /class="direct-answer"/);
  assert.match(html, /70 €\/h/);
  assert.match(html, /Z1=15 € \/ Z2=25 € \/ Z3=35 € \/ Z4=45 € \/ Z5=55 € \/ Z6=65 €/);
  assert.match(html, /orçamento por escrito antes de qualquer intervenção, sem surpresas/i);
  assert.match(html, /fala sempre com a mesma pessoa, não um call center/i);
  assert.match(html, /href="tel:\+351932321892"/);
  assert.match(html, /"@type":"EmergencyService"/);
  assert.match(html, /"@type":"Service"/);
  assert.match(html, /"@type":"FAQPage"/);
  assert.match(html, /"@type":"HowTo"/);
  assert.match(html, /Relatos de intervenção verificados/);
  assert.doesNotMatch(html, /Maria S\.|exemplo real|relatório técnico|certificad[oa] em|resposta prioritária/i);

  const safeFindings = auditConformity(html);
  assert.equal(safeFindings.length, 0, `generated HTML must pass conformity gate: ${JSON.stringify(safeFindings)}`);

  const ldBlocks = [...html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)];
  assert.ok(ldBlocks.length >= 3, 'renderer must emit at least three JSON-LD blocks');
  for (const match of ldBlocks) JSON.parse(match[1]);

  const firstParagraph = html.match(/<p class="direct-answer">([\s\S]*?)<\/p>/);
  assert.ok(firstParagraph, 'direct answer paragraph is required');
  const firstText = firstParagraph[1].replace(/<[^>]+>/g, ' ').trim();
  const firstWords = firstText.split(/\s+/).filter(Boolean).length;
  assert.ok(firstWords >= 40 && firstWords <= 60, `direct answer must be 40-60 words, got ${firstWords}`);

  const paragraphs = [...html.matchAll(/<p(?:\s[^>]*)?>([\s\S]*?)<\/p>/g)].map((m) => m[1]);
  assert.ok(paragraphs.some((p) => p.includes('<strong>texto forte</strong>')));
  assert.ok(paragraphs.some((p) => p.includes('<a href="/contactos">link interno</a>')));
  assert.match(html, /<table>/);
  assert.match(html, /<ul>/);

  const unsafe = spawnSync(process.execPath, [script, '--source', unsafeFixture, '--out-dir', tmp], {
    cwd: repo,
    encoding: 'utf8',
  });
  assert.notEqual(unsafe.status, 0, 'renderer must reject unsafe source content');
  assert.match(`${unsafe.stdout}\n${unsafe.stderr}`, /CONFORMITY BLOCK/i);
  assert.equal(fs.existsSync(path.join(tmp, 'conteudo-inseguro.html')), false);

  const badTitleFixture = path.join(tmp, 'bad-title.md');
  fs.writeFileSync(badTitleFixture, fs.readFileSync(fixture, 'utf8').replaceAll('Teste de Segurança Elétrica', 'Canalizador em Bragança'), 'utf8');
  const badTitle = spawnSync(process.execPath, [script, '--source', badTitleFixture, '--out-dir', tmp], {
    cwd: repo,
    encoding: 'utf8',
  });
  assert.notEqual(badTitle.status, 0, 'renderer must reject an unsafe title/H1');
  assert.equal(fs.existsSync(path.join(tmp, 'teste-seguranca-eletrica.html')), true, 'safe output remains intact');

  const dryRun = execFileSync(process.execPath, [script, '--source', fixture, '--out-dir', tmp, '--dry-run'], {
    cwd: repo,
    encoding: 'utf8',
  });
  assert.match(dryRun, /dry_run=true/);

  console.log('render-blog-md tests: PASS');
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}
