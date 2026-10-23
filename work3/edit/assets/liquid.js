// Liquid Morph background (from .claude/skills/motion-liquid-morph/template.html, draw() unchanged in spirit):
// chrome metaballs merging/splitting with an iridescent sheen. Repositioned and recoloured to sit behind a talking head.
(function () {
  const LOOP = 12;                       // seconds per seamless orbit
  const COL = { bg: '#0e0710', c1: '#f5c542', c2: '#e0303a', c3: '#4a74ff' };
  const W = 1080, H = 1920, U = Math.min(W, H);
  const CX = W * 0.5, CY = H * 0.42;      // centred on head/shoulders
  const ORB = 1.55, RAD = 1.35;           // orbit and blob size multipliers
  const cv = document.getElementById('liquid'); cv.width = W; cv.height = H;
  const ctx = cv.getContext('2d');
  const TAU = Math.PI * 2, clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x)), lerp = (a, b, t) => a + (b - a) * t;
  const hexRGB = h => { const n = parseInt(h.slice(1), 16); return [n >> 16 & 255, n >> 8 & 255, n & 255]; };
  const SC = 3, bw = Math.ceil(W / SC), bh = Math.ceil(H / SC);
  const buf = document.createElement('canvas'); buf.width = bw; buf.height = bh;
  const bx = buf.getContext('2d'), img = bx.createImageData(bw, bh);
  const A = hexRGB(COL.c1), B = hexRGB(COL.c2), C = hexRGB(COL.c3), BG = hexRGB(COL.bg);
  const NB = 5;
  function balls(t) {
    const T = t / LOOP * TAU, out = [];
    for (let i = 0; i < NB; i++) {
      const k = i / NB * TAU;
      const rr = U * (.085 + .025 * Math.sin(T * 2 + i)) * (i === 0 ? 1.3 : 1) * RAD;
      const orb = U * (.2 + .1 * Math.sin(T + i * 1.7)) * (i === 0 ? .15 : 1) * ORB;
      out.push([CX + Math.cos(k + T * (i % 2 ? 1 : -1)) * orb, CY + Math.sin(k * 1.3 + T * (i % 2 ? 1 : -1)) * orb * 1.25, rr]);
    }
    return out;
  }
  function draw(t) {
    const bs = balls(t), d = img.data, T = t / LOOP * TAU;
    for (let j = 0; j < bh; j++) {
      const y = j * SC;
      for (let i = 0; i < bw; i++) {
        const x = i * SC; let f = 0, gx = 0, gy = 0;
        for (const b of bs) { const dx = x - b[0], dy = y - b[1], r2 = dx * dx + dy * dy + 1, v = b[2] * b[2] / r2; f += v; gx += -2 * v * dx / r2; gy += -2 * v * dy / r2; }
        const o = (j * bw + i) * 4;
        // ambient glow of the field so the dark backdrop is never flat
        const glow = clamp(f * .55) * .22;
        const edge = clamp((f - 1) / .06);
        // transparent canvas: only a soft warm haze around the field plus the blobs themselves
        let r = 255, g = 170, bl = 120, al = glow * 0.55;
        if (edge > 0) {
          const hk = U * .05 / Math.sqrt(Math.max(f - .95, .02));
          let nx = -gx * hk, ny = -gy * hk, nz = 1; const nl = Math.hypot(nx, ny, nz); nx /= nl; ny /= nl; nz /= nl;
          const h = nx * .18 - ny * .14 + y / H * .7 + x / W * .15 + T * .1;
          const w1 = .5 + .5 * Math.cos(h * TAU), w2 = .5 + .5 * Math.cos((h - .33) * TAU), w3 = .5 + .5 * Math.cos((h - .66) * TAU);
          const ws = w1 + w2 + w3 + 1e-3;
          let cr = (A[0] * w1 + B[0] * w2 + C[0] * w3) / ws, cg = (A[1] * w1 + B[1] * w2 + C[1] * w3) / ws, cb = (A[2] * w1 + B[2] * w2 + C[2] * w3) / ws;
          const rim = Math.pow(1 - nz, 3), spec = Math.pow(clamp(-nx * .5 - ny * .6 + nz * .62), 40), diff = .62 + .38 * nz;
          cr = cr * diff * (1 - rim * .25) + 255 * spec * .95 + 40 * rim; cg = cg * diff * (1 - rim * .25) + 255 * spec * .95 + 30 * rim; cb = cb * diff * (1 - rim * .2) + 255 * spec * .95 + 60 * rim;
          r = lerp(r, clamp(cr, 0, 255), edge); g = lerp(g, clamp(cg, 0, 255), edge); bl = lerp(bl, clamp(cb, 0, 255), edge);
          al = lerp(al, 0.9, edge);
        }
        d[o] = r; d[o + 1] = g; d[o + 2] = bl; d[o + 3] = al * 255;
      }
    }
    bx.putImageData(img, 0, 0);
    ctx.clearRect(0, 0, W, H);
    ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = 'high';
    ctx.drawImage(buf, 0, 0, bw * SC, bh * SC);
  }
  window.renderLiquid = t => draw(((t % LOOP) + LOOP) % LOOP);
  window.addEventListener('hf-seek', e => window.renderLiquid(e.detail.time));
  window.renderLiquid(0);
})();
