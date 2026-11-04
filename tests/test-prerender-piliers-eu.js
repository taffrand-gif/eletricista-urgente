#!/usr/bin/env node

const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync } = require('node:child_process');

const repo = path.resolve(__dirname, '..');
const sourceScript = path.join(repo, 'scripts', 'prerender-piliers-eu.mjs');
const trackingSource = path.join(repo, 'eletricista-urgente-braganca.html');
const outputs = [
  { file: 'eletricista-urgente-braganca.html', route: '/eletricista-urgente-braganca' },
  { file: 'eletricista-urgente-macedo-de-cavaleiros.html', route: '/eletricista-urgente-macedo-de-cavaleiros' },
  { file: 'eletricista-urgente-mirandela.html', route: '/eletricista-urgente-mirandela' },
];
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'eu-prerender-test-'));
const digest = (value) => crypto.createHash('sha256').update(value).digest('hex');

try {
  fs.mkdirSync(path.join(tmp, 'scripts'), { recursive: true });
  fs.copyFileSync(sourceScript, path.join(tmp, 'scripts', 'prerender-piliers-eu.mjs'));
  fs.copyFileSync(trackingSource, path.join(tmp, 'eletricista-urgente-braganca.html'));

  execFileSync('git', ['init', '-q'], { cwd: tmp });
  execFileSync('git', ['config', 'user.name', 'EU generator test'], { cwd: tmp });
  execFileSync('git', ['config', 'user.email', 'eu-generator-test@example.invalid'], { cwd: tmp });
  execFileSync('git', ['add', 'eletricista-urgente-braganca.html', 'scripts/prerender-piliers-eu.mjs'], { cwd: tmp });
  execFileSync('git', ['commit', '-q', '-m', 'temporary generator test fixture'], { cwd: tmp });

  const run = () => execFileSync(process.execPath, [path.join(tmp, 'scripts', 'prerender-piliers-eu.mjs')], {
    cwd: tmp,
    encoding: 'utf8',
  });

  const firstRun = run();
  for (const page of outputs) assert.match(firstRun, new RegExp(`WROTE ${page.route.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`));
  const first = new Map();

  for (const page of outputs) {
    const output = path.join(tmp, page.file);
    assert.equal(fs.existsSync(output), true, `${page.file} must be generated`);
    const html = fs.readFileSync(output, 'utf8');
    first.set(page.file, digest(html));

    assert.match(html, /<html lang="pt-PT">/);
    assert.match(html, /<link rel="canonical" href="https:\/\/eletricista-urgente\.pt/);
    assert.match(html, /<td>Dias úteis, 09:00–18:00<\/td>/);
    assert.doesNotMatch(html, /09:00\s+às\s+17:00|09:00\s*[–—-]\s*17:00/);
    assert.match(html, /70 €\/hora/);
    assert.match(html, /30 €/);
    assert.match(html, /100 €\/hora/);
    assert.match(html, /50 €/);
    assert.doesNotMatch(html, /\b(?:15|25|35|45|55|65)\s*€|\bZ[1-6]\b|\bZona\s*[1-6]\b|\+\s*50\s*%/i);
    assert.doesNotMatch(html, /\b(?:chegamos?|chegada)\b.{0,40}\b\d+\s*(?:min(?:utos?)?|h(?:oras?)?)\b/i,
      'generated pages must not promise a numeric arrival ETA');

    const ldBlocks = [...html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)];
    assert.equal(ldBlocks.length, 1, 'one JSON-LD graph is expected');
    const graph = JSON.parse(ldBlocks[0][1])['@graph'];
    const faq = graph.find((item) => item['@type'] === 'FAQPage');
    const priceAnswer = faq.mainEntity.find((item) => item.name.startsWith('Quanto custa'));
    assert.match(priceAnswer.acceptedAnswer.text, /09:00 às 18:00/);
    assert.match(priceAnswer.acceptedAnswer.text, /70 €/);
    assert.match(priceAnswer.acceptedAnswer.text, /30 €/);
    assert.match(priceAnswer.acceptedAnswer.text, /100 €/);
    assert.match(priceAnswer.acceptedAnswer.text, /50 €/);
  }

  run();
  for (const page of outputs) {
    const html = fs.readFileSync(path.join(tmp, page.file), 'utf8');
    assert.equal(digest(html), first.get(page.file), `${page.file} generation must be idempotent`);
  }

  console.log('prerender-piliers-eu tests: PASS (3 outputs, 09:00–18:00, current grid, idempotent)');
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}
