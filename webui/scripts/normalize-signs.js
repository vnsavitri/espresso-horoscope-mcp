const fs = require('fs');
const path = require('path');
const { optimize } = require('svgo');
const cheerio = require('cheerio');

const SRC = path.resolve('public/signs-src');
const OUT = path.resolve('public/signs');

const CANVAS_W = 128.5201;
const CANVAS_H = 198.64;
const GOLD = '#BDAC82';

if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });

const files = fs.readdirSync(SRC).filter(f => f.endsWith('.svg'));
for (const file of files) {
  const raw = fs.readFileSync(path.join(SRC, file), 'utf8');

  // keep original viewBox for scale math
  const vbMatch = raw.match(/viewBox="([\d.\-\s]+)"/);
  const orig = vbMatch ? vbMatch[1].split(/\s+/).map(Number) : [0,0, CANVAS_W, CANVAS_H];
  const [ox, oy, ow, oh] = orig;

  const svgo = optimize(raw, { path: file, multipass: true, configFile: path.resolve('.svgo.config.cjs') });
  const $ = cheerio.load(svgo.data, { xmlMode: true });
  const $svg = $('svg');

  // wrap all non-defs in a single group
  const g = $('<g id="sign-glyph"/>');
  $svg.children().toArray().forEach(n => {
    if (n.tagName !== 'defs') g.append($(n));
  });
  $svg.children().remove();
  const $defs = $('defs');
  if ($defs.length) $svg.append($defs);
  $svg.append(g);

  // compute uniform scale from original viewBox to target canvas
  const sx = CANVAS_W / ow;
  const sy = CANVAS_H / oh;
  const s = Math.min(sx, sy);
  const tx = (CANVAS_W - ow * s) / 2 - ox * s;
  const ty = (CANVAS_H - oh * s) / 2 - oy * s;
  g.attr('transform', `translate(${tx.toFixed(3)} ${ty.toFixed(3)}) scale(${s.toFixed(6)})`);

  // normalize styles
  $('path,circle,ellipse,line,polyline,polygon,rect').each((_, el) => {
    const $el = $(el);
    if (!$el.attr('fill') || $el.attr('fill') === 'none') $el.attr('fill', 'none');
    $el.attr('stroke', GOLD);
    $el.attr('stroke-width', '1.5');
    $el.attr('stroke-linecap', 'round');
    $el.attr('stroke-linejoin', 'round');
  });

  // final canvas
  $svg.attr('id', 'sign-svg');
  $svg.attr('xmlns', 'http://www.w3.org/2000/svg');
  $svg.attr('width', CANVAS_W);
  $svg.attr('height', CANVAS_H);
  $svg.attr('viewBox', `0 0 ${CANVAS_W} ${CANVAS_H}`);
  $svg.attr('preserveAspectRatio', 'xMidYMid meet');

  // write out
  const outPath = path.join(OUT, file.replace('sagitarius', 'sagittarius'));
  fs.writeFileSync(outPath, $.xml().replace(/>\s+</g, '>\n<'), 'utf8');
  console.log('✓ normalized:', path.basename(outPath));
}
console.log('Done:', OUT);
